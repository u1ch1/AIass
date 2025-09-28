#!/usr/bin/env python3
# config/settings.py

import os

# Получаем домашнюю директорию текущего пользователя
HOME_DIR = os.path.expanduser("~")

# Основные настройки
CONFIG = {
    "workspace": f"{HOME_DIR}/ai_pentest_workspace",  # ИСПРАВЛЕНО!
    "allowed_targets": [
        "testphp.vulnweb.com",
        "demo.testfire.net", 
        "scanme.nmap.org",
        "localhost"
    ],
    "ai_model": "codellama:7b",
    "ollama_url": "http://localhost:11434/api/generate",
    "max_execution_time": 300,
    "safe_mode": True
}

# Запрещенные команды
BANNED_COMMANDS = [
    "rm -rf /", "mkfs", "dd if=", "format",
    "chmod -R 777 /", "passwd", "useradd",
    "shutdown", "reboot", "init 0"
]
