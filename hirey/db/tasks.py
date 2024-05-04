import os
import logging

from fastapi import FastAPI
from databases import Database
from hirey.core.config import settings

logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI) -> None:
    DB_URL = (
        f"{settings.DATABASE_URL}_test"
        if os.environ.get("TESTING")
        else settings.DATABASE_URL
    )
    database = Database(DB_URL, min_size=2, max_size=10)

    try:
        await database.connect()
        app.state._db = database
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")
