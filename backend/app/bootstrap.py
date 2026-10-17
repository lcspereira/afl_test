"""Helpers de composição compartilhados de serviços da aplicação."""

from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.auth_service import AuthService
from app.application.services.task_service import TaskService
from app.core.config import Settings
from app.infrastructure.database.repositories.refresh_token import (
    SqlAlchemyRefreshTokenRepository,
)
from app.infrastructure.database.repositories.task import (
    SqlAlchemyTaskRepository,
)
from app.infrastructure.database.repositories.user import (
    SqlAlchemyUserRepository,
)
from app.infrastructure.security import Argon2PasswordHasher, JwtTokenService


@lru_cache
def get_password_hasher() -> Argon2PasswordHasher:
    """Share the password hasher and its dummy hash between requests."""
    return Argon2PasswordHasher()


def build_auth_service(
    session: AsyncSession,
    settings: Settings,
) -> AuthService:
    """Compose the authentication service for an existing database session."""
    return AuthService(
        users=SqlAlchemyUserRepository(session),
        refresh_tokens=SqlAlchemyRefreshTokenRepository(session),
        password_hasher=get_password_hasher(),
        token_service=JwtTokenService(settings),
    )


def build_task_service(session: AsyncSession) -> TaskService:
    """Compose the task service for an existing database session."""
    return TaskService(SqlAlchemyTaskRepository(session))
