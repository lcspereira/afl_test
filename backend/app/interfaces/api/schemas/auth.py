"""Schemas de requisição e resposta de autenticação."""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Dados para criação de uma conta."""

    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[A-Za-z0-9_.-]+$",
    )
    email: EmailStr = Field(max_length=254)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    """Credenciais de login."""

    email: EmailStr = Field(max_length=254)
    password: str = Field(min_length=1, max_length=128)


class RefreshRequest(BaseModel):
    """Refresh token a ser rotacionado."""

    refresh_token: str = Field(min_length=1, max_length=4096)


class UserResponse(BaseModel):
    """Dados públicos do usuário autenticado."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    is_active: bool


class TokenResponse(BaseModel):
    """Par de tokens e suas durações em segundos."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_expires_in: int
