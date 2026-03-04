import requests

from providers.base import BaseProvider


class LlamaProvider(BaseProvider):
    """Провайдер Ollama — локальный LLM без API-ключа."""

    def __init__(self, model: str, host: str = "http://localhost:11434"):
        self.model = model
        self.url = f"{host}/api/chat"

    def chat(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }
        response = requests.post(self.url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["message"]["content"]
