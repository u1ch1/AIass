#!/usr/bin/env python3
# main.py

import os
import sys
import argparse
from modules.pentest_modules import PentestModules

class KaliAIAssistant:
    def __init__(self):
        self.modules = PentestModules()
        self.banner = """
        🚀 Kali AI Assistant v1.0
        🤖 Автоматизация пентеста с искусственным интеллектом
        """
    
    def print_menu(self):
        print(self.banner)
        print("Доступные команды:")
        print("1.  create-project <name>    - Создать новый проект")
        print("2.  scan <target>           - Автоматическое сканирование")
        print("3.  web-scan <url>          - Сканирование веб-приложения")
        print("4.  network-scan <ip>       - Сканирование сети")
        print("5.  interactive             - Интерактивный режим")
        print("6.  help                    - Показать справку")
        print("7.  exit                    - Выход")
    
    def interactive_mode(self):
        """Интерактивный режим"""
        print("🔍 Интерактивный режим запущен!")
        print("Введите команды или 'back' для возврата")
        
        while True:
            try:
                user_input = input("\nAI> ").strip()
                
                if user_input in ['exit', 'quit', 'back']:
                    break
                elif user_input.startswith('scan '):
                    target = user_input[5:]
                    self.modules.automated_scan(target)
                elif user_input.startswith('create-project '):
                    name = user_input[15:]
                    self.modules.create_project(name)
                elif user_input == 'help':
                    self.print_menu()
                else:
                    print("Используйте: scan <target> или create-project <name>")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Ошибка: {e}")

def main():
    assistant = KaliAIAssistant()
    
    if len(sys.argv) == 1:
        assistant.interactive_mode()
        return
    
    parser = argparse.ArgumentParser(description="Kali AI Assistant")
    parser.add_argument('command', help='Команда для выполнения')
    parser.add_argument('target', nargs='?', help='Цель для сканирования')
    
    args = parser.parse_args()
    
    if args.command == "create-project" and args.target:
        assistant.modules.create_project(args.target)
    elif args.command == "scan" and args.target:
        assistant.modules.automated_scan(args.target)
    elif args.command == "interactive":
        assistant.interactive_mode()
    else:
        assistant.print_menu()

if __name__ == "__main__":
    main()
