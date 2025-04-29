from pydantic import BaseModel
from typing import Optional
from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint
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


class Cart(BaseModel):
    user_id: int
    product_id: str
    product_count: int


class CartModel(Base):
    __tablename__ = 'carts'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    product_id = Column(String, primary_key=True)
    product_count = Column(Integer)
       
    product = relationship("UserModel")

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'product_id'),
       )
