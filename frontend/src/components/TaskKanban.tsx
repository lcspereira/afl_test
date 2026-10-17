import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Chip from '@mui/material/Chip'
import CircularProgress from '@mui/material/CircularProgress'
import Dialog from '@mui/material/Dialog'
import DialogActions from '@mui/material/DialogActions'
import DialogContent from '@mui/material/DialogContent'
import DialogContentText from '@mui/material/DialogContentText'
import DialogTitle from '@mui/material/DialogTitle'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import type { DragEvent } from 'react'
import { useEffect, useState } from 'react'
import { Link as RouterLink } from 'react-router-dom'
import { TaskCard } from './TaskCard'
import { TaskForm } from './TaskForm'
import { ApiError } from '../services/apiClient'
import {
  deleteTask,
  getTasks,
  TaskStatus,
  updateTask,
} from '../services/taskService'
import type { Task } from '../services/taskService'

const columns = [
  { status: TaskStatus.PENDING, title: 'Pendente' },
  { status: TaskStatus.IN_PROGRESS, title: 'Em andamento' },
  { status: TaskStatus.COMPLETED, title: 'Concluída' },
] as const

interface TaskKanbanProps {
  handleNewTaskButtonClick: () => void
  refreshTrigger: number
}

function errorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message
  }
  return 'Ocorreu um erro inesperado.'
}

export function TaskKanban({
  handleNewTaskButtonClick,
  refreshTrigger,
}: TaskKanbanProps) {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [requiresLogin, setRequiresLogin] = useState(false)
  const [draggedTaskId, setDraggedTaskId] = useState<number | null>(null)
  const [activeColumn, setActiveColumn] = useState<TaskStatus | null>(null)
  const [savingTaskIds, setSavingTaskIds] = useState<Set<number | undefined>>(
    () => new Set(),
  )
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [deletingTask, setDeletingTask] = useState<Task | null>(null)
  const [deleteError, setDeleteError] = useState<string | null>(null)
  const [retryCount, setRetryCount] = useState(0)

  useEffect(() => {
    let active = true

    getTasks()
      .then((loadedTasks) => {
        if (active) {
          setTasks(loadedTasks)
        }
      })
      .catch((requestError: unknown) => {
        if (!active) {
          return
        }
        setError(errorMessage(requestError))
        setRequiresLogin(
          requestError instanceof ApiError && requestError.status === 401,
        )
      })
      .finally(() => {
        if (active) {
          setLoading(false)
        }
      })

    return () => {
      active = false
    }
  }, [refreshTrigger, retryCount])

  async function handleDrop(
    event: DragEvent<HTMLDivElement>,
    nextStatus: TaskStatus,
  ): Promise<void> {
    event.preventDefault()
    setActiveColumn(null)
    setDraggedTaskId(null)

    const taskId = Number(event.dataTransfer.getData('text/plain'))
    const task = tasks.find((item) => item.id === taskId)
    if (
      !Number.isInteger(taskId) ||
      !task ||
      task.status === nextStatus ||
      savingTaskIds.has(taskId)
    ) {
      return
    }

    setError(null)
    setTasks((currentTasks) =>
      currentTasks.map((item) =>
        item.id === taskId ? { ...item, status: nextStatus } : item,
      ),
    )
    setSavingTaskIds((currentIds) => new Set(currentIds).add(taskId))

    try {
      const updatedTask = await updateTask(taskId, { status: nextStatus })
      setTasks((currentTasks) =>
        currentTasks.map((item) => (item.id === taskId ? updatedTask : item)),
      )
    } catch (requestError: unknown) {
      setTasks((currentTasks) =>
        currentTasks.map((item) => (item.id === taskId ? task : item)),
      )
      setError(errorMessage(requestError))
      setRequiresLogin(
        requestError instanceof ApiError && requestError.status === 401,
      )
    } finally {
      setSavingTaskIds((currentIds) => {
        const nextIds = new Set(currentIds)
        nextIds.delete(taskId)
        return nextIds
      })
    }
  }

  function handleTaskUpdated(updatedTask: Task) {
    setTasks((currentTasks) =>
      currentTasks.map((task) =>
        task.id === updatedTask.id ? updatedTask : task,
      ),
    )
    setEditingTask(null)
  }

  async function handleTaskDelete() {
    if (deletingTask?.id === undefined) {
      return
    }

    const taskId = deletingTask.id
    setSavingTaskIds((currentIds) => new Set(currentIds).add(taskId))
    try {
      await deleteTask(taskId)
      setTasks((currentTasks) =>
        currentTasks.filter((task) => task.id !== taskId),
      )
      setDeletingTask(null)
      setDeleteError(null)
      setError(null)
    } catch (requestError: unknown) {
      setDeleteError(errorMessage(requestError))
      setError(errorMessage(requestError))
      setRequiresLogin(
        requestError instanceof ApiError && requestError.status === 401,
      )
    } finally {
      setSavingTaskIds((currentIds) => {
        const nextIds = new Set(currentIds)
        nextIds.delete(taskId)
        return nextIds
      })
    }
  }

  return (
    <Stack spacing={3}>
      <Box>
        <Typography variant="h4" component="h1" gutterBottom>
          Minhas tarefas
        </Typography>
        <Typography color="text.secondary">
          Arraste os cartões para outra coluna para atualizar o status.
        </Typography>
        <Button
          variant="contained"
          onClick={handleNewTaskButtonClick}
          sx={{ mt: 2 }}
        >
          Nova Tarefa
        </Button>
      </Box>

      {error && (
        <Alert
          severity="error"
          action={
            requiresLogin ? (
              <Button
                color="inherit"
                component={RouterLink}
                to="/login"
                size="small"
              >
                Entrar
              </Button>
            ) : undefined
          }
        >
          {requiresLogin ? 'Faça login para acessar as tarefas.' : error}
        </Alert>
      )}

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 6 }}>
          <CircularProgress aria-label="Carregando tarefas" />
        </Box>
      ) : error && tasks.length === 0 ? (
        !requiresLogin && (
          <Button
            variant="outlined"
            onClick={() => {
              setLoading(true)
              setError(null)
              setRequiresLogin(false)
              setRetryCount((count) => count + 1)
            }}
            sx={{ alignSelf: 'flex-start' }}
          >
            Tentar novamente
          </Button>
        )
      ) : (
        <Box
          sx={{
            display: 'grid',
            gridTemplateColumns: {
              xs: '1fr',
              md: 'repeat(3, minmax(0, 1fr))',
            },
            gap: 2,
            alignItems: 'start',
          }}
        >
          {columns.map((column) => {
            const columnTasks = tasks.filter(
              (task) => task.status === column.status,
            )

            return (
              <Box
                key={column.status}
                onDragOver={(event) => {
                  event.preventDefault()
                  event.dataTransfer.dropEffect = 'move'
                }}
                onDragEnter={() => setActiveColumn(column.status)}
                onDrop={(event) => void handleDrop(event, column.status)}
                sx={{
                  minHeight: 280,
                  p: 2,
                  border: 1,
                  borderColor:
                    activeColumn === column.status
                      ? 'primary.main'
                      : 'divider',
                  borderRadius: 2,
                  bgcolor:
                    activeColumn === column.status
                      ? 'action.hover'
                      : 'background.paper',
                  transition: 'background-color 120ms, border-color 120ms',
                }}
              >
                <Stack
                  direction="row"
                  sx={{
                    mb: 2,
                    alignItems: 'center',
                    justifyContent: 'space-between',
                  }}
                >
                  <Typography variant="h6" component="h2">
                    {column.title}
                  </Typography>
                  <Chip label={columnTasks.length} size="small" />
                </Stack>

                <Stack spacing={1.5}>
                  {columnTasks.map((task, index) => (
                    <TaskCard
                      key={task.id ?? `${task.titulo}-${index}`}
                      task={task}
                      isSaving={savingTaskIds.has(task.id)}
                      isDragging={draggedTaskId === task.id}
                      onDragStart={setDraggedTaskId}
                      onEdit={setEditingTask}
                      onDelete={(task) => {
                        setDeleteError(null)
                        setDeletingTask(task)
                      }}
                      onDragEnd={() => {
                        setDraggedTaskId(null)
                        setActiveColumn(null)
                      }}
                    />
                  ))}
                  {columnTasks.length === 0 && (
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      sx={{ py: 2, textAlign: 'center' }}
                    >
                      Solte uma tarefa aqui
                    </Typography>
                  )}
                </Stack>
              </Box>
            )
          })}
        </Box>
      )}

      <Dialog
        open={editingTask !== null}
        onClose={() => setEditingTask(null)}
        fullWidth
        maxWidth="sm"
      >
        {editingTask && (
          <>
            <DialogTitle>Editar tarefa</DialogTitle>
            <TaskForm
              key={editingTask.id}
              mode="edit"
              task={editingTask}
              onSaved={handleTaskUpdated}
              onCancel={() => setEditingTask(null)}
            />
          </>
        )}
      </Dialog>

      <Dialog
        open={deletingTask !== null}
        onClose={() => setDeletingTask(null)}
      >
        <DialogTitle>Excluir tarefa?</DialogTitle>
        <DialogContent>
          {deleteError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {deleteError}
            </Alert>
          )}
          <DialogContentText>
            A tarefa “{deletingTask?.titulo}” será excluída permanentemente.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeletingTask(null)}>Cancelar</Button>
          <Button
            color="error"
            onClick={() => void handleTaskDelete()}
            disabled={deletingTask?.id === undefined}
          >
            Excluir
          </Button>
        </DialogActions>
      </Dialog>
    </Stack>
  )
}
