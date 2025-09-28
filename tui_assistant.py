#!/usr/bin/env python3
import os
import sys
import requests
import subprocess
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich import box

console = Console()

class KaliTUIAssistant:
    def __init__(self):
        self.workspace = f"{os.path.expanduser('~')}/kali_tui_workspace"
        os.makedirs(self.workspace, exist_ok=True)
        os.chdir(self.workspace)
        
        self.history = []
        self.setup_ui()
        
    def setup_ui(self):
        """Настраиваем интерфейс"""
        console.clear()
        console.print(
            Panel.fit(
                "🎯 [bold cyan]Kali Linux AI Assistant[/bold cyan] - Графический интерфейс",
                border_style="green",
                padding=(1, 2)
            )
        )
    
    def show_main_menu(self):
        """Главное меню"""
        while True:
            console.clear()
            
            # Создаем layout
            layout = Layout()
            
            # Заголовок
            layout.split_column(
                Layout(name="header", size=3),
                Layout(name="main"),
                Layout(name="footer", size=3)
            )
            
            # Заголовок
            header_text = Text()
            header_text.append("🎯 ", style="bold red")
            header_text.append("Kali AI Assistant", style="bold cyan")
            header_text.append(" - Выберите действие", style="bold white")
            
            layout["header"].update(
                Panel(header_text, style="bold", box=box.DOUBLE)
            )
            
            # Основное меню
            menu_table = Table(show_header=False, box=box.ROUNDED)
            menu_table.add_column("№", style="cyan", width=3)
            menu_table.add_column("Действие", style="white")
            menu_table.add_column("Описание", style="green")
            
            menu_items = [
                ("1", "💬 Чат с AI", "Общение на естественном языке"),
                ("2", "🔍 Быстрое сканирование", "Автоматический анализ цели"),
                ("3", "📊 История команд", "Просмотр выполненных действий"),
                ("4", "🛠️ Инструменты", "Прямой доступ к утилитам"),
                ("5", "⚙️ Настройки", "Конфигурация ассистента"),
                ("6", "❌ Выход", "Завершение работы")
            ]
            
            for num, action, desc in menu_items:
                menu_table.add_row(num, action, desc)
            
            layout["main"].update(
                Panel(menu_table, title="[bold yellow]Главное меню[/bold yellow]")
            )
            
            # Футер
            layout["footer"].update(
                Panel("[italic]Используйте цифры 1-6 для выбора[/italic]", box=box.SIMPLE)
            )
            
            console.print(layout)
            
            choice = Prompt.ask(
                "Выберите действие",
                choices=["1", "2", "3", "4", "5", "6"],
                default="1"
            )
            
            if choice == "1":
                self.chat_interface()
            elif choice == "2":
                self.quick_scan_interface()
            elif choice == "3":
                self.show_history()
            elif choice == "4":
                self.tools_interface()
            elif choice == "5":
                self.settings_interface()
            elif choice == "6":
                console.print("👋 До свидания!", style="bold green")
                break
    
    def chat_interface(self):
        """Интерфейс чата"""
        console.clear()
        console.print(
            Panel.fit(
                "💬 [bold cyan]Режим чата с AI[/bold cyan]",
                border_style="blue"
            )
        )
        
        console.print("[italic]Введите ваш вопрос или 'назад' для возврата[/italic]\n")
        
        while True:
            user_input = Prompt.ask("[bold green]Вы[/bold green]")
            
            if user_input.lower() in ['назад', 'back', 'exit']:
                break
            
            # Имитация ответа AI
            with console.status("[bold green]AI думает...[/bold green]"):
                import time
                time.sleep(1)
                
                # Простой AI ответ
                if 'сканир' in user_input.lower():
                    response = """🤖 **AI ассистент:**
                    
Для сканирования рекомендую:

🔍 **Базовое сканирование:**
```bash
nmap -sV -sC target.com
