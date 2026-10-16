"""Implementação do probe de saúde do banco de dados."""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyDatabaseProbe:
    """Verifica a disponibilidade do banco executando uma consulta simples."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def is_available(self) -> bool:
        """Retorna `True` quando a consulta de teste é bem-sucedida."""
        try:
            await self._session.execute(text("SELECT 1"))
        except SQLAlchemyError:
            return False
        return True
