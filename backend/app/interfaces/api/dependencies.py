"""Injeção de dependências dos endpoints (composição das camadas)."""

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from app.application.services.auth_service import AuthService
from app.application.services.health_service import HealthService
from app.application.services.task_service import TaskService
from app.bootstrap import (
    build_auth_service,
    build_task_service,
)
from app.domain.exceptions import InvalidAccessTokenError
from app.domain.user import User
from app.infrastructure.database.probe import SqlAlchemyDatabaseProbe

_bearer_scheme = HTTPBearer(auto_error=False)


def get_session_factory(
    request: Request,
) -> async_sessionmaker[AsyncSession]:
    """Obtém a fábrica de sessões armazenada no estado da aplicação."""
    return request.app.state.session_factory


async def get_db_session(
    session_factory: Annotated[
        async_sessionmaker[AsyncSession],
        Depends(get_session_factory),
    ],
) -> AsyncIterator[AsyncSession]:
    """Entrega uma sessão por requisição e a fecha ao final."""
    async with session_factory() as session:
        yield session


def get_health_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> HealthService:
    """Monta o serviço de saúde com o probe baseado na sessão atual."""
    return HealthService(SqlAlchemyDatabaseProbe(session))


def get_task_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TaskService:
    """Monta o serviço de tarefas com o repositório da sessão atual."""
    return build_task_service(session)


def get_auth_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    request: Request,
) -> AuthService:
    """Monta o serviço de autenticação com dependências concretas."""
    return build_auth_service(session, request.app.state.settings)


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(_bearer_scheme),
    ],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    """Valida o bearer token e retorna o usuário ativo correspondente."""
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Autenticação necessária.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise unauthorized

    try:
        user = await service.user_from_access_token(credentials.credentials)
    except InvalidAccessTokenError as exc:
        raise unauthorized from exc
    if user is None:
        raise unauthorized
    return user
