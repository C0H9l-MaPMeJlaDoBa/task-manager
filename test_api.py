from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_get_all_tasks():
    """Проверка, что GET /tasks возвращает код 200 и список."""
    response = client.get('/tasks')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_task():
    """Проверка, что POST /tasks создаёт задачу."""
    response = client.post('/tasks', json={'title': 'Тестовая задача'})
    assert response.status_code == 200
    assert 'task_id' in response.json()

def test_get_task_not_found():
    """Проверка, что при неверном ID возвращается 404."""
    response = client.get('/tasks/000000000')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Задача не найдена'

def test_create_category():
    """Проверка создания категории."""
    response = client.post('/categories', json={'name': 'Тестовая категория'})
    assert response.status_code == 200
    assert 'id' in response.json()