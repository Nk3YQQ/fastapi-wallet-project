from fastapi import APIRouter, Depends

from users.auth import get_current_user
from users.models import User
from users.schemas import WalletSerializer
from wallet.models import Wallet
from wallet.schemas import WalletCreateSerializer

router = APIRouter()


@router.post('/create/', response_model=WalletSerializer, description='Create a new wallet')
async def create_wallet(wallet: WalletCreateSerializer, current_user: User = Depends(get_current_user)):
    """ Контроллер для создания кошелька """

    wallet_obj = Wallet.create(
        balance=wallet.balance,
        currency=wallet.currency,
        wallet_type=wallet.wallet_type,
        owner=current_user
    )

    return wallet_obj
