import importlib.util
from pathlib import Path
import sys
from unittest.mock import Mock

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import llm
import long_range_review
import starter_pack


@pytest.fixture
def gateway_env(monkeypatch):
    for name in (
        "LLM_PROVIDER", "LLM_API_KEY", "LLM_BASE_URL", "LLM_MODEL",
        "LLM_FILTER_MODEL", "LLM_REWRITE_MODEL", "LLM_MAX_OUTPUT_TOKENS",
        "DPR_LLM_MAX_OUTPUT_TOKENS", "DEEPSEEK_API_KEY", "DEEPSEEK_BASE_URL",
        "DEEPSEEK_MODEL", "DEEPSEEK_FILTER_MODEL", "DEEPSEEK_REWRITE_MODEL",
        "SUMMARY_API_KEY", "SUMMARY_BASE_URL", "SUMMARY_MODEL",
    ):
        monkeypatch.delenv(name, raising=False)
    settings = {
        "LLM_PROVIDER": "openai-compatible",
        "LLM_API_KEY": "test-only",
        "LLM_BASE_URL": "https://gateway.example/v1",
        "LLM_MODEL": "vendor/summary-model",
        "LLM_FILTER_MODEL": "vendor/filter-model",
        "LLM_REWRITE_MODEL": "vendor/rewrite-model",
    }
    for name, value in settings.items():
        monkeypatch.setenv(name, value)
    return settings


def load_script(filename):
    spec = importlib.util.spec_from_file_location(
        "consumer_" + filename.replace(".", "_"), ROOT / "src" / filename
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module




def test_enrichment_without_credentials_fails_before_reading_subscription_data(
    gateway_env, monkeypatch, tmp_path
):
    monkeypatch.delenv("LLM_API_KEY")
    module = load_script("0.enrich_config_queries.py")
    config = tmp_path / "config.yaml"
    config.write_text("subscriptions: {}\n", encoding="utf-8")
    monkeypatch.setattr(module, "CONFIG_FILE", str(config))
    monkeypatch.setattr(sys, "argv", ["0.enrich_config_queries.py"])
    with pytest.raises(RuntimeError):
        module.main()


def test_reading_generation_without_credentials_keeps_content_skip_behavior(
    gateway_env, monkeypatch
):
    monkeypatch.delenv("LLM_API_KEY")
    module = load_script("6.generate_docs.py")
    assert module.translate_title_and_abstract_to_zh("Synthetic title", "Synthetic abstract") == ("", "")




def test_starter_review_cache_tracks_actual_gateway_model_and_endpoint(
    gateway_env, monkeypatch, tmp_path
):
    client = Mock(kwargs={})
    client.chat_structured.return_value = {
        "parsed": {"papers": [{
            "id": "p0", "score": 8, "scope_match": True,
            "evidence": "asymmetric traveling salesman", "reason": "test",
        }]}
    }
    create = Mock(return_value=client)
    monkeypatch.setattr(llm.ClientFactory, "create", create)
    papers = [{"id": "p1", "title": "ATSP", "abstract": "asymmetric traveling salesman"}]
    topic = {"tag": "ATSP"}
    first = starter_pack.review_candidates(papers, topic, tmp_path, 1)
    assert first["new_reviews"] == 1
    again = starter_pack.review_candidates(papers, topic, tmp_path, 1)
    assert again["cached_reviews"] == 1 and create.call_count == 1
    monkeypatch.setenv("LLM_FILTER_MODEL", "vendor/second-filter")
    assert starter_pack.review_candidates(papers, topic, tmp_path, 1)["new_reviews"] == 1
    monkeypatch.setenv("LLM_BASE_URL", "https://other.example/v1")
    assert starter_pack.review_candidates(papers, topic, tmp_path, 1)["new_reviews"] == 1
    assert create.call_count == 3


