"""Rotas de usuário autenticado."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.domain.user import User
from app.interfaces.api.dependencies import get_current_user
from app.interfaces.api.schemas.auth import UserResponse

router = APIRouter(prefix="/users", tags=["usuários"])


@router.get("/me", response_model=UserResponse)
async def read_current_user(
    user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
    )
