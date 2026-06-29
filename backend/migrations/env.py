"""
migrations/env.py
─────────────────────────────────────────────────────────────────
Alembic async migration environment for EKOS.

Uses asyncpg driver via SQLAlchemy 2.x async engine.
Imports all ORM models so Alembic can generate migrations automatically.
"""
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Import the declarative base that all our models inherit from
from database.engine import Base

# Import ALL ORM models so Alembic detects them in metadata
import database.models  # noqa: F401 — registers models against Base.metadata

# Alembic config object — provides .ini file values
config = context.config

# Configure Python logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate
target_metadata = Base.metadata


def get_url() -> str:
    """
    Pull the database URL from environment / config.
    Converts postgresql:// → postgresql+asyncpg:// for the async engine.
    """
    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from config.manager import get_config
    url = get_config().db.database_url
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    return url


def run_migrations_offline() -> None:
    """Run migrations in offline mode (no live DB connection)."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations against live DB using asyncpg."""
    config.set_main_option("sqlalchemy.url", get_url())

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
