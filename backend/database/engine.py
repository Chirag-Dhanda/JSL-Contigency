"""
database/engine.py
─────────────────────────────────────────────────────────────────
Enterprise async database engine.
Provides the SQLAlchemy async engine and session factory.
All database operations must go through get_async_session().
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
import logging
from contextlib import asynccontextmanager

logger = logging.getLogger("Database")


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""
    pass


# Module-level engine — initialised by DatabaseModule.initialize()
_engine = None
_session_factory = None


def init_engine(database_url: str, pool_size: int = 5, max_overflow: int = 10) -> None:
    """
    Initialise the async engine. Called once during application startup.
    database_url must use the postgresql+asyncpg:// scheme.
    """
    global _engine, _session_factory

    # Ensure asyncpg driver scheme
    url = database_url
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)

    _engine = create_async_engine(
        url,
        pool_size=pool_size,
        max_overflow=max_overflow,
        echo=False,
        future=True,
    )

    _session_factory = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    logger.info("Async database engine initialised.")


def get_engine():
    if _engine is None:
        raise RuntimeError("Database engine has not been initialised. Call init_engine() first.")
    return _engine


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency and generic async context for DB sessions."""
    if _session_factory is None:
        raise RuntimeError("Database session factory has not been initialised.")
    async with _session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def close_engine() -> None:
    """Dispose the engine — called on application shutdown."""
    global _engine
    if _engine:
        await _engine.dispose()
        _engine = None
        logger.info("Database engine disposed.")
