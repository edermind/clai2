import anthropic

from providers.base import BaseProvider


class ClaudeProvider(BaseProvider):
    """Провайдер Anthropic Claude."""

    def __init__(self, api_key: str, model: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def chat(self, prompt: str) -> str:
        message = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        return message.content[0].text
