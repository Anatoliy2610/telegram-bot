from fastapi import APIRouter, HTTPException, status, Depends, Response
from typing import List
from sqlalchemy.orm import Session

from tel_bot.users.utils import (get_db, get_password_hash, verify_password, create_access_token, get_current_user)
from tel_bot.users.models import UserModel, UserAuthModel, User
from tel_bot.users.shemas import UserRegister


router = APIRouter(tags=['Пользователь'])


@router.get("/users", response_model=List[User])
async def register(db: Session = Depends(get_db)):
    return db.query(UserModel).all()


@router.post("/register/")
async def register_user(user_data: UserRegister, db: Session = Depends(get_db)) -> dict:
    user = db.query(UserModel).filter(UserModel.username == user_data.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    db_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        full_name = user_data.full_name,
        hash_password = get_password_hash(user_data.password)
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login/")
async def auth_user(response: Response, user_data: UserAuthModel, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == user_data.username).first()
    check_pass = verify_password(user_data.password, user.hash_password)
    if user is None and not check_pass:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверное имя пользователя или пароль'
                            )
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}


@router.get("/me/")
async def get_me(user_data: UserModel = Depends(get_current_user)):
    return user_data


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}
