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


def test_all_products():
    response = client.get("/all_products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_productfolder():
    response = client.get("/productfolder")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


def test_get_product():
    response = client.get("/product")
    assert response.status_code == 200
    data = response.json()
    assert len(data['products']) == 5
    response = client.get("/product", params={'limit': 10})
    assert response.status_code == 200
    assert len(response.json()['products']) == 10
    response = client.get("/product", params={'search': "мясная"})
    assert response.status_code == 200
    assert response.json()['products'][0]['name'] == 'Мясная нарезка'


def test_customerorder():
    response = client.post("/product_order")
    assert response.status_code == 200
