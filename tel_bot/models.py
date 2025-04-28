from pydantic import BaseModel
from typing import Optional
from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from tel_bot.database import Base


class OrderModelBase(BaseModel):
    id_prod: str
    counter: int


class OrderModel(BaseModel):
    items: List[OrderModelBase]


class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    password: str


class UserModel(Base):
    '''
    __tablename__ - имя таблицы
    primary_key - для первичного ключа
    index - для поиска из БД (быстрый поиск)
    '''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String)
    full_name = Column(String)
    hash_password = Column(String, nullable=True)
