from tortoise import Model, fields

from users.validators import PassportSeriesValidator, PassportNumberValidator, EmailValidator

PRIMARY_KEY = {'unique': True, 'null': False}


class User(Model):
    """ Модель для пользователя """

    id = fields.IntField(pk=True, description='Первичный ключ')
    first_name = fields.CharField(max_length=150, description='Имя')
    last_name = fields.CharField(max_length=150, description='Фамилия')
    email = fields.CharField(max_length=100, **PRIMARY_KEY, validators=[EmailValidator()],
                             description='Электронная почта')
    password = fields.CharField(max_length=100, description='Пароль')
    passport_series = fields.IntField(validators=[PassportSeriesValidator()], description='Серия паспорта')
    passport_number = fields.IntField(validators=[PassportNumberValidator()], description='Номер паспорта')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
