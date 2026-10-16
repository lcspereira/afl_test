"""Schemas para criação, atualização e resposta de tarefas."""

from datetime import datetime

from pydantic import BaseModel

from app.infrastructure.database.models import Status


class TaskCreateSchema(BaseModel):
    titulo: str
    descricao: str
    status: Status


class TaskUpdateSchema(BaseModel):
    titulo: str | None = None
    descricao: str | None = None
    status: Status | None = None


class TaskResponseSchema(BaseModel):
    id: int
    titulo: str
    descricao: str
    status: Status
    id_usuario: int
    data_criacao: datetime
