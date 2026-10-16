"""Fixtures compartilhadas pelos testes."""

from collections.abc import AsyncIterator, Iterator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.infrastructure.database.session import (
    create_async_db_engine,
    create_async_session_factory,
    init_database,
)
from app.main import create_app


@pytest.fixture
def settings() -> Settings:
    """Configurações isoladas, com banco SQLite temporário por teste."""
    return Settings(
        _env_file=None,
        environment="test",
        debug=True,
        database_url="sqlite:///:memory:",
    )


@pytest_asyncio.fixture
async def db_session(settings: Settings) -> AsyncIterator[AsyncSession]:
    """Sessão assíncrona SQLAlchemy apontando para banco temporário."""
    engine = create_async_db_engine(settings.database_url)
    await init_database(engine)
    try:
        async with create_async_session_factory(engine)() as session:
            yield session
    finally:
        await engine.dispose()


@pytest.fixture
def client(settings: Settings) -> Iterator[TestClient]:
    """Cliente HTTP da aplicação com ciclo de vida (lifespan) executado."""
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client
