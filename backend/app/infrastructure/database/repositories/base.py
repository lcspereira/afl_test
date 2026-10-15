"""Repositório genérico baseado em SQLAlchemy."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.repositories import Repository
from app.infrastructure.database.base import Base


class SqlAlchemyRepository[ModelT: Base](Repository[ModelT]):
    """Implementa o contrato de repositório usando uma sessão SQLAlchemy.

    Subclasses definem `model` com a classe ORM que será persistida.
    """

    model: type[ModelT]

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: int) -> ModelT | None:
        return self._session.get(self.model, entity_id)

    def list_all(self) -> list[ModelT]:
        return list(self._session.scalars(select(self.model)).all())

    def add(self, entity: ModelT) -> None:
        self._session.add(entity)

    def remove(self, entity: ModelT) -> None:
        self._session.delete(entity)
