import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from llm import ClientFactory, LLMClient, resolve_llm_config


class LlmBaseUrlTest(unittest.TestCase):
    def _mock_response(self):
        resp = MagicMock()
        resp.raise_for_status.return_value = None
        resp.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "ok",
                    }
                }
            ],
            "usage": {
                "prompt_tokens": 1,
                "completion_tokens": 1,
                "total_tokens": 2,
            },
        }
        return resp

    @patch("llm.requests.post")
    def test_chat_auth_error_fails_without_retrying_other_bases(self, mock_post):
        resp = MagicMock()
        resp.status_code = 401
        resp.json.return_value = {
            "error": {
                "message": "Authentication Fails, Your api key is invalid",
                "type": "authentication_error",
            }
        }
        err = Exception("401 Client Error: Authorization Required")
        err.response = resp
        resp.raise_for_status.side_effect = err
        mock_post.return_value = resp

        client = LLMClient(
            api_key="bad-key",
            model="deepseek-v4-flash",
            base_url="https://api.deepseek.com,https://fallback.invalid",
        )

        with self.assertRaises(Exception):
            client.chat([{"role": "user", "content": "hello"}])

        self.assertEqual(mock_post.call_count, 1)

    @patch("llm.requests.post")
    def test_chat_appends_v1_when_base_is_root(self, mock_post):
        mock_post.return_value = self._mock_response()
        client = LLMClient(
            api_key="test-key",
            model="gpt-4.1-mini",
            base_url="https://api.openai.com",
        )

        client.chat([{"role": "user", "content": "hello"}])

        self.assertEqual(
            mock_post.call_args.args[0],
            "https://api.openai.com/v1/chat/completions",
        )

    @patch("llm.requests.post")
    def test_chat_keeps_versioned_base(self, mock_post):
        mock_post.return_value = self._mock_response()
        client = LLMClient(
            api_key="test-key",
            model="gpt-4.1-mini",
            base_url="https://api.openai.com/v1",
        )

        client.chat([{"role": "user", "content": "hello"}])

        self.assertEqual(
            mock_post.call_args.args[0],
            "https://api.openai.com/v1/chat/completions",
        )

    @patch("llm.requests.post")
    def test_chat_uses_full_endpoint_directly(self, mock_post):
        mock_post.return_value = self._mock_response()
        client = LLMClient(
            api_key="test-key",
            model="gpt-4.1-mini",
            base_url="https://api.openai.com/v1/chat/completions",
        )

        client.chat([{"role": "user", "content": "hello"}])

        self.assertEqual(
            mock_post.call_args.args[0],
            "https://api.openai.com/v1/chat/completions",
        )


class LlmConfigurationTest(unittest.TestCase):
    @patch.dict("llm.os.environ", {
        "LLM_PROVIDER": "openai-compatible",
        "LLM_API_KEY": "gateway-key",
        "LLM_BASE_URL": "https://gateway.example/v1",
        "LLM_MODEL": "vendor/text-model",
        "DEEPSEEK_API_KEY": "stale-key",
        "DEEPSEEK_BASE_URL": "https://api.deepseek.com",
        "DEEPSEEK_MODEL": "deepseek-v4-flash",
    }, clear=True)
    def test_explicit_gateway_preserves_raw_model_path_and_overrides_legacy_credentials(self):
        client = ClientFactory.from_env()
        self.assertEqual(
            (client.provider, client.api_key, client.base_url, client.model),
            ("openai-compatible", "gateway-key", "https://gateway.example/v1", "vendor/text-model"),
        )

    @patch.dict("llm.os.environ", {
        "LLM_MODEL": "openai-compatible/vendor/text-model",
        "LLM_API_KEY": "gateway-key",
        "LLM_BASE_URL": "https://gateway.example/v1",
    }, clear=True)
    def test_qualified_provider_does_not_strip_upstream_model_path(self):
        self.assertEqual(ClientFactory.from_env().model, "vendor/text-model")

    @patch.dict("llm.os.environ", {
        "LLM_PROVIDER": "openai-compatible",
        "LLM_MODEL": "summary-model",
        "LLM_FILTER_MODEL": "filter-model",
        "LLM_REWRITE_MODEL": "rewrite-model",
        "LLM_API_KEY": "gateway-key",
        "LLM_BASE_URL": "https://gateway.example/v1",
        "DEEPSEEK_FILTER_MODEL": "stale-filter",
        "DEEPSEEK_REWRITE_MODEL": "stale-rewrite",
    }, clear=True)
    def test_roles_share_gateway_credentials_without_losing_model_choices(self):
        for purpose, model in (("summary", "summary-model"), ("filter", "filter-model"), ("rewrite", "rewrite-model")):
            with self.subTest(purpose=purpose):
                settings = resolve_llm_config(purpose)
                self.assertEqual(settings["model"], model)
                self.assertEqual(settings["api_key"], "gateway-key")
                self.assertEqual(settings["base_url"], "https://gateway.example/v1")

    @patch.dict("llm.os.environ", {
        "DEEPSEEK_API_KEY": "native-key",
        "DEEPSEEK_MODEL": "deepseek-v4-flash",
        "SUMMARY_API_KEY": "summary-key",
        "SUMMARY_BASE_URL": "https://summary.example/v1",
    }, clear=True)
    def test_native_and_summary_credentials_remain_role_specific(self):
        self.assertEqual(ClientFactory.from_env("filter").api_key, "native-key")
        summary = ClientFactory.from_env("summary")
        self.assertEqual((summary.api_key, summary.base_url), ("summary-key", "https://summary.example/v1"))

    @patch.dict("llm.os.environ", {"LLM_MODEL": "openai-compatible/"}, clear=True)
    def test_empty_qualified_model_is_rejected(self):
        with self.assertRaises(ValueError):
            ClientFactory.from_env()

    @patch.dict("llm.os.environ", {"LLM_PROVIDER": "unsupported"}, clear=True)
    def test_unknown_explicit_provider_is_rejected(self):
        with self.assertRaises(ValueError):
            ClientFactory.from_env()


if __name__ == "__main__":
    unittest.main()
