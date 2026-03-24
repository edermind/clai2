
import sys

from core.config import load_config
from core.file_handler import inject_files
from core.agent import ask
from core.agent_loop import run_agent


def main():
    args = sys.argv[1:]

    if not args:
        print("Использование:")
        print('  clai2 "вопрос"')
        print('  clai2 "вопрос @файл"')
        print('  clai2 agent "вопрос о системе"')
        sys.exit(0)

    config = load_config()

    # Режим агента
    if args[0] == "agent":
        if len(args) < 2:
            print("Использование: clai2 agent \"вопрос\"")
            print("Примеры:")
            print('  clai2 agent "что жрёт память"')
            print('  clai2 agent "какой линукс стоит"')
            print('  clai2 agent "выведи топ процессов"')
            sys.exit(0)

        question = " ".join(args[1:])
        try:
            response = run_agent(question, config)
        except Exception as e:
            print(f"[clai2] Ошибка агента: {e}", file=sys.stderr)
            sys.exit(1)
        print(response)
        return

    # Обычный режим
    prompt = inject_files(" ".join(args))
    try:
        response = ask(prompt, config)
    except Exception as e:
        print(f"[clai2] Ошибка при обращении к провайдеру: {e}", file=sys.stderr)
        sys.exit(1)
    print(response)


if __name__ == "__main__":
    main()