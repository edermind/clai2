import sys
from pathlib import Path

import yaml

CONFIG_PATH = Path.home() / ".clai2" / "config.yaml"

# Ключи, обязательные для каждого провайдера
REQUIRED_KEYS = {
    "claude":    ["api_key"],
    "openai":    ["api_key"],
    "gemini":    ["api_key"],
    "gigachat":  [],  # валидируется отдельно: нужен credentials ИЛИ api_key
    "llama":     [],  # ключ не нужен
}


def load_config() -> dict:
    """Загружает config.yaml. Завершает программу с понятной ошибкой если что-то не так."""

    if not CONFIG_PATH.exists():
        _exit(
            f"Конфиг не найден: {CONFIG_PATH}\n"
            "Создайте файл. Пример:\n\n"
            "  provider: gigachat\n"
            "  model: GigaChat\n"
            "  api_key: <ваш токен>\n"
        )

    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    provider = config.get("provider")
    if not provider:
        _exit("В конфиге не указан 'provider'.")

    if provider not in REQUIRED_KEYS:
        supported = ", ".join(REQUIRED_KEYS.keys())
        _exit(f"Неизвестный провайдер '{provider}'. Поддерживаются: {supported}")

    for key in REQUIRED_KEYS[provider]:
        if not config.get(key):
            _exit(f"Для провайдера '{provider}' в конфиге обязателен параметр '{key}'.")

    # Отдельная валидация GigaChat: нужен хотя бы один из двух ключей
    if provider == "gigachat":
        if not config.get("credentials") and not config.get("api_key"):
            _exit("Для провайдера 'gigachat' укажите 'api_key' или 'credentials' в конфиге.")

    if not config.get("model"):
        _exit("В конфиге не указана 'model'.")

    return config


def _exit(message: str):
    print(f"[clai2] Ошибка конфигурации: {message}", file=sys.stderr)
    sys.exit(1)
