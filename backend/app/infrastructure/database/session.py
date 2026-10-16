"""Async engine, session factory, and database initialization."""

from pathlib import Path
from typing import Any

from sqlalchemy import event
from sqlalchemy.engine import URL, make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from app.infrastructure.database import models  # noqa: F401
from app.infrastructure.database.base import Base


def _enable_sqlite_foreign_keys(dbapi_connection: Any, _: Any) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def _async_database_url(database_url: str) -> URL:
    url = make_url(database_url)
    if (
        url.get_backend_name() == "sqlite"
        and url.drivername != "sqlite+aiosqlite"
    ):
        url = url.set(drivername="sqlite+aiosqlite")
    return url


def create_async_db_engine(database_url: str) -> AsyncEngine:
    """Create an async SQLAlchemy engine from the configured URL."""
    url = make_url(_async_database_url(database_url))
    if url.get_backend_name() == "sqlite":
        connect_args = {"check_same_thread": False}
        if url.database in (None, ":memory:"):
            engine = create_async_engine(
                url,
                connect_args=connect_args,
                poolclass=StaticPool,
            )
        else:
            engine = create_async_engine(url, connect_args=connect_args)
        event.listen(
            engine.sync_engine,
            "connect",
            _enable_sqlite_foreign_keys,
        )
        return engine
    return create_async_engine(url)


def create_async_session_factory(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """Create an async session factory bound to the given engine."""
    return async_sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )


async def init_database(engine: AsyncEngine) -> None:
    """Create the SQLite data directory and initialize mapped tables."""
    database_file = engine.url.database
    if engine.url.get_backend_name() == "sqlite" and database_file not in (
        None,
        ":memory:",
    ):
        Path(database_file).parent.mkdir(parents=True, exist_ok=True)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
