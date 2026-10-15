"""Implementação do probe de saúde do banco de dados."""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


class SqlAlchemyDatabaseProbe:
    """Verifica a disponibilidade do banco executando uma consulta simples."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def is_available(self) -> bool:
        """Retorna `True` quando a consulta de teste é bem-sucedida."""
        try:
            self._session.execute(text("SELECT 1"))
        except SQLAlchemyError:
            return False
        return True
