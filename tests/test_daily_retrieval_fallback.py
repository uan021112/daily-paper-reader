"""Database outage fallback is per-run and must not confuse empty with failed."""

import copy
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import sys
from threading import Thread
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from main import _prepare_daily_fetch
from source_config import get_source_backend
from supabase_source import get_supabase_read_config


class BackendHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.server.request_count += 1
        body = self.server.body.encode("utf-8")
        self.send_response(self.server.status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class DailyRetrievalFallbackTest(unittest.TestCase):
    def setUp(self):
        self.environ = patch.dict(os.environ, {}, clear=True)
        self.environ.start()
        self.addCleanup(self.environ.stop)
        self.server = HTTPServer(("127.0.0.1", 0), BackendHandler)
        self.server.status = 200
        self.server.body = "[]"
        self.server.request_count = 0
        self.thread = Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop_server)
        self.config = {
            "arxiv_paper_setting": {"prefer_supabase_read": True},
            "source_backends": {
                "arxiv": {
                    "enabled": True,
                    "url": f"http://127.0.0.1:{self.server.server_port}",
                    "anon_key": "test-key",
                    "papers_table": "arxiv_papers",
                    "use_bm25_rpc": True,
                    "use_vector_rpc": True,
                },
                "biorxiv": {
                    "enabled": True,
                    "url": "https://other-source.invalid",
                    "anon_key": "other-key",
                    "papers_table": "biorxiv_papers",
                    "use_bm25_rpc": True,
                    "use_vector_rpc": True,
                },
            },
            "subscriptions": {
                "intent_profiles": [
                    {
                        "tag": "robotics",
                        "enabled": True,
                        "paper_sources": ["arxiv"],
                        "keywords": [{"keyword": "robot manipulation"}],
                    }
                ]
            },
        }

    def stop_server(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()

    def test_successful_empty_database_still_uses_database(self):
        self.assertTrue(_prepare_daily_fetch(self.config, None))
        self.assertTrue(get_supabase_read_config(self.config)["enabled"])
        self.assertTrue(get_source_backend(self.config, "arxiv")["use_vector_rpc"])

    def test_failure_switches_only_arxiv_without_rewriting_configuration(self):
        for status, body in (
            (403, json.dumps({"message": "permission denied"})),
            (200, json.dumps({"error": "invalid response"})),
            (200, "not json"),
        ):
            with self.subTest(status=status, body=body), patch.dict(os.environ, {}, clear=True):
                self.server.status, self.server.body = status, body
                original = copy.deepcopy(self.config)
                other_source = get_source_backend(self.config, "biorxiv")
                self.assertFalse(_prepare_daily_fetch(self.config, None))
                self.assertFalse(get_supabase_read_config(self.config)["enabled"])
                arxiv = get_source_backend(self.config, "arxiv")
                self.assertFalse(arxiv["use_bm25_rpc"])
                self.assertFalse(arxiv["use_vector_rpc"])
                self.assertEqual(get_source_backend(self.config, "biorxiv"), other_source)
                self.assertEqual(self.config, original)

    def test_other_source_queries_do_not_trigger_arxiv_fallback(self):
        self.config["subscriptions"]["intent_profiles"][0]["paper_sources"] = ["biorxiv"]
        self.server.status = 403
        self.assertTrue(_prepare_daily_fetch(self.config, None))
        self.assertEqual(self.server.request_count, 0)
        self.assertTrue(get_source_backend(self.config, "arxiv")["enabled"])


if __name__ == "__main__":
    unittest.main()
