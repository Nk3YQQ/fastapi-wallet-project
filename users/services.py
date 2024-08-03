from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from config.settings import ALGORITHM, SECRET_KEY
from users.models import User
from users.schemas import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def verify_password(plain_password, hashed_password):
    """Функция для верификации паролей"""

    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Функция для хеширования паролей"""

    return pwd_context.hash(password)


async def get_user(email: str):
    """Функция для получения пользователя по почте"""

    return await User.filter(email=email).first()


async def authenticate_user(email: str, password: str):
    """Функция для аутентификации пользователя"""

    user = await get_user(email)

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Функция для создания access токена"""

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Функция для получения текущего пользователя"""

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

        token_data = TokenData(email=email)

    except JWTError:
        raise credentials_exception

    user = await get_user(email=token_data.email)

    if user is None:
        raise credentials_exception

    return user


async def check_passport(passport_series, passport_number):
    """Функция проверяет, существует ли пользователь с соответствующим паспортом"""

    user = await User.filter(passport_series=passport_series, passport_number=passport_number).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User with these series and number already exist"
        )
