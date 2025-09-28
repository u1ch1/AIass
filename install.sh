#!/bin/bash
# install.sh

echo "🔄 Установка Kali AI Assistant..."

# Проверяем Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен"
    exit 1
fi

# Устанавливаем зависимости
pip3 install requests argparse

# Делаем скрипты исполняемыми
chmod +x main.py
chmod +x core/ai_engine.py
chmod +x modules/pentest_modules.py

echo "✅ Установка завершена!"
echo "🚀 Запуск: python3 main.py"
