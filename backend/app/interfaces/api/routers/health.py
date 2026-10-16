"""Rota de verificação de saúde da aplicação."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.services.health_service import HealthService
from app.interfaces.api.dependencies import get_health_service
from app.interfaces.api.schemas.health import HealthResponse

router = APIRouter(tags=["saúde"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Verifica a saúde da aplicação",
)
async def read_health(
    service: Annotated[HealthService, Depends(get_health_service)],
) -> HealthResponse:
    """Informa o estado geral da aplicação e do banco de dados."""
    report = await service.check()
    return HealthResponse(
        status=report.status,
        database=report.database_status,
    )
