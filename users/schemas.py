from typing import List, Literal

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints, field_validator, model_validator
from typing_extensions import Annotated

str_150 = Annotated[str, StringConstraints(max_length=150)]
str_100 = Annotated[str, StringConstraints(max_length=100)]


class Wallet(BaseModel):
    """Базовая модель для кошелька"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    balance: int
    currency: Literal["USD", "EUR", "RUB", "CNY"]
    wallet_type: Literal["main", "bonus", "saving"]


class Token(BaseModel):
    """Схема для токена"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Схема для данных токена"""

    email: str | None = None


class UserRegistrationSerializer(BaseModel):
    """Модель для регистрации пользователя"""

    first_name: str_150
    last_name: str_150
    email: EmailStr
    passport_series: str
    passport_number: str
    password: str
    password_confirm: str

    @model_validator(mode="after")
    def password_match(self):
        password = self.password
        password_confirm = self.password_confirm

        if password != password_confirm:
            raise ValueError("Passwords should be equal")
        return self

    @field_validator("passport_series")
    @classmethod
    def validate_passport_series(cls, v: str):
        if len(v) != 4 or not v.isdigit():
            raise ValueError("Len of value passport_series should be equal 6")
        return v

    @field_validator("passport_number")
    @classmethod
    def validate_passport_number(cls, v: str):
        if len(v) != 6 or not v.isdigit():
            raise ValueError("Len of value passport_number should be equal 6")
        return v

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, v: str):
        if not v.isalpha():
            raise ValueError("First name and last name should be only string")
        return v.capitalize()


class User(BaseModel):
    """Базовая модель для пользователя"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str_150
    last_name: str_150
    email: str
    passport_series: str
    passport_number: str


class UserWithWallets(User):
    """Модель пользователя с кошельком"""

    wallets: List["Wallet"]


class UserUpdateSerializer(BaseModel):
    """Модель для обновления данных пользователя"""

    first_name: str_150 | None = None
    last_name: str_150 | None = None
    email: EmailStr | None = None
    passport_series: str | None = None
    passport_number: str | None = None
