"""Exceções da camada de domínio."""


class DomainError(Exception):
    """Erro base para violações de regras de negócio."""


class EntityNotFoundError(DomainError):
    """Indica que a entidade solicitada não existe."""

    def __init__(self, entity_name: str, entity_id: object) -> None:
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(
            f"{entity_name} com id '{entity_id}' não foi encontrado."
        )
