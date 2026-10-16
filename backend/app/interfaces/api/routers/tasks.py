"""Rotas públicas para gerenciamento de tarefas."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.services.task_service import TaskService
from app.domain.task import Task
from app.domain.user import User
from app.infrastructure.database.models.task import TaskRecord
from app.interfaces.api.dependencies import get_current_user, get_task_service
from app.interfaces.api.schemas.task import (
    TaskCreateSchema,
    TaskResponseSchema,
    TaskUpdateSchema,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _task_response(task: Task | TaskRecord) -> TaskResponseSchema:
    return TaskResponseSchema(
        id=task.id,
        titulo=task.titulo,
        descricao=task.descricao,
        status=task.status,
        id_usuario=task.id_usuario,
        data_criacao=task.data_criacao,
    )


@router.post("/", response_model=TaskResponseSchema)
async def create_task(
    task: TaskCreateSchema,
    service: Annotated[TaskService, Depends(get_task_service)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Cria uma nova tarefa para o usuário atual."""
    task = await service.create_task(
        titulo=task.titulo,
        descricao=task.descricao,
        status=task.status,
        id_usuario=current_user.id,
    )
    return _task_response(task)


@router.put("/{task_id}", response_model=TaskResponseSchema)
async def update_task(
    task_id: int,
    task: TaskUpdateSchema,
    service: Annotated[TaskService, Depends(get_task_service)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Atualiza uma tarefa existente do usuário atual."""
    task = await service.update_task(
        task_id=task_id,
        titulo=task.titulo,
        descricao=task.descricao,
        status=task.status,
        id_usuario=current_user.id,
    )
    return _task_response(task)


@router.delete("/{task_id}", response_model=TaskResponseSchema)
async def delete_task(
    task_id: int,
    service: Annotated[TaskService, Depends(get_task_service)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Exclui uma tarefa existente do usuário atual."""
    task = await service.delete_task(
        task_id=task_id,
        id_usuario=current_user.id,
    )
    return _task_response(task)


@router.get("/", response_model=list[TaskResponseSchema])
async def list_tasks(
    service: Annotated[TaskService, Depends(get_task_service)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Lista todas as tarefas do usuário atual."""
    tasks = await service.list_tasks_by_user(id_usuario=current_user.id)
    return [_task_response(task) for task in tasks]


@router.get("/{task_id}", response_model=TaskResponseSchema)
async def get_task(
    task_id: int,
    service: Annotated[TaskService, Depends(get_task_service)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Obtém uma tarefa específica do usuário atual."""
    task = await service.get_task(
        task_id=task_id,
        id_usuario=current_user.id,
    )
    return _task_response(task)
