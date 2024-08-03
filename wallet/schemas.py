from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints

str_150 = Annotated[str, StringConstraints(max_length=150)]
str_100 = Annotated[str, StringConstraints(max_length=100)]


class User(BaseModel):
    """Базовая модель для пользователя"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str_150
    last_name: str_150
    email: str
    passport_series: str
    passport_number: str


class Wallet(BaseModel):
    """Базовая модель для кошелька"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    number: str
    balance: int
    currency: Literal["USD", "EUR", "RUB", "CNY"]
    wallet_type: Literal["main", "bonus", "saving"]
    owner: User


class WalletCreateSerializer(BaseModel):
    """Модель для создания кошелька"""

    currency: Literal["USD", "EUR", "RUB", "CNY"]
    wallet_type: Literal["main", "bonus", "saving"]


class WalletUpdateSerializer(BaseModel):
    """Модель для обновления кошелька"""

    balance: int
    currency: Literal["USD", "EUR", "RUB", "CNY"]
    wallet_type: Literal["main", "bonus", "saving"]


class WalletUpdateParticularSerializer(BaseModel):
    """Модель для частичного обновления кошелька"""

    balance: int | None = None
    currency: Literal["USD", "EUR", "RUB", "CNY"] | None = None
    wallet_type: Literal["main", "bonus", "saving"] | None = None
