"""Casos de uso de cadastro e autenticação."""

from datetime import UTC, datetime

from app.application.ports import PasswordHasher, TokenService
from app.domain.exceptions import (
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    UserAlreadyExistsError,
)
from app.domain.repositories import RefreshTokenRepository, UserRepository
from app.domain.user import User


class AuthService:
    """Orquestra cadastro, login e resolução de tokens."""

    def __init__(
        self,
        users: UserRepository,
        refresh_tokens: RefreshTokenRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ) -> None:
        self._users = users
        self._refresh_tokens = refresh_tokens
        self._password_hasher = password_hasher
        self._token_service = token_service

    async def register(
        self,
        username: str,
        email: str,
        password: str,
    ) -> User:
        normalized_username = username.strip().casefold()
        normalized_email = email.strip().casefold()
        if (
            await self._users.get_by_username(normalized_username) is not None
            or await self._users.get_by_email(normalized_email) is not None
        ):
            raise UserAlreadyExistsError()

        user = User(
            id=None,
            username=normalized_username,
            email=normalized_email,
            password_hash=await self._password_hasher.hash_password(password),
        )
        return await self._users.add(user)

    async def authenticate(
        self,
        email: str,
        password: str,
    ) -> tuple[User, str, str]:
        normalized_email = email.strip().casefold()
        user = await self._users.get_by_email(normalized_email)
        password_hash = user.password_hash if user is not None else None
        if (
            not await self._password_hasher.verify_password(
                password, password_hash
            )
            or user is None
            or not user.is_active
            or user.id is None
        ):
            raise InvalidCredentialsError()

        refresh_token = self._token_service.create_refresh_token(user.id)
        await self._refresh_tokens.add(
            token_id=refresh_token.token_id,
            user_id=user.id,
            expires_at=refresh_token.expires_at,
        )
        return (
            user,
            self._token_service.create_access_token(user.id),
            refresh_token.encoded_token,
        )

    async def refresh(self, token: str) -> tuple[User, str, str]:
        claims = self._token_service.read_refresh_token(token)
        user = await self._users.get_by_id(claims.user_id)
        if user is None or not user.is_active or user.id is None:
            raise InvalidRefreshTokenError()

        replacement = self._token_service.create_refresh_token(user.id)
        rotated = await self._refresh_tokens.rotate(
            old_token_id=claims.token_id,
            user_id=user.id,
            new_token_id=replacement.token_id,
            new_expires_at=replacement.expires_at,
            now=datetime.now(UTC),
        )
        if not rotated:
            raise InvalidRefreshTokenError()

        return (
            user,
            self._token_service.create_access_token(user.id),
            replacement.encoded_token,
        )

    async def user_from_access_token(self, token: str) -> User | None:
        user_id = self._token_service.read_access_token(token)
        user = await self._users.get_by_id(user_id)
        if user is None or not user.is_active:
            return None
        return user

    async def logout(self, token: str) -> None:
        user_id = self._token_service.read_access_token(token)
        user = await self._users.get_by_id(user_id)
        if user is not None and user.id is not None:
            await self._refresh_tokens.revoke_by_user(user.id)
