from providers.claude import ClaudeProvider
from providers.openai import OpenAIProvider
from providers.gemini import GeminiProvider
from providers.llama import LlamaProvider
from providers.gigachat import GigaChatProvider
from providers.base import BaseProvider


def build_provider(config: dict) -> BaseProvider:
    """Создаёт нужный провайдер на основе конфига."""

    provider_name = config["provider"]
    model = config["model"]

    match provider_name:
        case "claude":
            return ClaudeProvider(api_key=config["api_key"], model=model)

        case "openai":
            return OpenAIProvider(api_key=config["api_key"], model=model)

        case "gemini":
            return GeminiProvider(api_key=config["api_key"], model=model)

        case "llama":
            host = config.get("host", "http://localhost:11434")
            return LlamaProvider(model=model, host=host)

        case "gigachat":
            return GigaChatProvider(
                credentials=config.get("credentials"),
                api_key=config.get("api_key"),
                model=model
            )
        # case "gigachat":
        #     return GigaChatProvider(credentials=config["credentials"], model=model)

        case _:
            raise ValueError(f"Неизвестный провайдер: {provider_name}")


def ask(prompt: str, config: dict) -> str:
    """Главная функция агента: принять промпт → вернуть ответ."""
    provider = build_provider(config)
    return provider.chat(prompt)
