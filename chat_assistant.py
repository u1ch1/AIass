#!/usr/bin/env python3
import os
import sys
import requests
import subprocess
import time
import readline
from datetime import datetime

class KaliChatAssistant:
    def __init__(self):
        self.workspace = f"{os.path.expanduser('~')}/kali_chat_workspace"
        os.makedirs(self.workspace, exist_ok=True)
        os.chdir(self.workspace)
        
        self.chat_history = []
        self.setup_ollama()
        
        print("🔧 Настраиваю русский язык для AI...")
        
    def setup_ollama(self):
        """Проверяем и настраиваем Ollama"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Ollama подключен")
            else:
                print("❌ Ollama не отвечает. Запустите: ollama serve")
        except:
            print("⚠️  Ollama не запущен. Команды будут базовыми.")
    
    def ask_ai_russian(self, message):
        """Общаемся с AI на русском"""
        prompt = f"""
        Ты русскоязычный ассистент по кибербезопасности Kali Linux. 
        Отвечай на русском понятно и подробно.
        
        Правила:
        - Объясняй команды перед выполнением
        - Предлагай варианты действий
        - Спрашивай уточнения если нужно
        - Будь дружелюбным и helpful
        
        История чата:
        {self.chat_history[-5:] if self.chat_history else 'Нет истории'}
        
        Пользователь: {message}
        
        Ассистент:"""
        
        try:
            payload = {
                "model": "codellama:7b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            response = requests.post("http://localhost:11434/api/generate", 
                                   json=payload, timeout=30)
            return response.json()["response"]
            
        except Exception as e:
            return f"Извините, произошла ошибка: {str(e)}. Использую базовые команды."
    
    def execute_command(self, command):
        """Безопасное выполнение команды"""
        dangerous = ["rm -rf", "format", "passwd", "chmod", "dd", "mkfs"]
        if any(cmd in command for cmd in dangerous):
            return "❌ Эта команда заблокирована для безопасности"
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, 
                                  text=True, timeout=120)
            return f"✅ Выполнено!\nРезультат:\n{result.stdout}\nОшибки (если есть):\n{result.stderr}"
        except subprocess.TimeoutExpired:
            return "❌ Команда выполнялась слишком долго"
        except Exception as e:
            return f"❌ Ошибка: {str(e)}"
    
    def smart_analysis(self, target):
        """Умный анализ цели"""
        analysis = f"""
🔍 **Анализ цели: {target}**

**Рекомендую следующий план:**

1. **Разведка сети** - узнаем что это за хост
   - `nmap -sn {target}` - проверим доступность
   - `ping {target}` - базовая проверка связи

2. **Сканирование портов** - что запущено на хосте
   - `nmap -sV -sC {target}` - детальное сканирование
   - `nmap -p- {target}` - все порты

3. **Веб-анализ** (если есть веб-сервер)
   - `nikto -h {target}` - поиск уязвимостей
   - `dirb http://{target}` - поиск скрытых директорий

**Начнем с базовой разведки?** (да/нет)
"""
        return analysis
    
    def start_chat(self):
        """Запускаем интерактивный чат"""
        print("\n" + "="*60)
        print("🤖 Kali AI Чат-ассистент запущен!")
        print("Я говорю на русском и помогу с пентестом")
        print("Просто опишите что хотите сделать")
        print("="*60)
        print("\nПримеры запросов:")
        print("- 'Как просканировать локальную сеть?'")
        print("- 'Найди уязвимости на сайте example.com'") 
        print("- 'Помоги настроить сканирование портов'")
        print("- 'Что можно сделать с помощью Kali?'")
        print("\nДля выхода введите 'выход' или 'quit'")
        print("-"*60)
        
        while True:
            try:
                user_input = input("\n👤 Вы: ").strip()
                
                if user_input.lower() in ['выход', 'quit', 'exit']:
                    print("👋 До свидания! Возвращайтесь для новых экспериментов.")
                    break
                elif not user_input:
                    continue
                
                # Сохраняем историю
                self.chat_history.append(f"User: {user_input}")
                
                print("\n🤖 AI: Думаю...")
                
                # Умная обработка запросов
                if any(word in user_input.lower() for word in ['привет', 'здравств', 'hello']):
                    response = "Привет! Я ваш ассистент по Kali Linux. Чем могу помочь?"
                
                elif any(word in user_input.lower() for word in ['помощь', 'help', 'команды']):
                    response = """
**Доступные возможности:**

🔍 **Сканирование:**
- Сканирование сети и портов
- Веб-анализ на уязвимости  
- Поиск скрытых директорий
- Анализ SSL сертификатов

📊 **Анализ:**
- Анализ результатов сканирования
- Генерация отчетов
- Рекомендации по дальнейшим действиям

🛠️ **Автоматизация:**
- Создание проектов пентеста
- Автоматическое сканирование
- Умный подбор инструментов

**Просто опишите что хотите сделать!**
"""
                elif any(word in user_input.lower() for word in ['сканир', 'scan', 'nmap']):
                    # Ищем цель в сообщении
                    target = "example.com"
                    if any(word in user_input for word in ['локальн', 'local', 'сеть']):
                        target = "192.168.1.0/24"
                    elif any(word in user_input for word in ['сайт', 'website', 'http']):
                        target = "testphp.vulnweb.com"
                    
                    response = self.smart_analysis(target)
                    
                elif any(word in user_input.lower() for word in ['создай', 'create', 'проект']):
                    project_name = f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    os.makedirs(project_name, exist_ok=True)
                    response = f"✅ Создал проект '{project_name}'! Теперь можем начать сканирование."
                
                else:
                    # Используем AI для сложных запросов
                    response = self.ask_ai_russian(user_input)
                
                # Показываем ответ с форматированием
                print(f"\n🤖 AI: {response}")
                self.chat_history.append(f"Assistant: {response}")
                
                # Если в ответе есть команды - предлагаем выполнить
                if "`" in response and any(cmd in response for cmd in ["nmap", "nikto", "dirb"]):
                    execute = input("\n🚀 Выполнить рекомендованные команды? (да/нет): ")
                    if execute.lower() in ['да', 'yes', 'y', 'д']:
                        self.execute_recommended_commands(response)
                
            except KeyboardInterrupt:
                print("\n👋 До свидания!")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")
    
    def execute_recommended_commands(self, ai_response):
        """Выполняет команды из ответа AI"""
        # Извлекаем команды из ответа (те что в `backticks`)
        lines = ai_response.split('\n')
        commands = []
        
        for line in lines:
            if '`' in line:
                # Извлекаем текст между ` `
                start = line.find('`') + 1
                end = line.find('`', start)
                if start > 0 and end > start:
                    command = line[start:end]
                    if any(cmd in command for cmd in ["nmap", "nikto", "dirb", "gobuster"]):
                        commands.append(command)
        
        if commands:
            print(f"\n🔧 Нашел {len(commands)} команд для выполнения:")
            for i, cmd in enumerate(commands, 1):
                print(f"{i}. {cmd}")
            
            choice = input("\nВыполнить все команды? (да/нет/номер): ")
            
            if choice.lower() in ['да', 'yes', 'y', 'д', 'all']:
                for cmd in commands:
                    print(f"\n🚀 Выполняю: {cmd}")
                    result = self.execute_command(cmd)
                    print(f"📊 Результат: {result}")
                    time.sleep(2)
            elif choice.isdigit() and 1 <= int(choice) <= len(commands):
                cmd = commands[int(choice)-1]
                print(f"\n🚀 Выполняю: {cmd}")
                result = self.execute_command(cmd)
                print(f"📊 Результат: {result}")
        else:
            print("❌ Не нашел команд для выполнения")

def main():
    assistant = KaliChatAssistant()
    assistant.start_chat()

if __name__ == "__main__":
    main()
