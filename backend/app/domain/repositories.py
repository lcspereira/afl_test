"""Contratos de persistência definidos pelo domínio."""

from abc import ABC, abstractmethod


class Repository[EntityT](ABC):
    """Contrato genérico de repositório para uma entidade do domínio."""

    @abstractmethod
    def get_by_id(self, entity_id: int) -> EntityT | None:
        """Retorna a entidade pelo identificador ou `None` se não existir."""

    @abstractmethod
    def list_all(self) -> list[EntityT]:
        """Retorna todas as entidades persistidas."""

    @abstractmethod
    def add(self, entity: EntityT) -> None:
        """Registra a entidade para persistência."""

    @abstractmethod
    def remove(self, entity: EntityT) -> None:
        """Marca a entidade para remoção."""
