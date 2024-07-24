from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import IntegrityError

from users.auth import (get_password_hash, authenticate_user, ACCESS_TOKEN_EXPIRE_HOURS, create_access_token,
                        get_current_user)
from users.models import User
from users.schemas import UserSerializer, UserRegistrationSerializer, Token

router = APIRouter()


@router.post('/register/', response_model=UserSerializer)
async def register_user(user: UserRegistrationSerializer):
    """ Контроллер для регистрации пользователя """

    hashed_password = get_password_hash(user.password)

    try:
        user_obj = await User.create(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=hashed_password,
            passport_serias=user.passport_series,
            passport_number=user.passport_number
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with current email is already registered'
        )

    return user_obj


@router.post('/token/', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """ Контроллер для получения access токена """

    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/me/', response_model=User)
async def read_current_user(current_user: User = Depends(get_current_user)):
    """ Контроллер для получения текущего пользователя """

    return current_user
