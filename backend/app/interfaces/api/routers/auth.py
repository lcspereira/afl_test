"""Rotas públicas de cadastro e emissão de tokens."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status

from app.application.services.auth_service import AuthService
from app.interfaces.api.dependencies import get_auth_service
from app.interfaces.api.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["autenticação"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: UserCreate,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserResponse:
    user = await service.register(
        username=payload.username,
        email=str(payload.email),
        password=payload.password,
    )
    return UserResponse.model_validate(user)


@router.post("/token", response_model=TokenResponse)
async def create_token(
    payload: LoginRequest,
    request: Request,
    response: Response,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> TokenResponse:
    _, access_token, refresh_token = await service.authenticate(
        str(payload.email),
        payload.password,
    )
    return _token_response(request, response, access_token, refresh_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    payload: RefreshRequest,
    request: Request,
    response: Response,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> TokenResponse:
    _, access_token, refresh_token = await service.refresh(
        payload.refresh_token
    )
    return _token_response(request, response, access_token, refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    response: Response,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> None:
    token = request.headers.get("Authorization")
    if token is not None and token.startswith("Bearer "):
        token = token[len("Bearer ") :]
    else:
        token = request.cookies.get("access_token")
    if token:
        await service.logout(token)
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")


def _token_response(
    request: Request,
    response: Response,
    access_token: str,
    refresh_token: str,
) -> TokenResponse:
    settings = request.app.state.settings
    access_expires_in = settings.jwt_access_token_expire_minutes * 60
    refresh_expires_in = settings.jwt_refresh_token_expire_days * 24 * 60 * 60
    secure = request.url.scheme == "https"
    response.set_cookie(
        "access_token",
        access_token,
        max_age=access_expires_in,
        httponly=True,
        secure=secure,
        samesite="lax",
        path="/",
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        max_age=refresh_expires_in,
        httponly=True,
        secure=secure,
        samesite="lax",
        path="/",
    )
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_expires_in,
        refresh_expires_in=refresh_expires_in,
    )
