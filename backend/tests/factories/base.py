"""Fábrica base para modelos SQLAlchemy usando factory_boy."""

from collections.abc import Iterator

from factory.alchemy import SESSION_PERSISTENCE_FLUSH, SQLAlchemyModelFactory
from sqlalchemy.orm import Session


class BaseFactory(SQLAlchemyModelFactory):
    """Base das fábricas de modelos; a sessão é injetada pelo conftest."""

    class Meta:
        abstract = True
        sqlalchemy_session_persistence = SESSION_PERSISTENCE_FLUSH


def _iter_factories(root: type[BaseFactory]) -> Iterator[type[BaseFactory]]:
    yield root
    for subclass in root.__subclasses__():
        yield from _iter_factories(subclass)


def bind_session(session: Session) -> None:
    """Associa a sessão informada a todas as fábricas registradas."""
    for factory_class in _iter_factories(BaseFactory):
        factory_class._meta.sqlalchemy_session = session
