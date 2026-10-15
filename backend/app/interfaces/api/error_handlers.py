"""Traduz exceções de domínio em respostas HTTP."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import DomainError, EntityNotFoundError


def register_exception_handlers(app: FastAPI) -> None:
    """Registra os handlers de exceções de domínio na aplicação."""

    @app.exception_handler(EntityNotFoundError)
    def handle_not_found(_: Request, exc: EntityNotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(DomainError)
    def handle_domain_error(_: Request, exc: DomainError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": str(exc)})
