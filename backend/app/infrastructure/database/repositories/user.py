"""Repositório SQLAlchemy de usuários."""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions import UserAlreadyExistsError
from app.domain.repositories import UserRepository
from app.domain.user import User
from app.infrastructure.database.models.user import UserRecord


class SqlAlchemyUserRepository(UserRepository):
    """Adapta operações de usuário para SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: int) -> User | None:
        record = await self._session.get(UserRecord, user_id)
        return self._to_entity(record) if record is not None else None

    async def get_by_email(self, email: str) -> User | None:
        record = await self._session.scalar(
            select(UserRecord).where(UserRecord.email == email)
        )
        return self._to_entity(record) if record is not None else None

    async def get_by_username(self, username: str) -> User | None:
        record = await self._session.scalar(
            select(UserRecord).where(UserRecord.username == username)
        )
        return self._to_entity(record) if record is not None else None

    async def add(self, user: User) -> User:
        record = UserRecord(
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            is_active=user.is_active,
        )
        self._session.add(record)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            raise UserAlreadyExistsError() from exc
        await self._session.refresh(record)
        return self._to_entity(record)

    @staticmethod
    def _to_entity(record: UserRecord) -> User:
        return User(
            id=record.id,
            username=record.username,
            email=record.email,
            password_hash=record.password_hash,
            is_active=record.is_active,
        )
