import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import requests


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from llm import ClientFactory, LLMClient


class LlmStructuredOutputTest(unittest.TestCase):

    def _mock_success_response(self, message: dict):
        resp = MagicMock()
        resp.raise_for_status.return_value = None
        resp.json.return_value = {
            "choices": [
                {
                    "message": message,
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 1,
                "completion_tokens": 1,
                "total_tokens": 2,
            },
        }
        return resp

    def _mock_http_error_response(self, text: str, status_code: int = 400):
        resp = MagicMock()
        resp.status_code = status_code
        resp.text = text
        resp.raise_for_status.side_effect = requests.exceptions.HTTPError(
            f"HTTP {status_code}",
            response=resp,
        )
        return resp

    @patch.dict("llm.os.environ", {}, clear=False)
    @patch("llm.requests.post")
    def test_chat_allows_deepseek_v4_large_output_window_by_default(self, mock_post):
        mock_post.return_value = self._mock_success_response({"content": "ok"})
        client = LLMClient(
            api_key="test-key",
            model="deepseek-v4-flash",
            base_url="https://api.deepseek.com",
        )
        client.kwargs["max_tokens"] = 500000

        client.chat(messages=[{"role": "user", "content": "hello"}])

        self.assertEqual(mock_post.call_args.kwargs["json"]["max_tokens"], 393216)

    @patch.dict("llm.os.environ", {"DPR_LLM_MAX_OUTPUT_TOKENS": "8192"}, clear=False)
    @patch("llm.requests.post")
    def test_chat_max_output_window_can_be_overridden_by_env(self, mock_post):
        mock_post.return_value = self._mock_success_response({"content": "ok"})
        client = LLMClient(
            api_key="test-key",
            model="deepseek-v4-flash",
            base_url="https://api.deepseek.com",
        )
        client.kwargs["max_tokens"] = 500000

        client.chat(messages=[{"role": "user", "content": "hello"}])

        self.assertEqual(mock_post.call_args.kwargs["json"]["max_tokens"], 8192)

    @patch("llm.requests.post")
    def test_chat_structured_prefers_json_object_for_deepseek(self, mock_post):
        mock_post.return_value = self._mock_success_response({"content": '{"answer":"ok"}'})
        client = LLMClient(
            api_key="test-key",
            model="deepseek-v4-flash",
            base_url="https://api.deepseek.com",
        )

        result = client.chat_structured(
            messages=[{"role": "user", "content": "hello"}],
            schema_name="answer_payload",
            schema={
                "type": "object",
                "properties": {"answer": {"type": "string"}},
                "required": ["answer"],
                "additionalProperties": False,
            },
        )

        self.assertEqual(result["response_format_used"], "json_object")
        self.assertEqual(result["parsed"], {"answer": "ok"})
        self.assertEqual(
            [call.kwargs["json"]["response_format"]["type"] for call in mock_post.call_args_list],
            ["json_object"],
        )

    @patch("llm.requests.post")
    def test_chat_structured_falls_back_to_prompt_only_when_json_object_unsupported(self, mock_post):
        mock_post.side_effect = [
            self._mock_http_error_response(
                '{"error":{"message":"response_format json_object is not supported"}}'
            ),
            self._mock_success_response({"content": '{"answer":"ok"}'}),
        ]
        client = LLMClient(
            api_key="test-key",
            model="deepseek-v4-flash",
            base_url="https://api.deepseek.com",
        )

        result = client.chat_structured(
            messages=[{"role": "user", "content": "hello"}],
            schema_name="answer_payload",
            schema={
                "type": "object",
                "properties": {"answer": {"type": "string"}},
                "required": ["answer"],
                "additionalProperties": False,
            },
        )

        self.assertEqual(result["response_format_used"], "prompt_only")
        self.assertEqual(
            [call.kwargs["json"].get("response_format", {}).get("type") for call in mock_post.call_args_list],
            ["json_object", None],
        )

    @patch("llm.requests.post")
    def test_chat_structured_validates_schema_locally_and_falls_back(self, mock_post):
        mock_post.side_effect = [
            self._mock_success_response({"content": '{"answer":"ok","extra":1}'}),
            self._mock_success_response({"content": '{"answer":"ok"}'}),
        ]
        client = LLMClient(
            api_key="test-key",
            model="deepseek-v4-flash",
            base_url="https://api.deepseek.com",
        )

        result = client.chat_structured(
            messages=[{"role": "user", "content": "return JSON"}],
            schema_name="answer_payload",
            schema={
                "type": "object",
                "properties": {"answer": {"type": "string"}},
                "required": ["answer"],
                "additionalProperties": False,
            },
        )

        self.assertEqual(result["response_format_used"], "prompt_only")
        self.assertEqual(result["parsed"], {"answer": "ok"})

    @patch("llm.requests.post")
    def test_chat_structured_returns_refusal(self, mock_post):
        mock_post.return_value = self._mock_success_response(
            {"refusal": "I'm sorry, I cannot assist with that request."}
        )
        client = LLMClient(
            api_key="test-key",
            model="deepseek-v4-flash",
            base_url="https://api.deepseek.com",
        )

        result = client.chat_structured(
            messages=[{"role": "user", "content": "hello"}],
            schema_name="answer_payload",
            schema={
                "type": "object",
                "properties": {"answer": {"type": "string"}},
                "required": ["answer"],
                "additionalProperties": False,
            },
        )

        self.assertEqual(
            result["refusal"],
            "I'm sorry, I cannot assist with that request.",
        )
        self.assertIsNone(result["parsed"])
        self.assertIsNone(result["parse_error"])

    @patch.dict("llm.os.environ", {"LLM_MAX_OUTPUT_TOKENS": "8192"}, clear=True)
    @patch("llm.requests.post")
    def test_explicit_gateway_handles_native_named_model_without_provider_specific_parameters(self, mock_post):
        def strict_gateway(*args, **kwargs):
            payload = kwargs["json"]
            if "thinking" in payload or payload.get("max_tokens", 0) > 8192:
                return self._mock_http_error_response('{"error":{"message":"invalid request parameters"}}')
            return self._mock_success_response({"content": '{"answer":"accepted"}'})

        mock_post.side_effect = strict_gateway
        client = ClientFactory.create("test-key", "deepseek-v4-flash", "https://gateway.example/v1", "openai-compatible")
        client.kwargs.update(thinking={"type": "disabled"}, max_tokens=500000)
        result = client.chat_structured(
            [{"role": "user", "content": "Return JSON with the answer."}],
            "gateway_answer",
            {"type": "object", "properties": {"answer": {"type": "string"}}, "required": ["answer"], "additionalProperties": False},
        )
        self.assertEqual(result["parsed"], {"answer": "accepted"})
        self.assertIsNone(result["parse_error"])

    @patch.dict("llm.os.environ", {}, clear=True)
    @patch("llm.requests.post")
    def test_gateway_falls_back_to_json_object_when_schema_is_rejected(self, mock_post):
        mock_post.side_effect = [
            self._mock_http_error_response('{"error":{"message":"response_format json_schema is not supported"}}'),
            self._mock_success_response({"content": '{"answer":"compatible"}'}),
        ]
        client = ClientFactory.create("test-key", "text-model", "https://gateway.example/v1")
        result = client.chat_structured(
            [{"role": "user", "content": "Return JSON with the answer."}],
            "gateway_answer",
            {"type": "object", "properties": {"answer": {"type": "string"}}, "required": ["answer"], "additionalProperties": False},
        )
        self.assertEqual(result["parsed"], {"answer": "compatible"})
        self.assertEqual(result["response_format_used"], "json_object")


if __name__ == "__main__":
    unittest.main()
