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

from hirey.models.cleaning import CleaningCreate, CleaningInDB
from hirey.db.repositories.cleanings import CleaningsRepository


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
async def test_cleaning(db: Database) -> CleaningInDB:
    cleaning_repo = CleaningsRepository(db)
    new_cleaning = CleaningCreate(
        name="fake cleaning name",
        description="fake cleaning description",
        price=9.99,
        cleaning_type="spot_clean",
    )

    return await cleaning_repo.create_cleaning(new_cleaning=new_cleaning)


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator[TestClient, None]:
    async with TestClient(app) as client:
        yield client
