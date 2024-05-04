import warnings
import os

import pytest
import pytest_asyncio
import alembic

from typing import AsyncGenerator

from async_asgi_testclient import TestClient
from fastapi import FastAPI
from databases import Database
from alembic.config import Config


# @pytest.fixture(scope="session")
# def apply_migrations():
#     warnings.filterwarnings("ignore", category=DeprecationWarning)
#     os.environ["TESTING"] = "1"
#     config = Config("alembic.ini")

#     alembic.command.upgrade(config, "head")
#     yield
#     alembic.command.downgrade(config, "base")


@pytest.fixture
def app() -> FastAPI:
    from hirey.api.server import get_application

    return get_application()


@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator[TestClient, None]:
    async with TestClient(app) as client:
        yield client
