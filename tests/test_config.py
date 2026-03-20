import pytest
from pathlib import Path
from unittest.mock import patch
from core.config import load_config


def make_config(tmp_path, content: str) -> Path:
    """Создаёт временный config.yaml с нужным содержимым."""
    cfg = tmp_path / "config.yaml"
    cfg.write_text(content)
    return cfg


def test_valid_gigachat_config(tmp_path):
    cfg = make_config(tmp_path, """
provider: gigachat
model: GigaChat
api_key: test_key
""")
    with patch("core.config.CONFIG_PATH", cfg):
        config = load_config()
    assert config["provider"] == "gigachat"
    assert config["model"] == "GigaChat"


def test_valid_llama_config(tmp_path):
    """Llama не требует api_key."""
    cfg = make_config(tmp_path, """
provider: llama
model: llama3.2
""")
    with patch("core.config.CONFIG_PATH", cfg):
        config = load_config()
    assert config["provider"] == "llama"


def test_missing_provider_exits(tmp_path):
    cfg = make_config(tmp_path, "model: GigaChat\napi_key: key")
    with patch("core.config.CONFIG_PATH", cfg):
        with pytest.raises(SystemExit):
            load_config()


def test_missing_api_key_exits(tmp_path):
    cfg = make_config(tmp_path, "provider: claude\nmodel: claude-sonnet-4-20250514")
    with patch("core.config.CONFIG_PATH", cfg):
        with pytest.raises(SystemExit):
            load_config()


def test_unknown_provider_exits(tmp_path):
    cfg = make_config(tmp_path, "provider: chatgpt\nmodel: gpt5\napi_key: key")
    with patch("core.config.CONFIG_PATH", cfg):
        with pytest.raises(SystemExit):
            load_config()


def test_gigachat_needs_key_or_credentials(tmp_path):
    """GigaChat без api_key и без credentials — ошибка."""
    cfg = make_config(tmp_path, "provider: gigachat\nmodel: GigaChat")
    with patch("core.config.CONFIG_PATH", cfg):
        with pytest.raises(SystemExit):
            load_config()