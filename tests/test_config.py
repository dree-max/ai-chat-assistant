from config import load_config

def test_default_config_loads():
    config = load_config()

    assert config.app_title
    assert config.provider in ("ollama", "openai")
    assert config.ollama_base_url.startswith("http://") or config.ollama_base_url.startswith("https://")
    assert config.ollama_model
    assert config.openai_model
    assert "helpful ai chat assistant" in config.system_prompt.lower()