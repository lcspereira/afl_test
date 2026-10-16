"""Entidade de usuário do domínio."""

from dataclasses import dataclass


@dataclass
class User:
    """Usuário autenticável da aplicação."""

    id: int | None
    username: str
    email: str
    password_hash: str
    is_active: bool = True
