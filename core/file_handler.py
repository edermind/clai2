import re
import sys
from pathlib import Path


# Паттерн: @filename — имя файла до пробела/конца строки
_FILE_PATTERN = re.compile(r"@(\S+)")


def inject_files(prompt: str) -> str:
    """
    Находит все вхождения @filename в промпте и заменяет их содержимым файла.

    Пример:
        "что случилось с nginx @/var/log/nginx/error.log"
        →
        "что случилось с nginx\n\n[/var/log/nginx/error.log]\n<содержимое файла>"
    """
    matches = _FILE_PATTERN.findall(prompt)

    if not matches:
        return prompt

    for filepath_str in matches:
        filepath = Path(filepath_str)

        if not filepath.exists():
            print(f"[clai2] Файл не найден: {filepath}", file=sys.stderr)
            sys.exit(1)

        if not filepath.is_file():
            print(f"[clai2] Путь не является файлом: {filepath}", file=sys.stderr)
            sys.exit(1)

        try:
            content = filepath.read_text(encoding="utf-8", errors="replace")
        except PermissionError:
            print(f"[clai2] Нет прав на чтение: {filepath}", file=sys.stderr)
            sys.exit(1)

        replacement = f"\n\n[{filepath_str}]\n{content}"
        prompt = prompt.replace(f"@{filepath_str}", replacement)

    return prompt
