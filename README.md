# Task Manager

Это менеджер задач с двумя интерфейсами: CLI для терминала (Windows) и REST API на FastAPI. Данные хранятся в SQLite, валидация входящих данных выполняется через Pydantic.

## О проекте

Это учебный backend-проект, демонстрирующий полный цикл разработки: от проектирования моделей и базы данных до создания REST API с автоматической документацией. Реализованы CRUD-операции, обработка ошибок и разделение ответственности между слоями (модели, работа с БД, интерфейсы).

## Стек

- **Язык:** Python 3.12
- **Фреймворк:** FastAPI, Uvicorn
- **База данных:** SQLite
- **Валидация:** Pydantic
- **CLI:** rich
- **Инструменты:** Git, venv

## Структура проекта

```text
task_manager_project/
├── api.py             # REST API на FastAPI (эндпоинты, Pydantic-схемы)
├── db.py              # DatabaseManager: подключение и CRUD-операции с SQLite
├── main.py            # CLI-интерфейс на rich
├── models.py          # Классы Task и Category
├── test_api.py        # Тесты (pytest)
├── requirements.txt   # Зависимости проекта
├── .gitignore         # Исключения для Git (venv, __pycache__, *.db)
└── README.md
```

## Запуск

### 1. Клонировать репозиторий 
```bash
git clone <ссылка-на-репозиторий>
cd <имя папки>
```

### 2. Создать и активировать виртуальное окружение
```bash
python -m venv venv
venv\Scripts\activate           # Windows
# source venv/bin/activate      # Linux / macOS
```

### 3. Установить зависимости
```bash
pip install -r requirements.txt
```

### 4. Запустить CLI
```bash
python main.py
```

### 5. Запустить REST API
```bash
uvicorn api:app --reload
```