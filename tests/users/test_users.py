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
    test_user = UserModel(id=1, username="testuser", email='test_email', hash_password='test_password', full_name='test_fullname')
    return test_user

app.dependency_overrides[get_current_user] = override_get_current_user


def test_register():
    response = client.get("/users")
    assert response.status_code == 200


def test_register_user():
    response = client.post("/register", json={
        "username": "test",
        "email": "test",
        "full_name": "test",
        "password": "test"
        })
    assert response.status_code == 200
    response = client.post("/register", json={
        "username": "test",
        "email": "test",
        "full_name": "test",
        "password": "test"
        })
    assert response.status_code == 409


def test_auth_user():
    response = client.post("/login", json={
        "username": "test",
        "password": "test"
    })
    assert response.status_code == 200
    response = client.post("/login", json={
        "username": "test_new_test",
        "password": "test_new_test"
    })
    assert response.status_code == 401
    response = client.post("/login", json={
        "username": "test",
        "password": "test_new_test"
    })
    assert response.status_code == 401
    response = client.post("/login", json={
        "username": "test_new_test",
        "password": "test"
    })
    assert response.status_code == 401


def test_get_me():
    response = client.get("/me")
    assert response.status_code == 200
