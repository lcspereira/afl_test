from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.task import Task
from app.infrastructure.database.models import TaskRecord


class SqlAlchemyTaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, task: TaskRecord) -> TaskRecord:
        self._session.add(task)
        await self._session.commit()
        await self._session.refresh(task)
        return self._to_entity(task)

    async def get_by_id(self, task_id: int) -> Task | None:
        task = await self._session.scalar(
            select(TaskRecord).where(TaskRecord.id == task_id)
        )
        return self._to_entity(task) if task else None

    async def list_all(self) -> list[Task]:
        result = await self._session.execute(select(TaskRecord))
        tasks = result.scalars().all()
        return [self._to_entity(task) for task in tasks]

    async def list_by_user_id(self, user_id: int) -> list[Task]:
        result = await self._session.execute(
            select(TaskRecord).where(TaskRecord.id_usuario == user_id)
        )
        tasks = result.scalars().all()
        return [self._to_entity(task) for task in tasks]

    async def remove(self, task_id: int) -> None:
        stmt = delete(TaskRecord).where(TaskRecord.id == task_id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def update(self, task: TaskRecord) -> TaskRecord:
        updated_task = await self._session.merge(task)
        await self._session.commit()
        await self._session.refresh(updated_task)
        return self._to_entity(updated_task)

    @staticmethod
    def _to_entity(task: TaskRecord) -> Task:
        return Task(
            id=task.id,
            id_usuario=task.id_usuario,
            titulo=task.titulo,
            descricao=task.descricao,
            status=task.status,
            data_criacao=task.data_criacao,
        )
