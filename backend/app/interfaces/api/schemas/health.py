"""Schemas da rota de saúde."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Resposta do endpoint de saúde."""

    status: str
    database: str
