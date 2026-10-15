"""Portas: contratos que a aplicação exige da infraestrutura."""

from typing import Protocol


class DatabaseProbe(Protocol):
    """Verifica se o banco de dados está acessível."""

    def is_available(self) -> bool:
        """Retorna `True` quando o banco responde corretamente."""
