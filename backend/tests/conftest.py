"""Fixtures compartilhadas pelos testes.

Este arquivo contém apenas fixtures. Os testes são escritos pela equipe.
"""

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.infrastructure.database.session import (
    create_db_engine,
    create_session_factory,
    init_database,
)
from app.main import create_app
from tests.factories.base import bind_session


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    """Configurações isoladas, com banco SQLite temporário por teste."""
    return Settings(
        _env_file=None,
        environment="test",
        debug=True,
        database_url=f"sqlite:///:memory:",
    )


@pytest.fixture
def db_session(settings: Settings) -> Iterator[Session]:
    """Sessão SQLAlchemy apontando para o banco temporário."""
    engine = create_db_engine(settings.database_url)
    init_database(engine)
    session = create_session_factory(engine)()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture(autouse=True)
def _bind_factories_session(db_session: Session) -> None:
    """Vincula as fábricas factory_boy à sessão de teste."""
    bind_session(db_session)


@pytest.fixture
def client(settings: Settings) -> Iterator[TestClient]:
    """Cliente HTTP da aplicação com ciclo de vida (lifespan) executado."""
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client
