import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from fastapi import Depends
from sqlalchemy.ext.declarative import declarative_base

from tel_bot.main import app  # импорт вашего FastAPI приложения
from tel_bot.carts.models import CartModel  # ваши модели
from tel_bot.users.models import UserModel  # ваши модели
from tel_bot.users.utils import get_db, get_current_user
from tel_bot.database import Base

# Создаём клиент для тестирования FastAPI
client = TestClient(app)

# Мокаем get_current_user, чтобы возвращать тестового пользователя
def override_get_current_user():
    test_user = UserModel(id=1)
    return test_user

app.dependency_overrides[get_current_user] = override_get_current_user


def test_add_to_cart():
    response = client.post("/cart/add", json={
        "id": "04dae928-089a-11f0-0a80-165a001c4f4c", # "name": "Мясная нарезка",
        "count": 5
    })
    response = client.post("/cart/add", json={
        "id": "09205987-0899-11f0-0a80-09d9001c758e",# "name": "Блэк шип стаут",
        "count": 10
    })
    response = client.post("/cart/add", json={
        "id": "0faa771b-089a-11f0-0a80-15bb001bfcf6",# "name": "Гренки",
        "count": 15
    })
    response = client.post("/cart/add", json={
        "id": "1c375087-0898-11f0-0a80-1a37001b173f",# "name": "Гамбринус тёмное",
        "count": 7
    })
    response = client.post("/cart/add", json={
        "id": "2eb64a88-089a-11f0-0a80-01d9001be124",# "name": "Вяленый елец",
        "count": 17
    })
    assert response.status_code == 200
    response_get = client.get("/cart")
    data = response_get.json()
    assert data[-1]["product_id"] == '2eb64a88-089a-11f0-0a80-01d9001be124' # "Мясная нарезка"
    assert data[-1]["product_count"] == 17


def test_get_cart():
    response = client.get("/cart")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["user_id"] == 1
    assert data[0]["product_id"] == '04dae928-089a-11f0-0a80-165a001c4f4c' # "Мясная нарезка"
    assert data[0]["product_count"] == 5
