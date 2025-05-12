from tel_bot.database import SessionLocal
from passlib.context import CryptContext
from fastapi import Depends, Header
from sqlalchemy.orm import Session
from fastapi import Request, HTTPException, status, Depends
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from tel_bot.users.models import UserModel
from tel_bot.config import SECRET_KEY_TOKEN, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user or verify_password(plain_password=password, hashed_password=user.hash_password) is False:
        return None
    return user


def get_auth_data():
    return {"secret_key": SECRET_KEY_TOKEN, "algorithm": ALGORITHM}


async def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail='не авторизован')
    try:
        auth_data = get_auth_data()
        token_type, access_token = authorization.split()
        payload = jwt.decode(access_token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except ValueError:
        raise HTTPException(status_code=401, detail='неправильный заголовок')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')
    if token_type != 'Bearer':
        raise HTTPException(status_code=401, detail='неправильный тип')
    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')
    user = db.query(UserModel).filter(UserModel.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_TOKEN, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY_TOKEN, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )


