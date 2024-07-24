from tortoise.exceptions import ValidationError
from tortoise.validators import Validator


class WalletTypeValidator(Validator):
    """ Валидатор для определения тепа кошелька """

    def __call__(self, value: str):
        if value not in ['main', 'bonus', 'saving']:
            raise ValidationError(f"Value '{value}' should be 'main', 'bonus' or 'saving'")
