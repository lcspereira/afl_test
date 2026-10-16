"""Fábrica base para modelos SQLAlchemy usados com sessões assíncronas."""

import factory
from sqlalchemy.ext.asyncio import AsyncSession


class BaseFactory(factory.Factory):
    """Cria objetos ORM e oferece persistência em sessão assíncrona."""

    class Meta:
        abstract = True

    @classmethod
    async def create_async(
        cls,
        session: AsyncSession,
        **kwargs: object,
    ) -> object:
        instance = cls.build(**kwargs)
        session.add(instance)
        await session.flush()
        return instance
