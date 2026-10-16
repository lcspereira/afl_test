from app.infrastructure.database.models.task import TaskRecord, Status
import factory
from tests.factories.base import BaseFactory
from datetime import datetime, timezone
from tests.factories.user import UserFactory

class TaskFactory(BaseFactory):
    class Meta:
        model = TaskRecord

    id = factory.Sequence(lambda n: n)
    titulo = factory.Faker("sentence", nb_words=4)
    descricao = factory.Faker("sentence", nb_words=10)
    data_criacao = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    status = factory.Faker("random_element", elements=[Status.PENDING, Status.COMPLETED, Status.IN_PROGRESS])
    id_usuario = factory.SubFactory(UserFactory)