import asyncio
import logging
import re
from logging.config import fileConfig
from typing import Any, Dict

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config, AsyncEngine
from sqlmodel import SQLModel

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# MODELS
import app.models.all  # noqa: needed to create the tables with "magic"

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

db_names = config.get_main_option("databases", "")


target_metadata = SQLModel.metadata


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations(engine: AsyncEngine) -> None:
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


async def run_migrations_online() -> None:
    engines: Dict[str, Any] = {}

    for name in re.split(r",\s*", db_names):
        engines[name] = config = {}
        config["engine"] = async_engine_from_config(
            context.config.get_section(name, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
        await run_async_migrations(config["engine"])


asyncio.run(run_migrations_online())
