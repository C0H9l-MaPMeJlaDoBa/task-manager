class Category:

    def __init__(self, name: str, id: int = None):

        self.id = id

        if not isinstance(name, str) or not name.strip():
            raise ValueError('Название категории не может быть пустым')
        self.name = name.strip()

    def __str__(self):
        return f'Категория: {self.name}'

class Task:

    def __init__(self, title: str, category_id: int = None, description: str = '', deadline: str = None, id: int = None, status: str = 'В процессе', created_at: str = None):
         
         self.id = id

         self.category_id = category_id

         self.description = description

         self.deadline = deadline

         self.status = status

         self.created_at = created_at


         if not isinstance(title, str) or not title.strip():
             
             raise ValueError('Название задачи не может быть пустым')
         
         self.title = title.strip()

         allowed_statuses = ['В процессе', 'Выполнено']

         if status not in allowed_statuses:
             
             raise ValueError(f'Статус должен быть одним из: {allowed_statuses}')

    def __str__(self):

        status_mark = '+' if self.status == 'Выполнено' else '-'

        return f"{status_mark} {self.title} (Дедлайн: {self.deadline or 'Нет'})"
        