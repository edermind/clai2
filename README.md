# clai2

Терминальный AI-агент для Linux. Задаёшь вопрос прямо из командной строки — получаешь ответ. Поддерживает несколько AI-провайдеров и умеет читать файлы через `@`-синтаксис.

```bash
clai2 "что это за процесс занимает всю память?"
clai2 "что случилось с nginx @/var/log/nginx/error.log"
clai2 "объясни этот код @main.py"
```

---

## Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/<твой_ник>/clai2.git
cd clai2
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Создать конфиг

```bash
mkdir -p ~/.clai2
cp config.example.yaml ~/.clai2/config.yaml
```

Открыть `~/.clai2/config.yaml` и вписать свои данные. Минимальный рабочий вариант для GigaChat:

```yaml
provider: gigachat
model: GigaChat
api_key: ВАШ_ТОКЕН
```

Для других провайдеров — смотри примеры в `config.example.yaml`.

### 4. Запустить

```bash
python clai2.py "привет, как дела?"
```

### 5. Опционально — сделать глобальной командой

```bash
chmod +x clai2.py
sudo ln -s $(pwd)/clai2.py /usr/local/bin/clai2
```

После этого можно запускать из любой директории:

```bash
clai2 "объясни этот конфиг @/etc/nginx/nginx.conf"
```

---

## Использование

### Простой вопрос

```bash
clai2 "чем отличается TCP от UDP?"
```

### Передача файла через @

```bash
clai2 "найди ошибки в этом логе @/var/log/syslog"
clai2 "сделай ревью кода @app.py"
clai2 "переведи этот текст на английский @письмо.txt"
```

Можно передавать несколько файлов сразу:

```bash
clai2 "сравни эти два конфига @nginx.conf @nginx.conf.bak"
```

---

## Структура проекта

```
clai2/
├── clai2.py                  # Точка входа
├── requirements.txt          # Зависимости
├── config.example.yaml       # Пример конфига
├── core/
│   ├── agent.py              # Выбор провайдера и отправка запроса
│   ├── config.py             # Загрузка и валидация конфига
│   └── file_handler.py       # Обработка @filename в промпте
└── providers/
    ├── base.py               # Абстрактный класс провайдера
    ├── claude.py             # Anthropic Claude
    ├── openai.py             # OpenAI
    ├── gemini.py             # Google Gemini
    ├── llama.py              # Ollama (локальные модели)
    └── gigachat.py           # GigaChat (Sber)
```

---

## Экскурс по файлам

### `clai2.py` — точка входа

Единственная задача — принять аргументы командной строки и запустить цепочку. Использует `argparse` для парсинга промпта. Вызывает `config.py` → `file_handler.py` → `agent.py` → печатает ответ. Никакой бизнес-логики здесь нет.

```
clai2 "вопрос @файл"
  │
  ├─ argparse         → достать строку "вопрос @файл"
  ├─ load_config()    → загрузить ~/.clai2/config.yaml
  ├─ inject_files()   → заменить @файл на его содержимое
  ├─ ask()            → отправить провайдеру, получить ответ
  └─ print(ответ)
```

---

### `core/config.py` — загрузка конфига

Читает `~/.clai2/config.yaml`. Проверяет что все обязательные поля заполнены для выбранного провайдера. Если что-то не так — завершает программу с понятной ошибкой на русском вместо Python traceback. Знает какие поля нужны каждому провайдеру (`api_key`, `credentials` и т.д.).

---

### `core/file_handler.py` — обработка @файлов

Ищет в тексте промпта паттерн `@путь_к_файлу` через регулярное выражение. Для каждого найденного пути читает файл и подставляет его содержимое прямо в текст запроса. Итоговая строка отправляется в модель как обычный текст.

```
"объясни @main.py"
→
"объясни

[main.py]
def hello():
    print('hello world')
..."
```

Если файл не найден или нет прав на чтение — завершает с ошибкой.

---

### `core/agent.py` — выбор провайдера

Смотрит на поле `provider` в конфиге и создаёт нужный объект провайдера. Передаёт ему промпт и возвращает ответ. Это единственное место где перечислены все доступные провайдеры — при добавлении нового нужно добавить одну строку в `match/case`.

---

### `providers/base.py` — контракт провайдера

Абстрактный класс с одним методом `chat(prompt: str) -> str`. Не содержит логики — только определяет интерфейс. Благодаря ему `agent.py` не знает с каким конкретно провайдером работает, что позволяет добавлять новых без изменения остального кода.

---

### `providers/gigachat.py` — GigaChat (Sber)

Использует официальную библиотеку `gigachat`. Поддерживает два способа авторизации: `api_key` (Bearer-токен) и `credentials` (Base64 clientId:secret из личного кабинета). `verify_ssl_certs=False` нужен для работы без сертификата Минцифры.

---

### `providers/claude.py` — Anthropic Claude

Использует официальную библиотеку `anthropic`. Авторизация через `api_key`. Модели: `claude-sonnet-4-20250514`, `claude-opus-4-5`, `claude-haiku-4-5-20251001`.

---

### `providers/openai.py` — OpenAI

Использует официальную библиотеку `openai`. Авторизация через `api_key`. Модели: `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`.

---

### `providers/gemini.py` — Google Gemini

Использует библиотеку `google-generativeai`. Авторизация через `api_key`. Модели: `gemini-2.0-flash`, `gemini-1.5-pro`.

---

### `providers/llama.py` — Ollama (локальные модели)

Единственный провайдер без API-ключа. Работает с локально запущенным Ollama через HTTP REST на `localhost:11434`. Поддерживает любую модель загруженную в Ollama: `llama3.2`, `mistral`, `gemma3` и другие. Хост можно переопределить в конфиге.

---

## Добавление нового провайдера

1. Создать файл `providers/newprovider.py`, унаследоваться от `BaseProvider`, реализовать метод `chat()`
2. Добавить импорт в `providers/__init__.py`
3. Добавить одну строку в `match/case` в `core/agent.py`
4. Добавить валидацию ключей в `REQUIRED_KEYS` в `core/config.py`

---

## Зависимости

| Библиотека | Для чего |
|---|---|
| `anthropic` | Claude |
| `openai` | OpenAI |
| `google-generativeai` | Gemini |
| `gigachat` | GigaChat |
| `requests` | Ollama (HTTP) |
| `pyyaml` | Чтение config.yaml |
