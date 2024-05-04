import warnings
import os

import pytest
import pytest_asyncio
import alembic

from typing import AsyncGenerator

from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from databases import Database
from alembic.config import Config


@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")

    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from hirey.api.server import get_application

    return get_application()


@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(app, startup_timeout=10, shutdown_timeout=10):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client
