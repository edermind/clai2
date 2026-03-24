import subprocess

TOOLS = {
    "get_processes": {
        "description": "Список запущенных процессов, топ по загрузке CPU и памяти",
        "command": "ps aux --sort=-%cpu | head -20",
    },
    "get_system_load": {
        "description": "Загрузка системы: CPU, оперативная память, uptime, дисковое пространство",
        "command": "echo '=== UPTIME ===' && uptime && echo '=== MEMORY ===' && free -h && echo '=== DISK ===' && df -h /",
    },
    "get_system_info": {
        "description": "Информация об операционной системе: дистрибутив, версия ядра, архитектура",
        "command": "echo '=== UNAME ===' && uname -a && echo '=== OS RELEASE ===' && cat /etc/os-release",
    },
}


def run_tool(name: str) -> str:
    """Выполняет команду инструмента и возвращает вывод."""
    if name not in TOOLS:
        return f"Неизвестный инструмент: {name}"

    command = TOOLS[name]["command"]
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
    )
    output = result.stdout
    if result.stderr:
        output += f"\n[stderr]: {result.stderr}"
    return output


def tools_description() -> str:
    """Возвращает описание всех инструментов для передачи в LLM."""
    lines = []
    for name, tool in TOOLS.items():
        lines.append(f"- {name}: {tool['description']}")
    return "\n".join(lines)
