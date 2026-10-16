import factory
from pwdlib import PasswordHash

from app.infrastructure.database.models.user import UserRecord
from tests.factories.base import BaseFactory


class UserFactory(BaseFactory):
    class Meta:
        model = UserRecord

    id = factory.Sequence(lambda n: n)
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password_hash = factory.LazyFunction(lambda: PasswordHash.recommended().hash("password"))
