import logging

import pathlib
import sys
import alembic
import os

from sqlalchemy import engine_from_config, create_engine, pool
from psycopg2 import DatabaseError

from logging.config import fileConfig
from hirey.core.config import settings

# we're appending the app directory to our path here so that we can import config easily
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from hirey.core.config import settings  # noqa

# Alembic Config object, which provides access to values within the .ini file
config = alembic.context.config

# Interpret the config file for logging
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode
    """
    DB_URL = (
        f"{settings.DATABASE_URL}_test"
        if os.environ.get("TESTING")
        else str(settings.DATABASE_URL)
    )

    # handle testing config for migrations
    if os.environ.get("TESTING"):
        # connect to primary db
        default_engine = create_engine(
            str(settings.DATABASE_URL), isolation_level="AUTOCOMMIT"
        )
        # drop testing db if it exists and create a fresh one
        with default_engine.connect() as default_conn:
            default_conn.execute(f"DROP DATABASE IF EXISTS {settings.POSTGRES_DB}_test")
            default_conn.execute(f"CREATE DATABASE {settings.POSTGRES_DB}_test")

    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", DB_URL)


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    """
    if os.environ.get("TESTING"):
        raise DatabaseError(
            "Running testing migrations offline currently not permitted."
        )

    alembic.context.configure(url=str(settings.DATABASE_URL))

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


if alembic.context.is_offline_mode():
    logger.info("Running migrations offline")
    run_migrations_offline()
else:
    logger.info("Running migrations online")
    run_migrations_online()
