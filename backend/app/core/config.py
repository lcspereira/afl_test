"""Configurações centrais da aplicação."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEVELOPMENT_JWT_SECRET = "development-only-secret-key-never-use-in-production"


class Settings(BaseSettings):
    """Configurações lidas de variáveis de ambiente ou do arquivo `.env`."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Aplicação"
    environment: Literal["development", "test", "production"] = "development"
    debug: bool = False
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./data/app.db"
    jwt_secret_key: SecretStr = SecretStr(DEVELOPMENT_JWT_SECRET)
    jwt_access_token_expire_minutes: int = Field(
        default=30,
        gt=0,
        le=1440,
    )
    jwt_refresh_token_expire_days: int = Field(
        default=7,
        gt=0,
        le=90,
    )
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:5173",
        ]
    )

    @model_validator(mode="after")
    def validate_jwt_secret(self) -> "Settings":
        secret = self.jwt_secret_key.get_secret_value()
        if len(secret) < 32:
            raise ValueError("JWT_SECRET_KEY must contain at least 32 chars.")
        if (
            self.environment == "production"
            and secret == DEVELOPMENT_JWT_SECRET
        ):
            raise ValueError(
                "Set a unique JWT_SECRET_KEY before production startup."
            )
        return self


@lru_cache
def get_settings() -> Settings:
    """Retorna a instância única de configurações da aplicação."""
    return Settings()
