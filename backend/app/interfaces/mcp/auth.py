"""Adaptadores de autenticação para requisições MCP."""

from fastmcp.server.auth import AccessToken
from fastmcp.server.auth.providers.jwt import JWTVerifier
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.bootstrap import build_auth_service
from app.core.config import Settings
from app.domain.exceptions import InvalidAccessTokenError


class ExistingAccessTokenVerifier(JWTVerifier):
    """Validate access tokens issued by this application's login endpoint."""

    def __init__(
        self,
        settings: Settings,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        super().__init__(
            public_key=settings.jwt_secret_key.get_secret_value(),
            algorithm="HS256",
        )
        self._settings = settings
        self._session_factory = session_factory

    async def verify_token(self, token: str) -> AccessToken | None:
        verified_token = await super().verify_token(token)
        if verified_token is None:
            return None

        try:
            async with self._session_factory() as session:
                user = await build_auth_service(
                    session,
                    self._settings,
                ).user_from_access_token(token)
        except InvalidAccessTokenError:
            return None

        if user is None or user.id is None:
            return None

        claims = {**verified_token.claims, "user_id": user.id}
        return verified_token.model_copy(
            update={
                "client_id": f"afl-test-user-{user.id}",
                "subject": str(user.id),
                "claims": claims,
            }
        )
