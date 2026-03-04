from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

from providers.base import BaseProvider


class GigaChatProvider(BaseProvider):
    """
    Провайдер GigaChat. Поддерживает два способа авторизации:
      - credentials: Base64(clientId:secret) — из личного кабинета Sber
      - api_key:     Bearer-токен            — если получен напрямую
    """

    def __init__(self, model: str, credentials: str = None, api_key: str = None):
        if not credentials and not api_key:
            raise ValueError("GigaChat: укажите 'credentials' или 'api_key' в конфиге.")
        self.model = model
        self.credentials = credentials
        self.api_key = api_key

    def chat(self, prompt: str) -> str:
        # Собираем kwargs в зависимости от того, что передано
        auth = (
            {"credentials": self.credentials}
            if self.credentials
            else {"access_token": self.api_key}
        )

        with GigaChat(**auth, verify_ssl_certs=False) as giga:
            response = giga.chat(
                Chat(
                    model=self.model,
                    messages=[
                        Messages(role=MessagesRole.USER, content=prompt)
                    ],
                )
            )
        return response.choices[0].message.content
