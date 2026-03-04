from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Контракт для всех провайдеров. Каждый провайдер обязан реализовать метод chat()."""

    @abstractmethod
    def chat(self, prompt: str) -> str:
        """Отправить промпт, получить текстовый ответ."""
        ...
