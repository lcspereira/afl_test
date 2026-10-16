"""Implementações de hashing de senha e tokens JWT."""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import anyio
import jwt
from pwdlib import PasswordHash

from app.core.config import Settings
from app.domain.exceptions import (
    InvalidAccessTokenError,
    InvalidRefreshTokenError,
)
from app.domain.tokens import IssuedRefreshToken, RefreshTokenClaims

JWT_ALGORITHM = "HS256"


class Argon2PasswordHasher:
    """Gera e verifica hashes de senha Argon2."""

    def __init__(self) -> None:
        self._password_hash = PasswordHash.recommended()
        self._dummy_hash = self._password_hash.hash(
            "senha-inexistente-para-tempo-constante"
        )

    async def hash_password(self, password: str) -> str:
        return await anyio.to_thread.run_sync(
            self._password_hash.hash,
            password,
        )

    async def verify_password(
        self,
        password: str,
        password_hash: str | None,
    ) -> bool:
        hash_to_verify = password_hash or self._dummy_hash
        verified = await anyio.to_thread.run_sync(
            self._password_hash.verify,
            password,
            hash_to_verify,
        )
        return password_hash is not None and verified


class JwtTokenService:
    """Assina e valida tokens de acesso JWT."""

    def __init__(self, settings: Settings) -> None:
        self._secret_key = settings.jwt_secret_key.get_secret_value()
        self._expires_in = timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )
        self._refresh_expires_in = timedelta(
            days=settings.jwt_refresh_token_expire_days
        )

    def create_access_token(self, user_id: int) -> str:
        issued_at = datetime.now(UTC)
        return jwt.encode(
            {
                "sub": str(user_id),
                "iat": issued_at,
                "exp": issued_at + self._expires_in,
                "jti": uuid4().hex,
                "token_type": "access",
            },
            self._secret_key,
            algorithm=JWT_ALGORITHM,
        )

    def read_access_token(self, token: str) -> int:
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[JWT_ALGORITHM],
                options={
                    "require": ["exp", "iat", "sub", "token_type"],
                },
            )
        except jwt.InvalidTokenError as exc:
            raise InvalidAccessTokenError() from exc

        subject = payload.get("sub")
        if (
            payload.get("token_type") != "access"
            or not isinstance(subject, str)
            or not subject.isdecimal()
        ):
            raise InvalidAccessTokenError()
        return int(subject)

    def create_refresh_token(self, user_id: int) -> IssuedRefreshToken:
        issued_at = datetime.now(UTC)
        expires_at = issued_at + self._refresh_expires_in
        token_id = uuid4().hex
        encoded_token = jwt.encode(
            {
                "sub": str(user_id),
                "iat": issued_at,
                "exp": expires_at,
                "jti": token_id,
                "token_type": "refresh",
            },
            self._secret_key,
            algorithm=JWT_ALGORITHM,
        )
        return IssuedRefreshToken(
            encoded_token=encoded_token,
            token_id=token_id,
            user_id=user_id,
            expires_at=expires_at,
        )

    def read_refresh_token(self, token: str) -> RefreshTokenClaims:
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[JWT_ALGORITHM],
                options={
                    "require": [
                        "exp",
                        "iat",
                        "jti",
                        "sub",
                        "token_type",
                    ],
                },
            )
        except jwt.InvalidTokenError as exc:
            raise InvalidRefreshTokenError() from exc

        subject = payload.get("sub")
        token_id = payload.get("jti")
        if (
            payload.get("token_type") != "refresh"
            or not isinstance(subject, str)
            or not subject.isdecimal()
            or not isinstance(token_id, str)
            or len(token_id) != 32
        ):
            raise InvalidRefreshTokenError()
        return RefreshTokenClaims(
            token_id=token_id,
            user_id=int(subject),
        )
