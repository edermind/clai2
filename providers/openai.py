from openai import OpenAI

from providers.base import BaseProvider


class OpenAIProvider(BaseProvider):
    """Провайдер OpenAI."""

    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content
