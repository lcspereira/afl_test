"""Traduz exceções de domínio em respostas HTTP."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    DomainError,
    EntityNotFoundError,
    InvalidAccessTokenError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    UserAlreadyExistsError,
)


def register_exception_handlers(app: FastAPI) -> None:
    """Registra os handlers de exceções de domínio na aplicação."""

    @app.exception_handler(EntityNotFoundError)
    async def handle_not_found(
        _: Request,
        exc: EntityNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(UserAlreadyExistsError)
    async def handle_user_already_exists(
        _: Request,
        exc: UserAlreadyExistsError,
    ) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(InvalidCredentialsError)
    async def handle_invalid_credentials(
        _: Request,
        exc: InvalidCredentialsError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(InvalidAccessTokenError)
    async def handle_invalid_access_token(
        _: Request,
        exc: InvalidAccessTokenError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(InvalidRefreshTokenError)
    async def handle_invalid_refresh_token(
        _: Request,
        exc: InvalidRefreshTokenError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(DomainError)
    async def handle_domain_error(
        _: Request,
        exc: DomainError,
    ) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": str(exc)})
