from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from config.database import TORTOISE_ORM
from users.routers import router as users_router
from wallet.routers import router as wallet_router


app = FastAPI(title='Wallet app')

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True
)

app.include_router(users_router, prefix='/users', tags=['users'])
app.include_router(wallet_router, prefix='/wallets', tags=['wallet'])
