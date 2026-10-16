"""Serviço de verificação de saúde da aplicação."""

from dataclasses import dataclass

from app.application.ports import DatabaseProbe


@dataclass(frozen=True)
class HealthReport:
    """Resultado de uma verificação de saúde."""

    database_available: bool

    @property
    def status(self) -> str:
        """Estado geral do sistema: `ok` ou `degradado`."""
        return "ok" if self.database_available else "degradado"

    @property
    def database_status(self) -> str:
        """Estado do banco de dados: `disponivel` ou `indisponivel`."""
        return "disponivel" if self.database_available else "indisponivel"


class HealthService:
    """Regras de negócio relacionadas à saúde do sistema."""

    def __init__(self, database_probe: DatabaseProbe) -> None:
        self._database_probe = database_probe

    async def check(self) -> HealthReport:
        """Executa as verificações e consolida o resultado."""
        return HealthReport(
            database_available=await self._database_probe.is_available(),
        )
