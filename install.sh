#!/bin/bash

set -e

CLAI2_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$HOME/.clai2"
CONFIG_FILE="$CONFIG_DIR/config.yaml"
BASHRC="$HOME/.bashrc"

echo "=== clai2 installer ==="
echo ""

# 1. Создать ~/.clai2/config.yaml
if [ -f "$CONFIG_FILE" ]; then
    echo "[✓] Конфиг уже существует: $CONFIG_FILE"
else
    mkdir -p "$CONFIG_DIR"
    cat > "$CONFIG_FILE" << 'YAML'
# clai2 config
# Документация по полям: см. config.example.yaml в папке проекта

provider: gigachat
model: GigaChat
api_key: ВАШ_ТОКЕН

# provider: claude
# model: claude-sonnet-4-20250514
# api_key: sk-ant-...

# provider: openai
# model: gpt-4o
# api_key: sk-...

# provider: gemini
# model: gemini-2.0-flash
# api_key: AIza...

# provider: llama
# model: llama3.2
# host: http://localhost:11434
YAML
    echo "[✓] Создан конфиг: $CONFIG_FILE"
    echo "    Не забудьте вписать ваш API-ключ в $CONFIG_FILE"
fi

# 2. Добавить alias в .bashrc
ALIAS_LINE="alias clai='python3 $CLAI2_DIR/clai2.py'"

if grep -q "alias clai=" "$BASHRC" 2>/dev/null; then
    echo "[✓] Alias 'clai' уже существует в $BASHRC"
else
    echo "" >> "$BASHRC"
    echo "# clai2 alias" >> "$BASHRC"
    echo "$ALIAS_LINE" >> "$BASHRC"
    echo "[✓] Alias добавлен в $BASHRC"
fi

# 3. Установить зависимости
echo ""
echo "[~] Устанавливаю зависимости..."
pip install -r "$CLAI2_DIR/requirements.txt" -q
echo "[✓] Зависимости установлены"

echo ""
echo "=== Готово ==="
echo ""
echo "Применить alias без перезапуска терминала:"
echo "  source ~/.bashrc"
echo ""
echo "Проверить установку:"
echo "  clai \"привет\""
echo "  clai agent \"какой линукс стоит\""
echo ""
echo "Не забудьте вписать API-ключ в $CONFIG_FILE"
