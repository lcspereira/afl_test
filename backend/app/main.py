"""Fábrica da aplicação FastAPI e ponto de entrada do Uvicorn."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings, get_settings
from app.infrastructure.database.session import (
    create_async_db_engine,
    create_async_session_factory,
    init_database,
)
from app.interfaces.api.error_handlers import register_exception_handlers
from app.interfaces.api.routers.auth import router as auth_router
from app.interfaces.api.routers.health import router as health_router
from app.interfaces.api.routers.users import router as users_router
from app.interfaces.api.routers.tasks import router as tasks_router


def create_app(settings: Settings | None = None) -> FastAPI:
    """Monta a aplicação com banco de dados, middlewares e rotas."""
    settings = settings or get_settings()
    engine = create_async_db_engine(settings.database_url)
    session_factory = create_async_session_factory(engine)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        await init_database(engine)
        try:
            yield
        finally:
            await engine.dispose()

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
    app.include_router(auth_router, prefix=settings.api_prefix)
    app.include_router(health_router, prefix=settings.api_prefix)
    app.include_router(users_router, prefix=settings.api_prefix)
    app.include_router(tasks_router, prefix=settings.api_prefix)
    return app


app = create_app()
