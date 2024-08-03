from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from tortoise.contrib.test import initializer, finalizer

from main import app


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
def initialize_test() -> AsyncGenerator[None, None]:
    initializer(modules=["wallet.models", "users.models"])
    yield
    finalizer()


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        yield client
