from typing import Literal, Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

str_150 = Annotated[str, StringConstraints(max_length=150)]
str_100 = Annotated[str, StringConstraints(max_length=100)]


class UserSerializer(BaseModel):
    """ Базовая модель для пользователя """

    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str_150
    last_name: str_150
    email: str
    passport_series: str
    passport_number: str
    wallets: list['WalletSerializer']


class WalletSerializer(BaseModel):
    """ Базовая модель для кошелька """

    model_config = ConfigDict(from_attributes=True)

    id: int
    balance: int
    currency: str
    wallet_type: Literal['main', 'bonus', 'saving']
    owner: UserSerializer


class WalletCreateSerializer(BaseModel):
    """ Модель для создания кошелька """

    balance: int
    currency: str
    wallet_type: Literal['main', 'bonus', 'saving']
    owner_id: int
