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


class UserAlreadyExistsError(DomainError):
    """Indica que nome de usuário ou e-mail já estão cadastrados."""

    def __init__(self) -> None:
        super().__init__("Usuário ou e-mail já cadastrado.")


class InvalidCredentialsError(DomainError):
    """Indica credenciais inválidas ou conta desativada."""

    def __init__(self) -> None:
        super().__init__("Credenciais inválidas.")


class InvalidAccessTokenError(DomainError):
    """Indica token de acesso inválido ou expirado."""

    def __init__(self) -> None:
        super().__init__("Token de acesso inválido ou expirado.")


class InvalidRefreshTokenError(DomainError):
    """Indica token de atualização inválido, expirado ou já utilizado."""

    def __init__(self) -> None:
        super().__init__(
            "Token de atualização inválido, expirado ou já utilizado."
        )
