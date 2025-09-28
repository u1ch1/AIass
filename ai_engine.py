#!/usr/bin/env python3
# core/ai_engine.py

import requests
import json
import subprocess
import os
import time
from config.settings import CONFIG, BANNED_COMMANDS

class KaliAIEngine:
    def __init__(self):
        self.ollama_url = CONFIG["ollama_url"]
        self.model = CONFIG["ai_model"]
        self.workspace = CONFIG["workspace"]
        
        # Создаем рабочую директорию
        os.makedirs(self.workspace, exist_ok=True)
        os.chdir(self.workspace)
    
    def ask_ai(self, prompt):
        """Общение с локальной AI моделью"""
        payload = {
            "model": self.model,
            "prompt": f"""Ты эксперт по кибербезопасности Kali Linux. 
            Сгенерируй команды для: {prompt}
            Верни только команды, без пояснений.""",
            "stream": False
        }
        
        try:
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            return response.json()["response"]
        except Exception as e:
            return f"nmap -sV {prompt}\nnikto -h {prompt}"
    
    def is_command_safe(self, command):
        """Проверка безопасности команды"""
        command_lower = command.lower()
        return not any(banned in command_lower for banned in BANNED_COMMANDS)
    
    def execute_command(self, command):
        """Безопасное выполнение команды"""
        if not self.is_command_safe(command):
            return "❌ Команда заблокирована по соображениям безопасности"
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=CONFIG["max_execution_time"]
            )
            return {
                "command": command,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return "❌ Команда превысила время выполнения"
        except Exception as e:
            return f"❌ Ошибка: {str(e)}"
