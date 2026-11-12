import json
import pathlib
import tempfile
import unittest


# Use the package path so maintain/arxiv.py cannot shadow the third-party SDK.
from src.maintain import common


class MaintainCommonTest(unittest.TestCase):
    def test_count_raw_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "rows.json"
            path.write_text(json.dumps([{"id": "a"}, {"id": "b"}]), encoding="utf-8")
            self.assertEqual(common.count_raw_rows(str(path)), 2)


if __name__ == "__main__":
    unittest.main()
