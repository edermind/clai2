#!/usr/bin/env python3
"""
clai2 — терминальный AI-агент для Linux.

Использование:
    clai2 "твой вопрос"
    clai2 "что случилось с nginx @/var/log/nginx/error.log"
    clai2 "объясни этот код @main.py"
"""

import argparse
import sys

from core.config import load_config
from core.file_handler import inject_files
from core.agent import ask


def main():
    parser = argparse.ArgumentParser(
        prog="clai2",
        description="Терминальный AI-агент. Задай вопрос, используй @файл для передачи содержимого.",
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Вопрос или задача. Используйте @filename чтобы вставить содержимое файла.",
    )

    args = parser.parse_args()

    # Если промпт не передан — показать помощь
    if not args.prompt:
        parser.print_help()
        sys.exit(0)

    config = load_config()

    prompt = inject_files(args.prompt)

    try:
        response = ask(prompt, config)
    except Exception as e:
        print(f"[clai2] Ошибка при обращении к провайдеру: {e}", file=sys.stderr)
        sys.exit(1)

    print(response)


if __name__ == "__main__":
    main()
