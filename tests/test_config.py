from resumetailor_agent.config import AppConfig


def test_app_config_defaults_to_rule_mode():
    config = AppConfig()

    assert config.llm_enabled is False
    assert config.mode == "rule"


def test_app_config_marks_llm_mode_when_credentials_exist():
    config = AppConfig(
        openai_api_key="test-key",
        openai_model="gpt-test",
    )

    assert config.llm_enabled is True
    assert config.mode == "llm"


def test_app_config_defaults_to_hybrid_retrieval():
    config = AppConfig()

    assert config.retrieval_mode == "hybrid"
    assert config.embedding_backend == "local"
