import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.task_service import TaskService
from app.domain.repositories import TaskRepository
from app.infrastructure.database.models.task import TaskRecord
from app.infrastructure.database.models.user import UserRecord
from tests.factories.user import UserFactory
from tests.factories.task import TaskFactory
from app.infrastructure.database.repositories.task import SqlAlchemyTaskRepository


async def _create_user(db_session: AsyncSession) -> UserRecord:
    user = UserFactory.build()
    db_session.add(user)
    await db_session.flush()
    return user


@pytest.mark.asyncio
async def test_create_task(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    task = TaskFactory(titulo="Test Task", descricao="Test Description")
    user = await _create_user(db_session)
    task.id_usuario = user.id
    task = await service.create_task(titulo=task.titulo, descricao=task.descricao, id_usuario=task.id_usuario)
    assert task.titulo == "Test Task"
    assert task.descricao == "Test Description"
    assert task.data_criacao is not None
    assert task.status == "pendente"
    assert task.id is not None
    assert task.id_usuario == task.id_usuario

@pytest.mark.asyncio
async def test_create_task_with_empty_title(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    task = TaskFactory(titulo="", descricao="Test Description")
    user = await _create_user(db_session)
    task.id_usuario = user.id
    with pytest.raises(ValueError):
        await service.create_task(titulo=task.titulo, descricao=task.descricao, id_usuario=task.id_usuario)

@pytest.mark.asyncio
async def test_create_task_with_empty_description(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    task = TaskFactory(titulo="Test Task", descricao="")
    user = await _create_user(db_session)
    task.id_usuario = user.id
    with pytest.raises(ValueError):
        await service.create_task(titulo=task.titulo, descricao=task.descricao, id_usuario=task.id_usuario)

@pytest.mark.asyncio
async def test_create_task_with_whitespace_title(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    task = TaskFactory(titulo="   ", descricao="Test Description")
    user = await _create_user(db_session)
    task.id_usuario = user.id
    with pytest.raises(ValueError):
        await service.create_task(titulo=task.titulo, descricao=task.descricao, id_usuario=task.id_usuario)

@pytest.mark.asyncio
async def test_create_task_with_whitespace_description(db_session):
    task = TaskFactory(titulo="Test Task", descricao="   ")
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    user = await _create_user(db_session)
    task.id_usuario = user.id
    with pytest.raises(ValueError):
        await service.create_task(titulo=task.titulo, descricao=task.descricao, id_usuario=task.id_usuario)

@pytest.mark.asyncio
async def test_get_task(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    task = TaskFactory(titulo="Test Task", descricao="Test Description")
    user = await _create_user(db_session)
    task.id_usuario = user.id
    task_record = await service.create_task(titulo=task.titulo, descricao=task.descricao, id_usuario=task.id_usuario)
    fetched_task = await service.get_task(task_record.id, id_usuario=task_record.id_usuario)
    assert fetched_task.id == task_record.id
    assert fetched_task.titulo == task_record.titulo
    assert fetched_task.descricao == task_record.descricao
    assert fetched_task.data_criacao is not None
    assert fetched_task.status == "pendente"

@pytest.mark.asyncio
async def test_list_tasks_scoped_by_user(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    task1 = TaskFactory(titulo="Task 1", descricao="Description 1")
    task2 = TaskFactory(titulo="Task 2", descricao="Description 2")
    user1 = await _create_user(db_session)
    task1.id_usuario = user1.id
    user2 = await _create_user(db_session)
    task2.id_usuario = user2.id
    await service.create_task(titulo=task1.titulo, descricao=task1.descricao, id_usuario=task1.id_usuario)
    await service.create_task(titulo=task2.titulo, descricao=task2.descricao, id_usuario=task2.id_usuario)
    tasks = await service.list_tasks_by_user(id_usuario=task1.id_usuario)
    assert len(tasks) == 1
    assert any(t.id_usuario == task1.id_usuario for t in tasks)
    assert all(t.id_usuario != task2.id_usuario for t in tasks)
    tasks = await service.list_tasks_by_user(id_usuario=task2.id_usuario)
    assert len(tasks) == 1
    assert any(t.id_usuario == task2.id_usuario for t in tasks)
    assert all(t.id_usuario != task1.id_usuario for t in tasks)

@pytest.mark.asyncio
async def test_get_task_not_found_by_user(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    task = TaskFactory(titulo="Test Task", descricao="Test Description", status="pendente")
    user = await _create_user(db_session)
    task.id_usuario = user.id
    await service.create_task(titulo=task.titulo, descricao=task.descricao, id_usuario=task.id_usuario)
    with pytest.raises(ValueError):
        await service.get_task(999, id_usuario=user.id)

@pytest.mark.asyncio
async def test_get_task_not_found(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    with pytest.raises(ValueError):
        await service.get_task(999, id_usuario=1)

@pytest.mark.asyncio
async def test_update_task(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    user = await _create_user(db_session)
    task_factory = TaskFactory(titulo="Test Task", descricao="Test Description", id_usuario=user.id)
    task = await service.create_task(
        titulo=task_factory.titulo,
        descricao=task_factory.descricao,
        id_usuario=user.id,
    )
    updated_task = await service.update_task(task.id, titulo="Updated Task", descricao="Updated Description", status="concluida", id_usuario=user.id)
    assert updated_task.id == task.id
    assert updated_task.titulo == "Updated Task"
    assert updated_task.descricao == "Updated Description"
    assert updated_task.data_criacao is not None
    assert updated_task.status == "concluida"
    assert updated_task.id_usuario == task.id_usuario

@pytest.mark.asyncio
async def test_update_task_not_found(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    with pytest.raises(ValueError):
        await service.update_task(999, titulo="Updated Task", descricao="Updated Description", status="concluida", id_usuario=1)

@pytest.mark.asyncio
async def test_update_task_another_user(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    user = await _create_user(db_session)
    task_factory = TaskFactory(titulo="Test Task", descricao="Test Description", id_usuario=user.id)
    task = await service.create_task(
        titulo=task_factory.titulo,
        descricao=task_factory.descricao,
        id_usuario=task_factory.id_usuario,
    )
    another_user = await _create_user(db_session)
    with pytest.raises(PermissionError):
        await service.update_task(task.id, titulo="Updated Task", descricao="Updated Description", status="concluida", id_usuario=another_user.id)

@pytest.mark.asyncio
async def test_update_task_with_empty_title(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    user = await _create_user(db_session)
    task_factory = TaskFactory(titulo="Test Task", descricao="Test Description", id_usuario=user.id)
    task = await service.create_task(
        titulo=task_factory.titulo,
        descricao=task_factory.descricao,
        id_usuario=task_factory.id_usuario,
    )
    with pytest.raises(ValueError):
        await service.update_task(task.id, titulo="", descricao="Updated Description", status="concluida", id_usuario=user.id)

@pytest.mark.asyncio
async def test_update_task_with_empty_description(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    user = await _create_user(db_session)
    task_factory = TaskFactory(titulo="Test Task", descricao="Test Description", id_usuario=user.id)
    task = await service.create_task(
        titulo=task_factory.titulo,
        descricao=task_factory.descricao,
        id_usuario=task_factory.id_usuario,
    )
    with pytest.raises(ValueError):
        await service.update_task(task.id, titulo="Updated Task", descricao="", status="concluida", id_usuario=user.id)

@pytest.mark.asyncio
async def test_update_task_with_whitespace_title(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    user = await _create_user(db_session)
    task_factory = TaskFactory(titulo="Test Task", descricao="Test Description", id_usuario=user.id)
    task = await service.create_task(
        titulo=task_factory.titulo,
        descricao=task_factory.descricao,
        id_usuario=task_factory.id_usuario,
    )
    with pytest.raises(ValueError):
        await service.update_task(task.id, titulo="   ", descricao="Updated Description", status="concluida", id_usuario=user.id)

@pytest.mark.asyncio
async def test_update_task_with_whitespace_description(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    user = await _create_user(db_session)
    task_factory = TaskFactory(titulo="Test Task", descricao="Test Description", id_usuario=user.id)
    task = await service.create_task(
        titulo=task_factory.titulo,
        descricao=task_factory.descricao,
        id_usuario=task_factory.id_usuario,
    )
    with pytest.raises(ValueError):
        await service.update_task(task.id, titulo="Updated Task", descricao="   ", status="concluida", id_usuario=user.id)

@pytest.mark.asyncio
async def test_update_task_with_invalid_status(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    user = await _create_user(db_session)
    task_factory = TaskFactory(titulo="Test Task", descricao="Test Description", id_usuario=user.id)
    task = await service.create_task(
        titulo=task_factory.titulo,
        descricao=task_factory.descricao,
        id_usuario=task_factory.id_usuario,
    )
    with pytest.raises(ValueError):
        await service.update_task(task.id, titulo="Updated Task", descricao="Updated Description", status="invalid_status", id_usuario=user.id)

@pytest.mark.asyncio
async def test_delete_task(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    user = await _create_user(db_session)
    task_factory = TaskFactory(titulo="Test Task", descricao="Test Description", id_usuario=user.id)
    task = await service.create_task(
        titulo=task_factory.titulo,
        descricao=task_factory.descricao,
        id_usuario=task_factory.id_usuario,
    )
    await service.delete_task(task.id, id_usuario=user.id)
    with pytest.raises(ValueError):
        await service.get_task(task.id, id_usuario=user.id)

@pytest.mark.asyncio
async def test_delete_nonexistent_task(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    with pytest.raises(ValueError):
        await service.delete_task(999, id_usuario=1)

@pytest.mark.asyncio
async def test_delete_task_another_user(db_session):
    service = TaskService(tasks=SqlAlchemyTaskRepository(db_session))
    user = await _create_user(db_session)
    task_factory = TaskFactory(titulo="Test Task", descricao="Test Description", id_usuario=user.id)
    task = await service.create_task(
        titulo=task_factory.titulo,
        descricao=task_factory.descricao,
        id_usuario=task_factory.id_usuario,
    )
    another_user = await _create_user(db_session)
    with pytest.raises(PermissionError):
        await service.delete_task(task.id, id_usuario=another_user.id)