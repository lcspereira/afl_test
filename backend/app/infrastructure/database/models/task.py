"""Modelo ORM de tarefas."""

from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import DateTime, ForeignKey, String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base
from app.domain.task import Status

class TaskRecord(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    data_criacao: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.PENDING, nullable=False)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)