import sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.table import Table

from db import DatabaseManager
from models import Category, Task

console = Console()
db = DatabaseManager()

def show_menu():
    """Отображает главное меню"""
    console.print('\n[bold cyan]=== Менеджер задач ===[/bold cyan]')
    console.print('1. Добавить задачу')
    console.print('2. Показать все задачи')
    console.print('3. Показать категории')
    console.print('0. Выход')
    console.print('------------------------')

def main():
    """Главный цикл программы."""
    while True:
        show_menu()
        choice = Prompt.ask('[yellow]Выберите действие[/yellow]', choices=["0", "1", "2", "3"])

        if choice == '0':
            console.print('[green]До встречи![/green]')
            db.close()
            sys.exit()

        elif choice == '1':
            console.print('-')

        elif choice == '2':
            console.print('-')

        elif choice == '3':
            console.print('-')

if __name__ == '__main__':
    main()