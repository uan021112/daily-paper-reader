import importlib.util
import pathlib
import sys
import unittest
from unittest.mock import patch


def _load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    with patch.object(sys, "path", [str(path.parent), str(path.parent.parent), *sys.path]):
        spec.loader.exec_module(mod)
    return mod


class InitSupabaseFromMedRxivTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = pathlib.Path(__file__).resolve().parents[1]
        src_dir = root / "src"
        cls.mod = _load_module(
            "init_medrxiv_supabase_mod",
            src_dir / "maintain" / "init_medrxiv.py",
        )

    def test_resolve_date_token_long_range(self):
        token = self.mod.resolve_date_token("", 30)
        self.assertRegex(token, r"^\d{8}-\d{8}$")

    def test_resolve_date_token_manual(self):
        token = self.mod.resolve_date_token("20260301-20260310", 30)
        self.assertEqual(token, "20260301-20260310")



if __name__ == "__main__":
    unittest.main()
