"""Repositório genérico baseado em SQLAlchemy."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories import Repository
from app.infrastructure.database.base import Base


class SqlAlchemyRepository[ModelT: Base](Repository[ModelT]):
    """Implementa o contrato de repositório usando uma sessão SQLAlchemy.

    Subclasses definem `model` com a classe ORM que será persistida.
    """

    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: int) -> ModelT | None:
        return await self._session.get(self.model, entity_id)

    async def list_all(self) -> list[ModelT]:
        records = await self._session.scalars(select(self.model))
        return list(records.all())

    async def add(self, entity: ModelT) -> None:
        self._session.add(entity)

    async def remove(self, entity: ModelT) -> None:
        await self._session.delete(entity)
