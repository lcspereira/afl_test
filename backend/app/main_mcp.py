"""Servidor MCP principal para gerenciamento de tarefas."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastmcp import FastMCP

from app.core.config import get_settings
from app.infrastructure.database.session import (
    create_async_db_engine,
    create_async_session_factory,
    init_database,
)
from app.interfaces.mcp.auth import ExistingAccessTokenVerifier
from app.interfaces.mcp.tools import register_tools

settings = get_settings()
engine = create_async_db_engine(settings.database_url)
session_factory = create_async_session_factory(engine)


@asynccontextmanager
async def lifespan(_: FastMCP) -> AsyncGenerator[dict[str, object], None]:
    await init_database(engine)
    try:
        yield {}
    finally:
        await engine.dispose()


mcp = FastMCP(
    name=settings.app_name,
    auth=ExistingAccessTokenVerifier(settings, session_factory),
    lifespan=lifespan,
)
register_tools(mcp, session_factory)

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host=settings.mcp_host,
        port=settings.mcp_port,
    )
