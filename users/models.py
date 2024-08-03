from tortoise import Model, fields

PRIMARY_KEY = {"unique": True, "null": False}


class User(Model):
    """Модель для пользователя"""

    id = fields.IntField(primary_key=True, description="Первичный ключ")
    first_name = fields.CharField(max_length=150, description="Имя")
    last_name = fields.CharField(max_length=150, description="Фамилия")
    email = fields.CharField(max_length=100, **PRIMARY_KEY, description="Электронная почта")
    password = fields.CharField(max_length=100, description="Пароль")
    passport_series = fields.CharField(max_length=4, description="Серия паспорта")
    passport_number = fields.CharField(max_length=6, description="Номер паспорта")
    wallets = fields.ReverseRelation["models.Wallet"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
