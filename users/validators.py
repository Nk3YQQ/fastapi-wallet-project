import re

from tortoise.exceptions import ValidationError
from tortoise.validators import Validator


class PassportSeriesValidator(Validator):
    """ Валидатор для серии паспорта """

    def __call__(self, value: str):
        if len(value) != 4:
            raise ValidationError(f"Len of value '{value}' should be equal 4")


class PassportNumberValidator(Validator):
    """ Валидатор для номера паспорта """

    def __call__(self, value: str):
        if len(value) != 6:
            raise ValidationError(f"Len of value '{value}' should be equal 6")


class EmailValidator(Validator):
    """ Валидатор для электронной почты """

    def __call__(self, value: str):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(email_regex, value):
            raise ValidationError(f"Incorrect type for '{value}'")
