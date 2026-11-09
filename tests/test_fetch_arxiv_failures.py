"""Direct arXiv failures must not publish partial data or advance state."""

import importlib.util
import json
from contextlib import ExitStack
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[1]



class FixedDateTime(datetime):
    @classmethod
    def now(cls, tz=None):
        value = cls(2026, 1, 5, tzinfo=timezone.utc)
        return value.astimezone(tz) if tz is not None else value.replace(tzinfo=None)

def _paper(pid="new-paper"):
    return SimpleNamespace(
        get_short_id=lambda: pid,
        entry_id=f"https://arxiv.org/abs/{pid}",
        title="A paper",
        summary="An abstract",
        authors=[SimpleNamespace(name="Author")],
        primary_category="cs.AI",
        categories=["cs.AI"],
        published=FixedDateTime(2026, 1, 2, tzinfo=timezone.utc),
    )


class ArxivFetchFailuresTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / "src" / "maintain" / "fetchers" / "fetch_arxiv.py"
        spec = importlib.util.spec_from_file_location("fetch_arxiv_failures_mod", path)
        cls.mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(cls.mod)

    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.directory = Path(self.stack.enter_context(TemporaryDirectory()))
        self.output = self.directory / "papers.json"
        self.seen = self.directory / "seen.json"
        self.crawl = self.directory / "crawl.json"
        self.output.write_text('[{"id": "existing"}]', encoding="utf-8")
        self.seen.write_text(json.dumps({
            "ids": ["existing"],
            "latest_published_at": "2026-01-01T00:00:00+00:00",
        }), encoding="utf-8")
        self.crawl.write_text(json.dumps({
            "last_crawl_at": "2026-01-01T00:00:00+00:00",
        }), encoding="utf-8")
        self.original = {p: p.read_bytes() for p in (self.output, self.seen, self.crawl)}
        self.start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.end = self.start + timedelta(days=4)
        self.client = Mock()
        for name, value in {
            "SEEN_IDS_FILE": str(self.seen),
            "CRAWL_STATE_FILE": str(self.crawl),
            "CATEGORIES_TO_FETCH": ["cs"],
        }.items():
            self.stack.enter_context(patch.object(self.mod, name, value))
        self.stack.enter_context(patch.object(self.mod, "load_config", return_value={}))
        self.stack.enter_context(patch.object(self.mod, "get_supabase_read_config", return_value={}))
        self.stack.enter_context(patch.object(self.mod, "iter_time_windows", return_value=[(self.start, self.end)]))
        self.stack.enter_context(patch.object(self.mod.arxiv, "Client", return_value=self.client))
        self.stack.enter_context(patch.object(self.mod.time, "sleep"))
        self.stack.enter_context(patch.object(self.mod, "datetime", FixedDateTime))
        for name in ("log", "group_start", "group_end"):
            self.stack.enter_context(patch.object(self.mod, name))

    def run_fetch(self):
        self.mod.fetch_all_domains_metadata_robust(
            days=7, output_file=str(self.output), disable_supabase_read=True,
        )

    def assert_unchanged(self):
        for path, original in self.original.items():
            with self.subTest(path=path.name):
                self.assertEqual(path.read_bytes(), original)

    def test_exhausted_subdivision_preserves_output_and_watermarks(self):
        self.client.results.side_effect = RuntimeError("transport exhausted")
        with self.assertRaisesRegex(RuntimeError, "transport exhausted"):
            self.run_fetch()
        self.assert_unchanged()

    def test_partial_iteration_failure_preserves_output_and_watermarks(self):
        def partial(_search):
            yield _paper()
            raise RuntimeError("connection lost during pagination")

        self.client.results.side_effect = partial
        with self.assertRaisesRegex(RuntimeError, "connection lost"):
            self.run_fetch()
        self.assert_unchanged()

    def test_invalid_entry_preserves_output_and_watermarks(self):
        self.client.results.side_effect = lambda _search: iter([_paper(), object()])
        with self.assertRaises(AttributeError):
            self.run_fetch()
        self.assert_unchanged()

    def test_failure_after_successful_category_preserves_state(self):
        with patch.object(self.mod, "CATEGORIES_TO_FETCH", ["cs", "math"]):
            self.client.results.side_effect = [
                iter([_paper()]), RuntimeError("category unavailable"),
                RuntimeError("category unavailable"),
            ]
            with self.assertRaisesRegex(RuntimeError, "category unavailable"):
                self.run_fetch()
        self.assert_unchanged()

    def test_successful_empty_fetch_writes_empty_array_and_advances_crawl(self):
        self.client.results.side_effect = lambda _search: iter(())
        self.run_fetch()
        self.assertEqual(json.loads(self.output.read_text(encoding="utf-8")), [])
        seen = json.loads(self.seen.read_text(encoding="utf-8"))
        self.assertEqual(seen["ids"], ["existing"])
        self.assertEqual(seen["latest_published_at"], "2026-01-01T00:00:00+00:00")
        crawl = json.loads(self.crawl.read_text(encoding="utf-8"))
        self.assertGreater(datetime.fromisoformat(crawl["last_crawl_at"]), self.start)

    def test_successful_bisection_publishes_both_child_results(self):
        self.client.results.side_effect = [
            RuntimeError("window too large"), iter([_paper("left")]), iter([_paper("right")]),
        ]
        self.run_fetch()
        papers = json.loads(self.output.read_text(encoding="utf-8"))
        self.assertEqual({paper["id"] for paper in papers}, {"left", "right"})
        seen = json.loads(self.seen.read_text(encoding="utf-8"))
        self.assertEqual(set(seen["ids"]), {"existing", "left", "right"})
        self.assertEqual(seen["latest_published_at"], "2026-01-02T00:00:00+00:00")

    def test_failed_second_child_does_not_publish_first_child(self):
        self.client.results.side_effect = [
            RuntimeError("window too large"), iter([_paper("left")]),
            RuntimeError("right child unavailable"),
        ]
        with self.assertRaisesRegex(RuntimeError, "right child unavailable"):
            self.run_fetch()
        self.assert_unchanged()


if __name__ == "__main__":
    unittest.main()
