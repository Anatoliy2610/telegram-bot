from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY_TOKEN = os.getenv('SECRET_KEY_TOKEN')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_TOKEN, algorithm=ALGORITHM)
    return encoded_jwt
