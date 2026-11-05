import logging
import sqlite3

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s- %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional 

from db import DatabaseManager
from models import Task

app = FastAPI(title='Task Manager API')

db = DatabaseManager()

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ''
    deadline: Optional[str] = None
    category_id: Optional[int] = Field(default=None, example=None)

@app.get('/tasks')
def get_all_tasks():
    tasks = db.get_tasks()

    return [
        {
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'status': t.status,
            'deadline': t.deadline
        }
        for t in tasks
    ]

@app.post('/tasks')
def create_task(task_data: TaskCreate):
    logger.info('POST /tasks: title=%s', task_data.title)
    try:

        new_task = Task(
             title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline,
            category_id=task_data.category_id
        )

        db.add_task(new_task)

        logger.info('Задача создана ID=%s', new_task.id)

        return {
            'message': 'Задача успешно создана',
            'task_id': new_task.id
        }
    except ValueError as e:
        logger.warning('Ошибка валидации: %s', e)
        raise HTTPException(status_code=400, detail=str(e))
    except sqlite3.IntegrityError as e:
        logger.error('Ошибка БД: %s', e)
        raise HTTPException(
            status_code=400,
            detail='Категория с таким ID не существует'
        )

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[str] = None

@app.put('/tasks/{task_id}')
def update_task(task_id: int, task_data: TaskUpdate):
    logger.info(
        'PUT /tasks/%s: поля=%s', 
        task_id, 
        list(task_data.model_dump(exclude_none=True).keys())
    )
    updates = task_data.model_dump(exclude_none=True)

    if not updates:
        logger.warning('PUT /tasks/%s: пустой запрос, нет полей для обновления', task_id)
        raise HTTPException(status_code=400, detail='Нет полей для обновления')

    updated = db.update_task(task_id, **updates)

    if updated is None:
        logger.warning('Задача ID=%s не найдена', task_id)
        raise HTTPException(status_code=404, detail='Задача не найдена')

    logger.info('Задача ID=%s обновлена', task_id)

    return {
        'message': 'Задача обновлена',
        'task': {
            'id': updated.id,
            'title': updated.title,
            'description': updated.description,
            'status': updated.status,
            'deadline': updated.deadline
        }
    }

@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):

    logger.info('DELETE /tasks/%s', task_id)

    success = db.delete_task(task_id)

    if not success:
        logger.warning('Задача ID=%s не найдена', task_id)
        raise HTTPException(status_code=404, detail='Задача не найдена')

    logger.info('Задача ID=%s удалена', task_id)

    return {'message': f'Задача {task_id} удалена'}