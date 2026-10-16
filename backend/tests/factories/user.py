from pwdlib import PasswordHash

from app.infrastructure.database.models.user import UserRecord
from tests.factories.base import BaseFactory


class UserFactory(BaseFactory):
    class Meta:
        model = UserRecord

    username = "testuser"
    email = "testuser@example.com"
    password_hash = PasswordHash.recommended().hash("password")
