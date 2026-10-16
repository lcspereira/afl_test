"""Repositório SQLAlchemy para sessões de refresh token."""

from datetime import UTC, datetime

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.refresh_token import (
    RefreshTokenRecord,
)


class SqlAlchemyRefreshTokenRepository:
    """Persiste e rotaciona refresh tokens de uso único."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(
        self,
        token_id: str,
        user_id: int,
        expires_at: datetime,
    ) -> None:
        self._session.add(
            RefreshTokenRecord(
                token_id=token_id,
                user_id=user_id,
                expires_at=expires_at,
            )
        )
        await self._session.commit()

    async def rotate(
        self,
        old_token_id: str,
        user_id: int,
        new_token_id: str,
        new_expires_at: datetime,
        now: datetime,
    ) -> bool:
        result = await self._session.execute(
            update(RefreshTokenRecord)
            .where(
                RefreshTokenRecord.token_id == old_token_id,
                RefreshTokenRecord.user_id == user_id,
                RefreshTokenRecord.revoked_at.is_(None),
                RefreshTokenRecord.expires_at > now,
            )
            .values(revoked_at=now)
        )
        if result.rowcount != 1:
            await self._session.rollback()
            return False

        self._session.add(
            RefreshTokenRecord(
                token_id=new_token_id,
                user_id=user_id,
                expires_at=new_expires_at,
            )
        )
        await self._session.commit()
        return True

    async def revoke_by_user(self, user_id: int) -> None:
        await self._session.execute(
            update(RefreshTokenRecord)
            .where(
                RefreshTokenRecord.user_id == user_id,
                RefreshTokenRecord.revoked_at.is_(None),
            )
            .values(revoked_at=datetime.now(UTC))
        )
        await self._session.commit()
