"""Fábrica da aplicação FastAPI e ponto de entrada do Uvicorn."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings, get_settings
from app.infrastructure.database.session import (
    create_db_engine,
    create_session_factory,
    init_database,
)
from app.interfaces.api.error_handlers import register_exception_handlers
from app.interfaces.api.routers.health import router as health_router


def create_app(settings: Settings | None = None) -> FastAPI:
    """Monta a aplicação com banco de dados, middlewares e rotas."""
    settings = settings or get_settings()
    engine = create_db_engine(settings.database_url)
    session_factory = create_session_factory(engine)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        init_database(engine)
        yield
        engine.dispose()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )
    app.state.settings = settings
    app.state.session_factory = session_factory

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_exception_handlers(app)
    app.include_router(health_router, prefix=settings.api_prefix)
    return app


app = create_app()
