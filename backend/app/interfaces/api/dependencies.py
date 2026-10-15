"""Injeção de dependências dos endpoints (composição das camadas)."""

from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session, sessionmaker

from app.application.services.health_service import HealthService
from app.infrastructure.database.probe import SqlAlchemyDatabaseProbe


def get_session_factory(request: Request) -> sessionmaker[Session]:
    """Obtém a fábrica de sessões armazenada no estado da aplicação."""
    return request.app.state.session_factory


def get_db_session(
    session_factory: Annotated[
        sessionmaker[Session], Depends(get_session_factory)
    ],
) -> Iterator[Session]:
    """Entrega uma sessão por requisição e a fecha ao final."""
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


def get_health_service(
    session: Annotated[Session, Depends(get_db_session)],
) -> HealthService:
    """Monta o serviço de saúde com o probe baseado na sessão atual."""
    return HealthService(SqlAlchemyDatabaseProbe(session))
