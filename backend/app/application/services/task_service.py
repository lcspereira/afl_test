"""Serviço de aplicação para gerenciamento de tarefas."""

from app.infrastructure.database.models.task import Status, TaskRecord
from app.infrastructure.database.repositories.task import (
    SqlAlchemyTaskRepository,
)


class TaskService:
    def __init__(self, tasks: SqlAlchemyTaskRepository):
        self._tasks = tasks

    async def create_task(
        self,
        titulo: str,
        descricao: str,
        id_usuario: int,
        status: Status = Status.PENDING,
    ) -> TaskRecord:
        """Cria uma nova tarefa para o usuário especificado.

        Args:
            titulo (str): O título da tarefa.
            descricao (str): A descrição da tarefa.
            id_usuario (int): O ID do usuário que está criando a tarefa.

        Returns:
            TaskRecord: A tarefa criada.

        Raises:
            ValueError: Se o título ou a descrição estiverem vazios.
        """
        if titulo is None or not titulo.strip():
            raise ValueError("Título não pode estar vazio")
        if descricao is None or not descricao.strip():
            raise ValueError("Descrição não pode estar vazia")
        new_task = TaskRecord(
            titulo=titulo,
            descricao=descricao,
            id_usuario=id_usuario,
            status=status,
        )
        return await self._tasks.add(new_task)

    async def get_task(self, task_id: int, id_usuario: int) -> TaskRecord:
        """Obtém uma tarefa específica para o usuário especificado.

        Args:
            task_id (int): O ID da tarefa.
            id_usuario (int): O ID do usuário que está solicitando a tarefa.

        Returns:
            TaskRecord: A tarefa solicitada.

        Raises:
            ValueError: Se a tarefa não for encontrada ou não pertencer
                ao usuário.
        """
        task = await self._tasks.get_by_id(task_id)
        if not task or task.id_usuario != id_usuario:
            raise ValueError("Tarefa não encontrada")
        return task

    async def update_task(
        self,
        task_id: int,
        titulo: str | None,
        descricao: str | None,
        status: Status | None,
        id_usuario: int,
    ) -> TaskRecord:
        """Atualiza uma tarefa existente para o usuário especificado.

        Args:
            task_id (int): O ID da tarefa a ser atualizada.
            titulo (str): O novo título da tarefa.
            descricao (str): A nova descrição da tarefa.
            status (Status): O novo status da tarefa.
            id_usuario (int): O ID do usuário que está atualizando a tarefa.

        Returns:
            TaskRecord: A tarefa atualizada.

        Raises:
            ValueError: Se o título ou a descrição estiverem vazios, se o
                status for inválido ou se a tarefa não for encontrada.
            PermissionError: Se o usuário não estiver autorizado a atualizar
                a tarefa.
        """
        if titulo is not None and not titulo.strip():
            raise ValueError("Título não pode estar vazio")
        if descricao is not None and not descricao.strip():
            raise ValueError("Descrição não pode estar vazia")
        if status is not None and status not in Status:
            raise ValueError("Status inválido")

        current_task = await self._tasks.get_by_id(task_id)
        if not current_task:
            raise ValueError("Tarefa não encontrada")
        if current_task.id_usuario != id_usuario:
            raise PermissionError("Não autorizado a atualizar esta tarefa")

        current_task = TaskRecord(
            id=current_task.id,
            titulo=titulo if titulo is not None else current_task.titulo,
            descricao=descricao
            if descricao is not None
            else current_task.descricao,
            status=status if status is not None else current_task.status,
            id_usuario=current_task.id_usuario,
            data_criacao=current_task.data_criacao,
        )
        await self._tasks.update(current_task)
        return current_task

    async def delete_task(self, task_id: int, id_usuario: int) -> TaskRecord:
        """Exclui uma tarefa existente para o usuário especificado.

        Args:
            task_id (int): O ID da tarefa a ser excluída.
            id_usuario (int): O ID do usuário que está solicitando a exclusão.

        Raises:
            ValueError: Se a tarefa não for encontrada.
            PermissionError: Se o usuário não estiver autorizado a deletar
                a tarefa.
        """
        task = await self._tasks.get_by_id(task_id)
        if not task:
            raise ValueError("Tarefa não encontrada")

        if task.id_usuario != id_usuario:
            raise PermissionError("Não autorizado a deletar esta tarefa")

        await self._tasks.remove(task.id)
        return task

    async def list_tasks_by_user(self, id_usuario: int) -> list[TaskRecord]:
        """Lista todas as tarefas de um usuário específico.

        Args:
            id_usuario (int): O ID do usuário cujas tarefas serão listadas.

        Returns:
            list[TaskRecord]: Uma lista de tarefas pertencentes ao usuário.
        """
        return await self._tasks.list_by_user_id(id_usuario)
