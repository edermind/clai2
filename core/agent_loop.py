import json
import sys

from core.agent import ask
from tools.system_tools import TOOLS, run_tool, tools_description


# Системный промпт — объясняет модели как себя вести
SYSTEM_PROMPT = """Ты — системный ассистент для Linux. У тебя есть инструменты для получения информации о системе.

Доступные инструменты:
{tools}

Когда пользователь задаёт вопрос:
1. Реши какие инструменты нужно вызвать (можно несколько)
2. Ответь ТОЛЬКО валидным JSON без лишнего текста в формате:
{{"tools": ["tool_name1", "tool_name2"]}}

Если вопрос не требует инструментов или ты не можешь помочь:
{{"tools": []}}

Отвечай только JSON. Никакого текста до или после.
"""

# Промпт для финального ответа после получения данных от инструментов
ANSWER_PROMPT = """Ты — системный ассистент для Linux. Пользователь задал вопрос и ты собрал данные с системы.

Вопрос пользователя: {question}

Данные с системы:
{data}

Проанализируй данные и дай чёткий понятный ответ на вопрос пользователя на русском языке.
"""


def run_agent(question: str, config: dict) -> str:
    """
    ReAct-цикл:
    1. LLM решает какие инструменты вызвать
    2. Инструменты выполняются
    3. LLM анализирует результат и отвечает
    """

    # Шаг 1 — спросить LLM какие инструменты нужны
    tool_selection_prompt = SYSTEM_PROMPT.format(tools=tools_description())
    tool_selection_prompt += f"\n\nВопрос пользователя: {question}"

    raw_response = ask(tool_selection_prompt, config)

    # Шаг 2 — распарсить JSON с названиями инструментов
    try:
        # Чистим ответ от возможных markdown-блоков ```json ... ```
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
        parsed = json.loads(cleaned.strip())
        selected_tools = parsed.get("tools", [])
    except (json.JSONDecodeError, KeyError):
        # Если LLM не вернул валидный JSON — отвечаем напрямую без инструментов
        return ask(question, config)

    # Если инструменты не нужны — просто отвечаем напрямую
    if not selected_tools:
        return ask(question, config)

    # Шаг 3 — выполнить инструменты и собрать данные
    collected_data = []
    for tool_name in selected_tools:
        if tool_name not in TOOLS:
            continue
        print(f"[agent] вызываю: {tool_name}...", file=sys.stderr)
        output = run_tool(tool_name)
        collected_data.append(f"[{tool_name}]\n{output}")

    if not collected_data:
        return ask(question, config)

    # Шаг 4 — отправить данные в LLM для финального анализа
    answer_prompt = ANSWER_PROMPT.format(
        question=question,
        data="\n\n".join(collected_data),
    )

    return ask(answer_prompt, config)
