from typing import Literal

from pydantic import BaseModel, ConfigDict, StringConstraints, model_validator, ValidationError, EmailStr
from typing_extensions import Annotated

str_150 = Annotated[str, StringConstraints(max_length=150)]
str_100 = Annotated[str, StringConstraints(max_length=100)]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserRegistrationSerializer(BaseModel):
    """ Модель для регистрации пользователя """

    first_name: str_150
    last_name: str_150
    email: EmailStr
    passport_series: str
    passport_number: str
    password: str
    password_confirm: str

    @model_validator(mode='after')
    def password_match(self):
        password = self.password
        password_confirm = self.password_confirm

        if password != password_confirm:
            raise ValidationError('Passwords should be equal')
        return self


class UserSerializer(BaseModel):
    """ Базовая модель для пользователя """

    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str_150
    last_name: str_150
    email: str
    passport_series: str
    passport_number: str
    wallets: list['WalletSerializer'] = []


class WalletSerializer(BaseModel):
    """ Базовая модель для кошелька """

    model_config = ConfigDict(from_attributes=True)
    id: int
    balance: int
    currency: str
    wallet_type: Literal['main', 'bonus', 'saving']
    owner: UserSerializer
