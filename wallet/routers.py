from typing import List

from fastapi import APIRouter, Depends
from tortoise.contrib.pydantic import pydantic_model_creator

from users.models import User
from users.services import get_current_user
from wallet.crud import WalletCRUD
from wallet.models import Wallet
from wallet.schemas import Wallet as WalletSerializer
from wallet.schemas import WalletCreateSerializer, WalletUpdateParticularSerializer, WalletUpdateSerializer

router = APIRouter()

WalletPydantic = pydantic_model_creator(Wallet)


@router.post("/", response_model=WalletSerializer, description="Create a new wallet")
async def create_wallet(
    form_data: WalletCreateSerializer, current_user: User = Depends(get_current_user), crud: WalletCRUD = Depends()
):
    """Контроллер для создания кошелька"""

    return await crud.create_wallet(form_data, current_user)


@router.get("/", response_model=List[WalletSerializer], description="Get wallet list")
async def read_wallets(
    skip: int = 0, limit: int = 10, current_user: User = Depends(get_current_user), crud: WalletCRUD = Depends()
):
    """Контроллер для чтения списка кошельков"""

    return await crud.read_wallet_list(skip, limit, current_user)


@router.get("/{wallet_id}", response_model=WalletSerializer, description="Get one wallet")
async def read_wallet(wallet_id: int, current_user: User = Depends(get_current_user), crud: WalletCRUD = Depends()):
    """Контроллер для чтения списка кошельков"""

    return await crud.read_wallet_object(wallet_id, current_user)


@router.put("/{wallet_id}", response_model=WalletSerializer, description="Update wallet")
async def update_wallet(
    wallet_id: int,
    form_data: WalletUpdateSerializer,
    current_user: User = Depends(get_current_user),
    crud: WalletCRUD = Depends(),
):
    """Контроллер для обновления кошелька"""

    return await crud.update_wallet(wallet_id, form_data, current_user)


@router.patch("/{wallet_id}", response_model=WalletSerializer, description="Update wallet particular")
async def update_wallet_particular(
    wallet_id: int,
    form_data: WalletUpdateParticularSerializer,
    current_user: User = Depends(get_current_user),
    crud: WalletCRUD = Depends(),
):
    """Контроллер для частичного обновления кошелька"""

    return await crud.update_wallet(wallet_id, form_data, current_user)


@router.delete("/{wallet_id}", description="Delete wallet")
async def delete_wallet(wallet_id: int, current_user: User = Depends(get_current_user), crud: WalletCRUD = Depends()):
    """Контроллер для удаления кошелька"""

    return crud.delete_wallet(wallet_id, current_user)
