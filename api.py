import sqlite3
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
    try:

        new_task = Task(
             title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline,
            category_id=task_data.category_id
        )

        db.add_task(new_task)

        return {
            'message': 'Задача успешно создана',
            'task_id': new_task.id
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail='Категория с таким ID не существует'
        )