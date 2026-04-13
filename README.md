# clai2

Терминальный AI-ассистент для Linux. Задаёшь вопрос из командной строки — получаешь ответ. Поддерживает GigaChat, Claude, OpenAI, Gemini, Ollama.

---

## Quick Start

```bash
# 1. Клонировать репозиторий
git clone https://github.com/<твой_ник>/clai2.git
cd clai2

# 2. Запустить установщик
bash install.sh

# 3. Применить alias
source ~/.bashrc

# 4. Вписать API-ключ
nano ~/.clai2/config.yaml

# 5. Готово
clai "привет"
```

---

## Фичи

### Обычный режим

Задаёшь любой вопрос — получаешь ответ от выбранного провайдера:

```bash
clai "чем отличается TCP от UDP?"
clai "напиши функцию на python которая разворачивает строку"
```

### @filehandler — передача файлов

Добавь `@путь_к_файлу` в запрос — содержимое файла автоматически вставится в промпт:

```bash
clai "что не так с nginx @/var/log/nginx/error.log"
clai "сделай ревью кода @main.py"
clai "сравни два конфига @nginx.conf @nginx.conf.bak"
```

Работает с любым текстовым файлом. Можно передавать несколько файлов сразу.

### agent — AI-агент с доступом к системе

Агент сам решает какие данные собрать, выполняет системные команды и возвращает анализ:

```bash
clai agent "что жрёт память"
clai agent "какой линукс стоит"
clai agent "выведи топ процессов по CPU"
clai agent "дай полный отчёт о системе"
```

Доступные инструменты агента:

| Инструмент | Что делает |
|---|---|
| `get_processes` | Топ процессов по загрузке CPU и памяти |
| `get_system_load` | RAM, uptime, дисковое пространство |
| `get_system_info` | Дистрибутив, версия ядра, архитектура |

Агент сам определяет нужный инструмент по смыслу вопроса — никакой привязки к конкретным фразам.

---

## Конфигурация

Конфиг находится в `~/.clai2/config.yaml`. Три строки для работы:

```yaml
provider: gigachat
model: GigaChat
api_key: ВАШ_ТОКЕН
```

Поддерживаемые провайдеры: `gigachat`, `claude`, `openai`, `gemini`, `llama`.
Подробнее — в `config.example.yaml`.

---

## Архитектура

```
clai2/
├── clai2.py              # Точка входа: разбор команд, вызов нужного режима
├── core/
│   ├── agent.py          # Выбор провайдера по конфигу, отправка запроса
│   ├── agent_loop.py     # ReAct-цикл для режима agent
│   ├── config.py         # Загрузка и валидация ~/.clai2/config.yaml
│   └── file_handler.py   # Парсинг @filename, подстановка содержимого файла
├── providers/
│   ├── base.py           # Абстрактный класс: метод chat(prompt) → str
│   ├── claude.py         # Anthropic SDK
│   ├── openai.py         # OpenAI SDK
│   ├── gemini.py         # Google GenAI SDK
│   ├── gigachat.py       # GigaChat SDK
│   └── llama.py          # Ollama HTTP REST
└── tools/
    └── system_tools.py   # Системные инструменты для агента (subprocess)
```

**Поток данных — обычный режим:**
```
clai "вопрос @файл"  →  file_handler  →  agent.py  →  provider  →  ответ
```

**Поток данных — режим agent:**
```
clai agent "вопрос"  →  agent_loop: LLM выбирает tool  →  subprocess
                     →  agent_loop: LLM анализирует результат  →  ответ
```

Добавить нового провайдера = один новый файл в `providers/` и одна строка в `core/agent.py`.
