import importlib.util
import os
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch


def _load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


class LocalDebugEnvTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = pathlib.Path(__file__).resolve().parents[1]
        sys.path.insert(0, str(root / "src"))
        cls.mod = _load_module("local_debug_server_mod", root / "src" / "local_debug_server.py")

    def test_saved_gateway_selection_replaces_stale_provider_and_preserves_roles(self):
        from llm import ClientFactory

        env = self.mod.build_secret_env({
            "llmProvider": {
                "type": "openai-compatible",
                "filterModel": "filter-model",
                "rewriteModel": "rewrite-model",
            },
            "summarizedLLM": {
                "apiKey": "gateway-key",
                "baseUrl": "http://gateway.example:8080/v1",
                "model": "summary-model",
            },
        })
        with patch.dict(os.environ, {
            "LLM_PROVIDER": "deepseek",
            "LLM_API_KEY": "stale-key",
            "DEEPSEEK_API_KEY": "stale-native-key",
            **env,
        }, clear=True):
            for purpose, model in (("summary", "summary-model"), ("filter", "filter-model"), ("rewrite", "rewrite-model")):
                with self.subTest(purpose=purpose):
                    client = ClientFactory.from_env(purpose)
                    self.assertEqual(
                        (client.provider, client.api_key, client.model, client.base_url),
                        ("openai-compatible", "gateway-key", model, "http://gateway.example:8080/v1"),
                    )

    def test_older_secret_clears_stale_explicit_provider_and_infers_native_service(self):
        from llm import ClientFactory

        env = self.mod.build_secret_env({
            "summarizedLLM": {
                "apiKey": "native-key", "baseUrl": "https://api.deepseek.com", "model": "deepseek-v4-flash",
            },
        })
        with patch.dict(os.environ, {"LLM_PROVIDER": "openai-compatible", **env}, clear=True):
            self.assertEqual(ClientFactory.from_env().provider, "deepseek")

    def test_update_env_file_replaces_old_keys_preserves_comments_and_clears_stale_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / ".env"
            path.write_text(
                "# local debug\n"
                "DEEPSEEK_API_KEY=old\n"
                "PUBLIC_RERANK_API_KEY=old-rerank\n"
                "UNCHANGED=value\n",
                encoding="utf-8",
            )

            self.mod.update_env_file(
                path,
                {
                    "DEEPSEEK_API_KEY": "sk-new",
                    "SUMMARY_API_KEY": "sk-new",
                    "DEEPSEEK_BASE_URL": "https://api.deepseek.com",
                    "PUBLIC_RERANK_API_KEY": "",
                },
            )
            text = path.read_text(encoding="utf-8")

            self.assertIn("# local debug", text)
            self.assertIn("UNCHANGED=value", text)
            self.assertIn("DEEPSEEK_API_KEY=sk-new", text)
            self.assertIn("SUMMARY_API_KEY=sk-new", text)
            self.assertIn("DEEPSEEK_BASE_URL=https://api.deepseek.com", text)
            self.assertIn("PUBLIC_RERANK_API_KEY=", text)
            self.assertNotIn("DEEPSEEK_API_KEY=old", text)
            self.assertNotIn("PUBLIC_RERANK_API_KEY=old-rerank", text)



if __name__ == "__main__":
    unittest.main()
