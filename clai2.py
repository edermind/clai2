#!/usr/bin/env python3
"""
clai2 — терминальный AI-ассистент для Linux.

Использование:
    clai2 "твой вопрос"
    clai2 "что случилось с nginx @/var/log/nginx/error.log"
    clai2 agent "выведи информацию о процессах"
    clai2 agent "что жрёт память"
    clai2 agent "какой линукс стоит"
"""

import argparse
import sys

from core.config import load_config
from core.file_handler import inject_files
from core.agent import ask
from core.agent_loop import run_agent


def main():
    parser = argparse.ArgumentParser(
        prog="clai2",
        description="Терминальный AI-ассистент для Linux.",
    )

    subparsers = parser.add_subparsers(dest="command")

    # Подкоманда: agent
    agent_parser = subparsers.add_parser(
        "agent",
        help="AI-агент с доступом к информации о системе.",
    )
    agent_parser.add_argument(
        "prompt",
        help="Вопрос агенту. Например: 'что жрёт память', 'какой линукс стоит'",
    )

    # Обычный режим — просто вопрос
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Вопрос или задача. Используйте @filename чтобы вставить содержимое файла.",
    )

    args = parser.parse_args()
    config = load_config()

    # Режим агента
    if args.command == "agent":
        if not args.prompt:
            agent_parser.print_help()
            sys.exit(0)
        try:
            response = run_agent(args.prompt, config)
        except Exception as e:
            print(f"[clai2] Ошибка агента: {e}", file=sys.stderr)
            sys.exit(1)
        print(response)
        return

    # Обычный режим
    if not args.prompt:
        parser.print_help()
        sys.exit(0)

    prompt = inject_files(args.prompt)

    try:
        response = ask(prompt, config)
    except Exception as e:
        print(f"[clai2] Ошибка при обращении к провайдеру: {e}", file=sys.stderr)
        sys.exit(1)

    print(response)


if __name__ == "__main__":
    main()
