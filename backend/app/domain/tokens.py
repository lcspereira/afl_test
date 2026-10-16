"""Value objects usados na emissão e validação de tokens."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class IssuedRefreshToken:
    """Token de atualização emitido e seus dados de persistência."""

    encoded_token: str
    token_id: str
    user_id: int
    expires_at: datetime


@dataclass(frozen=True)
class RefreshTokenClaims:
    """Claims validados de um token de atualização."""

    token_id: str
    user_id: int
