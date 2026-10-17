"""Task tools registered on the authenticated MCP server."""

from enum import Enum

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_access_token
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.bootstrap import build_task_service
from app.infrastructure.database.models.task import Status, TaskRecord

TaskPayload = dict[str, int | str]


def _current_user_id() -> int:
    access_token = get_access_token()
    user_id = access_token.claims.get("user_id") if access_token else None
    if not isinstance(user_id, int):
        raise ToolError("An authenticated user is required.")
    return user_id


def _task_payload(task: TaskRecord) -> TaskPayload:
    status = (
        task.status.value if isinstance(task.status, Enum) else task.status
    )
    return {
        "id": task.id,
        "titulo": task.titulo,
        "descricao": task.descricao,
        "status": str(status),
        "data_criacao": task.data_criacao.isoformat(),
    }


def register_tools(
    mcp: FastMCP,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """Register task tools that scope every operation to the token owner."""

    @mcp.tool
    async def list_tasks() -> list[TaskPayload]:
        """List tasks owned by the authenticated user."""
        user_id = _current_user_id()
        async with session_factory() as session:
            tasks = await build_task_service(session).list_tasks_by_user(
                id_usuario=user_id,
            )
        return [_task_payload(task) for task in tasks]

    @mcp.tool
    async def get_task(task_id: int) -> TaskPayload:
        """Get one task owned by the authenticated user."""
        user_id = _current_user_id()
        async with session_factory() as session:
            task = await build_task_service(session).get_task(
                task_id=task_id,
                id_usuario=user_id,
            )
        return _task_payload(task)

    @mcp.tool
    async def create_task(
        title: str,
        description: str,
        status: Status = Status.PENDING,
    ) -> TaskPayload:
        """Create a task for the authenticated user."""
        user_id = _current_user_id()
        async with session_factory() as session:
            task = await build_task_service(session).create_task(
                titulo=title,
                descricao=description,
                status=status,
                id_usuario=user_id,
            )
        return _task_payload(task)

    @mcp.tool
    async def update_task(
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        status: Status | None = None,
    ) -> TaskPayload:
        """Update a task owned by the authenticated user."""
        user_id = _current_user_id()
        async with session_factory() as session:
            task = await build_task_service(session).update_task(
                task_id=task_id,
                titulo=title,
                descricao=description,
                status=status,
                id_usuario=user_id,
            )
        return _task_payload(task)

    @mcp.tool
    async def delete_task(task_id: int) -> TaskPayload:
        """Delete a task owned by the authenticated user."""
        user_id = _current_user_id()
        async with session_factory() as session:
            task = await build_task_service(session).delete_task(
                task_id=task_id,
                id_usuario=user_id,
            )
        return _task_payload(task)
