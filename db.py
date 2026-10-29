import sqlite3

from models import Category, Task

class DatabaseManager:

    def __init__(self, db_name='tasks.db'):

        self.conn = sqlite3.connect(db_name)

        self.cursor = self.conn.cursor()

        self.cursor.execute('PRAGMA foreign_keys = ON;')

        self.create_tables()

    def create_tables(self):

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                category_id INTEGER,
                status TEXT DEFAULT 'В процессе',
                deadline TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        ''')

        self.conn.commit()

    def add_category(self, category: Category) -> Category:

        """Добавляет категорию в базу данных и возвращает её с присвоенным id"""
        
        self.cursor.execute(
            "INSERT INTO categories (name) VALUES (?)",
            (category.name,)
        )

        self.conn.commit()

        category.id = self.cursor.lastrowid

        return category
    
    def add_task(self, task: Task) -> Task:

        """Добавляет задачу в базу и возвращает её с присвоенным id"""

        self.cursor.execute(
            """
            INSERT INTO tasks (title, description, category_id, status, deadline)
            VALUES (?, ?, ?, ?, ?)
            """, 
            (task.title, task.description, task.category_id, task.status, task.deadline)
        )

        self.conn.commit()

        task.id = self.cursor.lastrowid

        return task

    def get_categories(self) -> list[Category]:

        self.cursor.execute("SELECT id, name FROM categories")

        rows = self.cursor.fetchall()

        categories = []

        for row in rows:

            cat = Category(id=row[0], name=row[1])

            categories.append(cat)

        return categories

    def get_tasks(self) -> list[Task]:

        self.cursor.execute("""
            SELECT id, title, description, category_id, status, deadline, created_at
            FROM tasks
        """)

        rows = self.cursor.fetchall()

        tasks = []

        for row in rows:
            t = Task(
                id = row[0],
                title = row[1],
                description = row[2],
                category_id = row[3],
                status = row[4],
                deadline = row[5],
                created_at = row[6]
            )

            tasks.append(t)
        return tasks

    def update_task_status(self, task_id: int, new_status: str) -> bool:
        """Обновляет статус задачи. Вернёт True, если удалось"""
        if new_status not in ['В процессе', 'Выполнено']:
            raise ValueError('Неверный статус')

        self.cursor.execute(
            'UPDATE tasks SET status = ? WHERE id = ?',
            (new_status, task_id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_task(self, task_id: int) -> bool:
        """Удаляет задачу по ID. Возвращает True, если удалось"""
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def close(self):

        self.conn.close()

if __name__ == '__main__':

    db = DatabaseManager()

    print('База данных успешно подключена!')

    cat = Category('Учеба')

    db.add_category(cat)

    print(f'Сохранена категория: {cat}')

    new_task = Task("Сдать проект", category_id=cat.id, deadline="2026-11-01")

    db.add_task(new_task)

    print(f'Сохранена задача: {new_task}')

    print('\nВсе категории из базы:')

    all_cats = db.get_categories()

    for c in all_cats:

        print(c)

    print('\nВсе задачи из базы:')

    all_tsk = db.get_tasks()

    for t in all_tsk:

        print(t)

    db.close()
