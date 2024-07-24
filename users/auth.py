import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from users.models import User
from users.schemas import TokenData

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_HOURS = 2

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    """ Функция для верификации паролей """

    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """ Функция для хеширования паролей """

    return pwd_context.hash(password)


async def get_user(email: str):
    """ Функция для получения пользователя по почте """

    return await User.get(email=email)


async def authenticate_user(email: str, password: str):
    """ Функция для аутентификации пользователя """

    user = await get_user(email)

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """ Функция для создания access токена """

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """ Функция для получения текущего пользователя """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

        token_data = TokenData(username=email)

    except JWTError:
        raise credentials_exception

    user = await get_user(email=token_data.email)

    if user is None:
        raise credentials_exception

    return user
