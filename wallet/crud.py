from fastapi import HTTPException
from tortoise.contrib.pydantic import pydantic_model_creator

from wallet.models import Wallet


class WalletCRUD:
    """CRUD для модели кошелька"""

    def __init__(self):
        self.model = Wallet
        self.model_serializer = pydantic_model_creator(Wallet)

    async def get_object(self, wallet_id: int, current_user):
        """Получение объекта кошелька по его id"""

        wallet = await self.model.filter(id=wallet_id).select_related("owner").first()

        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")

        if wallet.owner.id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")

        return wallet

    async def create_wallet(self, form_data, current_user):
        """Создание объекта кошелька"""

        number = await Wallet.generate_wallet_number()

        wallet = await self.model.create(
            number=number, currency=form_data.currency, wallet_type=form_data.wallet_type, owner=current_user
        )

        return wallet

    async def read_wallet_list(self, skip, limit, current_user):
        """Чтение списка кошельков"""

        wallets = await self.model.filter(owner=current_user).select_related("owner").offset(skip).limit(limit)

        return wallets

    async def read_wallet_object(self, wallet_id: int, current_user):
        """Чтение объекта кошелька"""

        wallet = await self.get_object(wallet_id, current_user)

        return await self.model_serializer.from_tortoise_orm(wallet)

    async def update_wallet(self, wallet_id: int, form_data, current_user):
        """Обновление объекта кошелька"""

        wallet = await self.get_object(wallet_id, current_user)

        wallet_data = dict(form_data)

        for key, value in wallet_data.items():
            if value:
                setattr(wallet, key, value)

        await wallet.save()

        return wallet

    async def delete_wallet(self, wallet_id: int, current_user):
        """Удаление объекта кошелька"""

        wallet = await self.get_object(wallet_id, current_user)

        await wallet.delete()

        return {"status": 204, "description": "Wallet was deleted"}
