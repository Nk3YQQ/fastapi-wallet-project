from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import IntegrityError

from config.settings import ACCESS_TOKEN_EXPIRE_HOURS
from users.models import User
from users.schemas import Token
from users.schemas import User as UserSerializer
from users.schemas import UserRegistrationSerializer, UserUpdateSerializer, UserWithWallets
from users.services import authenticate_user, check_passport, create_access_token, get_current_user, get_password_hash

router = APIRouter()

UserPydantic = pydantic_model_creator(User)


@router.post(
    "/registration",
    response_model=UserSerializer,
    status_code=status.HTTP_201_CREATED,
    description="Create a new user",
)
async def registration(form_data: UserRegistrationSerializer):
    """Контроллер для регистрации пользователя"""

    await check_passport(form_data.passport_series, form_data.passport_number)

    try:
        hashed_password = get_password_hash(form_data.password)

        user_obj = await User.create(
            first_name=form_data.first_name,
            last_name=form_data.last_name,
            email=form_data.email,
            password=hashed_password,
            passport_series=form_data.passport_series,
            passport_number=form_data.passport_number,
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User with current email is already registered"
        )

    user = await UserPydantic.from_tortoise_orm(user_obj)

    return user


@router.post("/login", response_model=Token, description="Login for user")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Контроллер для авторизации и получения токена доступа"""
    email = form_data.username
    password = form_data.password

    user = await authenticate_user(email, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/profile", response_model=UserWithWallets, description="Get the profile of current user")
async def read_current_user(current_user: User = Depends(get_current_user)):
    """Контроллер для получения текущего пользователя"""

    user = await User.filter(id=current_user.id).prefetch_related("wallets").first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@router.patch("/profile/update", response_model=UserSerializer, description="Update the profile of current user")
async def update_current_user(form_data: UserUpdateSerializer, current_user: User = Depends(get_current_user)):
    """Контроллер для обновления текущего пользователя"""

    print(form_data.model_dump())

    user = await User.filter(id=current_user.id).prefetch_related("wallets").first()

    user_data = dict(form_data)

    for key, value in user_data.items():
        if value:
            setattr(user, key, value)

    await user.save()

    return user
