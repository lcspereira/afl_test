"""Engine, fábrica de sessões e inicialização do banco de dados."""

from pathlib import Path
from typing import Any

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.database import models  # noqa: F401
from app.infrastructure.database.base import Base


def _enable_sqlite_foreign_keys(dbapi_connection: Any, _: Any) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_db_engine(database_url: str) -> Engine:
    """Cria a engine do SQLAlchemy a partir da URL configurada."""
    is_sqlite = database_url.startswith("sqlite")
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False} if is_sqlite else {},
    )
    if is_sqlite:
        event.listen(engine, "connect", _enable_sqlite_foreign_keys)
    return engine


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Cria a fábrica de sessões vinculada à engine informada."""
    return sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )


def init_database(engine: Engine) -> None:
    """Cria o diretório do arquivo SQLite (se necessário) e as tabelas."""
    database_file = engine.url.database
    if engine.url.get_backend_name() == "sqlite" and database_file not in (
        None,
        ":memory:",
    ):
        Path(database_file).parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(engine)
