import google.generativeai as genai

from providers.base import BaseProvider


class GeminiProvider(BaseProvider):
    """Провайдер Google Gemini."""

    def __init__(self, api_key: str, model: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def chat(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
