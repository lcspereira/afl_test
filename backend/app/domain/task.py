"""Definição da entidade de tarefa do domínio."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

class TaskStatus(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()

@dataclass
class Task:
    id: int
    titulo: str
    descricao: str
    status: TaskStatus
    id_usuario: int
    data_criacao: datetime