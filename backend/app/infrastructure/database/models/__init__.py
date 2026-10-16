"""Modelos ORM da aplicação.

Importe cada modelo neste pacote para que seja registrado em `Base.metadata`.
"""

from app.infrastructure.database.models.refresh_token import (  # noqa: F401
    RefreshTokenRecord,
)
from app.infrastructure.database.models.user import UserRecord  # noqa: F401
