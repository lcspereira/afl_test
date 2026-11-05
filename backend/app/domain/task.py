"""Definição da entidade de tarefa do domínio."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

class Status(str, Enum):
    PENDING = "pendente"
    IN_PROGRESS = "em andamento"
    COMPLETED = "concluida"

@dataclass
class Task:
    id: int
    titulo: str
    descricao: str
    status: Status
    id_usuario: int
    data_criacao: datetime