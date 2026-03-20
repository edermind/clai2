from unittest.mock import patch, MagicMock
from core.agent import build_provider
from providers.claude import ClaudeProvider
from providers.openai import OpenAIProvider
from providers.gemini import GeminiProvider
from providers.llama import LlamaProvider
from providers.gigachat import GigaChatProvider


def test_build_claude():
    config = {"provider": "claude", "model": "claude-sonnet-4-20250514", "api_key": "key"}
    with patch("core.agent.ClaudeProvider") as mock:
        build_provider(config)
        mock.assert_called_once_with(api_key="key", model="claude-sonnet-4-20250514")


def test_build_openai():
    config = {"provider": "openai", "model": "gpt-4o", "api_key": "key"}
    with patch("core.agent.OpenAIProvider") as mock:
        build_provider(config)
        mock.assert_called_once_with(api_key="key", model="gpt-4o")


def test_build_llama():
    config = {"provider": "llama", "model": "llama3.2"}
    with patch("core.agent.LlamaProvider") as mock:
        build_provider(config)
        mock.assert_called_once_with(model="llama3.2", host="http://localhost:11434")


def test_build_gigachat_with_api_key():
    config = {"provider": "gigachat", "model": "GigaChat", "api_key": "key"}
    with patch("core.agent.GigaChatProvider") as mock:
        build_provider(config)
        mock.assert_called_once_with(credentials=None, api_key="key", model="GigaChat")


def test_build_gigachat_with_credentials():
    config = {"provider": "gigachat", "model": "GigaChat", "credentials": "creds"}
    with patch("core.agent.GigaChatProvider") as mock:
        build_provider(config)
        mock.assert_called_once_with(credentials="creds", api_key=None, model="GigaChat")


def test_unknown_provider_raises():
    config = {"provider": "unknown", "model": "x"}
    try:
        build_provider(config)
        assert False, "должен был выбросить ValueError"
    except ValueError:
        pass