from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserRegister(BaseModel):
    username: str
    email: str
    full_name: str
    password: str = Field(..., min_length=4, max_length=50, description="Пароль, от 4 до 50 знаков")
