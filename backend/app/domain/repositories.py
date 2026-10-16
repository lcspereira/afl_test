"""Contratos de persistência definidos pelo domínio."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Protocol
from app.domain.task import Task

from app.domain.user import User


class Repository[EntityT](ABC):
    """Contrato genérico de repositório para uma entidade do domínio."""

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> EntityT | None:
        """Retorna a entidade pelo identificador ou `None` se não existir."""

    @abstractmethod
    async def list_all(self) -> list[EntityT]:
        """Retorna todas as entidades persistidas."""

    @abstractmethod
    async def add(self, entity: EntityT) -> None:
        """Registra a entidade para persistência."""

    @abstractmethod
    async def remove(self, entity: EntityT) -> None:
        """Marca a entidade para remoção."""


class UserRepository(Protocol):
    """Contrato de persistência específico para usuários."""

    async def get_by_id(self, user_id: int) -> User | None:
        """Retorna um usuário pelo identificador."""

    async def get_by_email(self, email: str) -> User | None:
        """Retorna um usuário pelo e-mail normalizado."""

    async def get_by_username(self, username: str) -> User | None:
        """Retorna um usuário pelo nome normalizado."""

    async def add(self, user: User) -> User:
        """Persiste e retorna um usuário recém-criado."""


class RefreshTokenRepository(Protocol):
    """Contrato para persistência e rotação de refresh tokens."""

    async def add(
        self,
        token_id: str,
        user_id: int,
        expires_at: datetime,
    ) -> None:
        """Registra um refresh token recém-emitido."""

    async def rotate(
        self,
        old_token_id: str,
        user_id: int,
        new_token_id: str,
        new_expires_at: datetime,
        now: datetime,
    ) -> bool:
        """Consome o token antigo e grava seu substituto atomicamente."""

    async def revoke_by_user(self, user_id: int) -> None:
        """Revoga todos os refresh tokens de um usuário."""


class TaskRepository(Protocol):
    """Contrato de persistência específico para tarefas."""

    async def get_by_id(self, task_id: int) -> Task | None:
        """Retorna uma tarefa pelo identificador."""

    async def list_by_user_id(self, user_id: int) -> list[Task]:
        """Retorna todas as tarefas associadas a um usuário específico."""

    async def add(self, task: Task) -> Task:
        """Persiste e retorna uma tarefa recém-criada."""

    async def remove(self, task: Task) -> None:
        """Marca a tarefa para remoção."""

    async def update(self, task: Task) -> Task:
        """Atualiza e retorna a tarefa persistida."""