from fastapi import FastAPI

from users.routers import router

app = FastAPI(title='Users app')

app.include_router(router, prefix='/users', tags=['users'])
