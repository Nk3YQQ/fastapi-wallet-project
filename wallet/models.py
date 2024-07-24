from tortoise import fields
from tortoise import Model

from wallet.validators import WalletTypeValidator


class Wallet(Model):
    """ Модель для кошелька """

    id = fields.IntField(primary_key=True, description='Первичный ключ')
    balance = fields.DecimalField(max_digits=10, decimal_places=2, default=0, description='Баланс')
    currency = fields.CharField(max_length=3, description='Валюта')
    wallet_type = fields.CharField(max_length=20, validators=[WalletTypeValidator], description='Тип кошелька')

    owner = fields.ForeignKeyField('users.User', related_name='wallets', on_delete=fields.CASCADE)

    def __str__(self):
        return f'{self.id}:{self.owner}:{self.wallet_type}:{self.currency}'
