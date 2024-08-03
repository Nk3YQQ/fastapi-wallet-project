from tortoise import fields
from tortoise import Model


class Wallet(Model):
    """ Модель для кошелька """

    id = fields.IntField(primary_key=True, description='Первичный ключ')
    number = fields.CharField(max_length=19, unique=True, description='Номер')
    balance = fields.DecimalField(max_digits=10, decimal_places=2, default=0, description='Баланс')
    currency = fields.CharField(max_length=3, description='Валюта')
    wallet_type = fields.CharField(max_length=20, description='Тип кошелька')

    owner = fields.ForeignKeyField('models.User', related_name='wallets', on_delete=fields.CASCADE)

    def __str__(self):
        return f'{self.id}:{self.owner}:{self.wallet_type}:{self.currency}'

    @classmethod
    async def generate_wallet_number(cls):
        last_wallet = await cls.all().order_by('-number').first()

        if last_wallet:
            last_number = int(last_wallet.number.replace(' ', ''))

        else:
            last_number = 0

        new_number = last_number + 1

        new_number_str = f'{new_number:016d}'

        formatted_number = ' '.join(new_number_str[i:i+4] for i in range(0, 16, 4))

        return formatted_number
