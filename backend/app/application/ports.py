"""Portas: contratos que a aplicação exige da infraestrutura."""

from typing import Protocol

from app.domain.tokens import IssuedRefreshToken, RefreshTokenClaims


class DatabaseProbe(Protocol):
    """Verifica se o banco de dados está acessível."""

    async def is_available(self) -> bool:
        """Retorna `True` quando o banco responde corretamente."""


class PasswordHasher(Protocol):
    """Contrato para geração e verificação segura de hashes de senha."""

    async def hash_password(self, password: str) -> str:
        """Gera um hash não reversível para a senha."""

    async def verify_password(
        self,
        password: str,
        password_hash: str | None,
    ) -> bool:
        """Compara uma senha com o hash armazenado."""


class TokenService(Protocol):
    """Contrato de emissão e leitura de tokens de acesso."""

    def create_access_token(self, user_id: int) -> str:
        """Emite um token de acesso para o usuário."""

    def read_access_token(self, token: str) -> int:
        """Valida o token e retorna o identificador do usuário."""

    def create_refresh_token(self, user_id: int) -> IssuedRefreshToken:
        """Emite um refresh token e seus dados de persistência."""

    def read_refresh_token(self, token: str) -> RefreshTokenClaims:
        """Valida um refresh token e retorna suas claims."""


class TaskCrud(Protocol):
    """Contrato para operações de persistência de tarefas."""

    async def create_task(self, titulo: str, descricao: str, id_usuario: int) -> int:
        """Cria uma nova tarefa e retorna seu identificador."""

    async def get_task(self, task_id: int, id_usuario: int) -> dict:
        """Retorna os dados de uma tarefa pelo seu identificador."""

    async def update_task(self, task_id: int, titulo: str, descricao: str, status: str, id_usuario: int) -> None:
        """Atualiza os dados de uma tarefa existente."""

    async def delete_task(self, task_id: int, id_usuario: int) -> None:
        """Remove uma tarefa pelo seu identificador."""

    async def list_tasks(self, id_usuario: int) -> list[dict]:
        """Retorna a lista de todas as tarefas de um usuário específico."""

