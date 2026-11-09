import importlib.util
import json
import os
from contextlib import ExitStack, contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def load_lane(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "src" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def response(rows=None, status=200, text=""):
    result = Mock(status_code=status, text=text)
    result.json.return_value = [] if rows is None else rows
    return result


def backend(**overrides):
    return {
        "enabled": True,
        "use_bm25_rpc": True,
        "use_vector_rpc": True,
        "url": "https://example.supabase.co",
        "anon_key": "test-key",
        "schema": "public",
        **overrides,
    }


def query(sources=None):
    return {
        "type": "keyword",
        "tag": "ML",
        "paper_tag": "keyword:ML",
        "query_text": "machine learning",
        "paper_sources": sources or ["arxiv"],
        "query_embedding": [1.0, 0.0],
        "embedding_cache": {"embedding": [1.0, 0.0]},
    }


class DailyRecallFailureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lanes = {
            "bm25": load_lane("daily_failure_bm25", "2.1.retrieval_papers_bm25.py"),
            "embedding": load_lane("daily_failure_embedding", "2.2.retrieval_papers_embedding.py"),
        }

    def rank(self, lane, module, *, conf=None, start=None, end=None, mode="exact"):
        args = {
            "queries": [query()],
            "top_k": 5,
            "supabase_conf": backend() if conf is None else conf,
            "start_dt": start,
            "end_dt": end,
        }
        if lane == "embedding":
            args.update(model=None, rpc_mode=mode)
        return module.rank_papers_for_queries_via_supabase(**args)

    @contextmanager
    def daily(self, lane, module, *, sources=None, backends=None, raw=None,
              explicit_input=False, multi=False):
        with tempfile.TemporaryDirectory() as directory, ExitStack() as stack:
            root = Path(directory)
            raw_dir = root / "raw"
            filtered_dir = root / "filtered"
            input_path = raw_dir / "papers.json"
            if raw is not None:
                raw_dir.mkdir()
                input_path.write_text(json.dumps(raw), encoding="utf-8")
            output_name = "papers" if raw is not None else f"arxiv_papers_{module.TODAY_STR}"
            output = (filtered_dir / "explicit.json" if explicit_input else
                      filtered_dir / f"{output_name}.{lane}.json")
            argv = ["recall", "--top-k", "5"]
            if explicit_input:
                argv += ["--input", str(input_path), "--output", str(output)]
            source_backends = backends or {source: backend() for source in (sources or ["arxiv"])}
            stack.enter_context(patch.dict(os.environ, {
                "DPR_ENABLE_MULTI_SOURCE_RPC": "1" if multi else "0",
            }, clear=True))
            stack.enter_context(patch.object(sys, "argv", argv))
            stack.enter_context(patch.object(module, "RAW_DIR", str(raw_dir)))
            stack.enter_context(patch.object(module, "FILTERED_DIR", str(filtered_dir)))
            stack.enter_context(patch.object(module, "load_config", return_value={}))
            stack.enter_context(patch.object(module, "build_pipeline_inputs", return_value={
                f"{lane}_queries": [query(sources)],
            }))
            stack.enter_context(patch.object(module, "get_supabase_read_config",
                                            return_value=source_backends.get("arxiv", {})))
            stack.enter_context(patch.object(module, "get_source_backend",
                                            side_effect=lambda _config, source: source_backends.get(source, {})))
            stack.enter_context(patch.object(module, "count_papers_by_date_range",
                                            return_value=(None, "count unavailable")))
            start = datetime(2026, 3, 1, tzinfo=timezone.utc)
            stack.enter_context(patch.object(module, "resolve_supabase_recall_window",
                                            return_value=(start, start + timedelta(days=1))))
            if lane == "embedding":
                # Cached queries and precomputed paper vectors need no model loading.
                filter_factory = stack.enter_context(patch.object(
                    module, "EmbeddingCoarseFilter", return_value=Mock(model=None)))
            else:
                filter_factory = None
            yield output, filter_factory

    def test_provider_failures_raise_instead_of_returning_empty_recall(self):
        failures = [
            {"side_effect": requests.ConnectionError("DNS lookup failed")},
            {"return_value": response(status=503, text="unavailable")},
            {"return_value": response(rows={"unexpected": "object"})},
            {"return_value": response(status=500, text='{"code":"57014"}')},
        ]
        start = datetime(2026, 3, 1, tzinfo=timezone.utc)
        for lane, module in self.lanes.items():
            for failure in failures:
                for bounded in (False, True):
                    with self.subTest(lane=lane, failure=failure, bounded=bounded):
                        with patch("supabase_source._request_with_retries", **failure):
                            with self.assertRaises(RuntimeError):
                                self.rank(lane, module, start=start if bounded else None,
                                          end=start + timedelta(days=2) if bounded else None)

    def test_partial_shard_failures_raise_even_with_nonzero_hits(self):
        start = datetime(2026, 3, 1, tzinfo=timezone.utc)
        row = {"id": "p1", "published": "2026-03-02T00:00:00+00:00",
               "score": 1.0, "similarity": 1.0}
        for lane, module in self.lanes.items():
            for rows in ([], [row]):
                with self.subTest(lane=lane, rows=rows):
                    with patch("supabase_source._request_with_retries", side_effect=[
                        response(rows), response(status=503, text="unavailable"),
                    ]):
                        with self.assertRaises(RuntimeError):
                            self.rank(lane, module, start=start, end=start + timedelta(days=8))

    def test_vector_ann_failure_also_raises(self):
        with patch("supabase_source._request_with_retries", return_value=response(status=503)):
            with self.assertRaises(RuntimeError):
                self.rank("embedding", self.lanes["embedding"], mode="ann")

    def test_successful_zero_result_preserves_query_metadata(self):
        for lane, module in self.lanes.items():
            with self.subTest(lane=lane):
                with patch("supabase_source._request_with_retries", return_value=response()):
                    result = self.rank(lane, module)
                self.assertEqual(result["total_hits"], 0)
                self.assertEqual(result["papers"], {})
                self.assertEqual(len(result["queries"]), 1)
                self.assertEqual(result["queries"][0]["query_text"], "machine learning")
                self.assertEqual(result["queries"][0]["paper_tag"], "keyword:ML")
                self.assertEqual(result["queries"][0]["sim_scores"], {})

    def test_missing_credentials_raise(self):
        for lane, module in self.lanes.items():
            for missing in ("url", "anon_key"):
                with self.subTest(lane=lane, missing=missing):
                    with self.assertRaises(RuntimeError):
                        self.rank(lane, module, conf=backend(**{missing: ""}))
                    with self.daily(lane, module, backends={"arxiv": backend(**{missing: ""})},
                                    raw=[{"id": "p1", "title": "machine learning"}]) as (output, _):
                        with self.assertRaises(RuntimeError):
                            module.main()
                        self.assertFalse(output.exists())

    def test_daily_successful_empty_provider_writes_without_raw(self):
        for lane, module in self.lanes.items():
            for explicit_input in (False, True):
                for multi in (False, True):
                    sources = ["arxiv", "biorxiv"] if multi else ["arxiv"]
                    with self.subTest(lane=lane, explicit=explicit_input, multi=multi):
                        with self.daily(lane, module, sources=sources, explicit_input=explicit_input,
                                        multi=multi) as (output, filter_factory):
                            with patch("supabase_source._request_with_retries", return_value=response()):
                                module.main()
                            payload = json.loads(output.read_text(encoding="utf-8"))
                            self.assertEqual(payload["papers"], [])
                            self.assertEqual(len(payload["queries"]), 1)
                            self.assertEqual(payload["queries"][0]["paper_sources"], sources)
                            self.assertEqual(payload["queries"][0]["sim_scores"], {})
                            if filter_factory is not None:
                                filter_factory.assert_not_called()

    def test_daily_failed_or_disabled_arxiv_without_raw_cannot_write(self):
        for lane, module in self.lanes.items():
            for enabled in (False, True):
                for sources in (["arxiv"], ["arxiv", "biorxiv"]):
                    with self.subTest(lane=lane, enabled=enabled, sources=sources):
                        backends = {source: backend() for source in sources}
                        backends["arxiv"]["enabled"] = enabled
                        with self.daily(lane, module, sources=sources, backends=backends) as (output, _):
                            with patch("supabase_source._request_with_retries",
                                       return_value=response(status=503)):
                                with self.assertRaises((RuntimeError, FileNotFoundError)):
                                    module.main()
                            self.assertFalse(output.exists())

    def test_other_source_failures_cannot_disappear_behind_successful_arxiv(self):
        for lane, module in self.lanes.items():
            with self.subTest(lane=lane):
                with self.daily(lane, module, sources=["arxiv", "biorxiv"]) as (output, _):
                    with patch("supabase_source._request_with_retries", side_effect=[
                        response(), response(status=503),
                    ]):
                        with self.assertRaises(RuntimeError):
                            module.main()
                    self.assertFalse(output.exists())

    def test_arxiv_failure_cannot_disappear_behind_other_source_success(self):
        for lane, module in self.lanes.items():
            with self.subTest(lane=lane):
                with self.daily(lane, module, sources=["arxiv", "biorxiv"]) as (output, _):
                    with patch("supabase_source._request_with_retries", side_effect=[
                        response(status=503), response(),
                    ]):
                        with self.assertRaises(FileNotFoundError):
                            module.main()
                    self.assertFalse(output.exists())

    def test_unconfigured_or_disabled_other_source_fails(self):
        for lane, module in self.lanes.items():
            for other in ({}, backend(enabled=False)):
                with self.subTest(lane=lane, other=other):
                    with self.daily(lane, module, sources=["arxiv", "biorxiv"], backends={
                        "arxiv": backend(), "biorxiv": other,
                    }) as (output, _):
                        with patch("supabase_source._request_with_retries", return_value=response()):
                            with self.assertRaises(RuntimeError):
                                module.main()
                        self.assertFalse(output.exists())

    def test_nonzero_local_arxiv_recall_survives_failure_disabled_or_empty_provider(self):
        raw = [{"id": "p1", "title": "machine learning", "abstract": "learning",
                "embedding": [1.0, 0.0]}]
        for lane, module in self.lanes.items():
            for state, multi in (("failure", False), ("disabled", False), ("empty", False),
                                 ("disabled", True), ("empty", True)):
                with self.subTest(lane=lane, state=state, multi=multi):
                    sources = ["arxiv", "biorxiv"] if multi else ["arxiv"]
                    backends = {source: backend() for source in sources}
                    backends["arxiv"]["enabled"] = state != "disabled"
                    with self.daily(lane, module, raw=raw, sources=sources,
                                    backends=backends, multi=multi) as (output, _):
                        rpc_response = response(status=503) if state == "failure" else response()
                        with patch("supabase_source._request_with_retries", return_value=rpc_response):
                            module.main()
                        payload = json.loads(output.read_text(encoding="utf-8"))
                        self.assertEqual([paper["id"] for paper in payload["papers"]], ["p1"])
                        self.assertIn("p1", payload["queries"][0]["sim_scores"])

    def test_successful_empty_provider_with_empty_raw_stays_valid(self):
        for lane, module in self.lanes.items():
            with self.subTest(lane=lane):
                with self.daily(lane, module, raw=[]) as (output, filter_factory):
                    with patch("supabase_source._request_with_retries", return_value=response()):
                        module.main()
                    payload = json.loads(output.read_text(encoding="utf-8"))
                    self.assertEqual(payload["papers"], [])
                    self.assertEqual(payload["queries"][0]["sim_scores"], {})
                    if filter_factory is not None:
                        filter_factory.assert_not_called()

    def test_valid_empty_raw_remains_successful_with_failed_or_disabled_provider(self):
        for lane, module in self.lanes.items():
            for enabled in (False, True):
                with self.subTest(lane=lane, enabled=enabled):
                    with self.daily(lane, module, raw=[], backends={
                        "arxiv": backend(enabled=enabled),
                    }) as (output, filter_factory):
                        with patch("supabase_source._request_with_retries", return_value=response(status=503)):
                            module.main()
                        payload = json.loads(output.read_text(encoding="utf-8"))
                        self.assertEqual(payload["papers"], [])
                        self.assertEqual(len(payload["queries"]), 1)
                        self.assertEqual(payload["queries"][0]["sim_scores"], {})
                        if filter_factory is not None:
                            filter_factory.assert_not_called()

    def test_malformed_raw_without_successful_provider_fails(self):
        for lane, module in self.lanes.items():
            for raw in ({}, [{}], ["invalid"]):
                with self.subTest(lane=lane, raw=raw):
                    with self.daily(lane, module, raw=raw) as (output, _):
                        with patch("supabase_source._request_with_retries", return_value=response(status=503)):
                            with self.assertRaises(ValueError):
                                module.main()
                        self.assertFalse(output.exists())

    def test_disabled_source_never_uses_multi_source_backend(self):
        config = {"source_backends": {"arxiv": backend(), "biorxiv": backend()}}
        for lane, module in self.lanes.items():
            resolver = (module.resolve_multi_source_bm25_backend if lane == "bm25" else
                        module.resolve_multi_source_vector_backend)
            with self.subTest(lane=lane):
                with patch.dict(os.environ, {}, clear=True):
                    self.assertIsNotNone(resolver(config, [query(["arxiv", "biorxiv"])]))
                with patch.dict(os.environ, {"DPR_ARXIV_ENABLED": "0"}, clear=True):
                    self.assertIsNone(resolver(config, [query(["arxiv", "biorxiv"])]))


if __name__ == "__main__":
    unittest.main()
