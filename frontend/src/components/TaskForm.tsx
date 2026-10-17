import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import MenuItem from '@mui/material/MenuItem'
import TextField from '@mui/material/TextField'
import type { FormEvent } from 'react'
import { useState } from 'react'
import {
  createTask,
  TaskStatus,
  updateTask,
} from '../services/taskService'
import type { NewTask, Task } from '../services/taskService'

type TaskFormProps =
  | {
      mode: 'create'
      onSaved: (task: Task) => void
      onCancel?: () => void
    }
  | {
      mode: 'edit'
      task: Task
      onSaved: (task: Task) => void
      onCancel?: () => void
    }

function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : 'Ocorreu um erro inesperado.'
}

export function TaskForm(props: TaskFormProps) {
  const [titulo, setTitulo] = useState(
    props.mode === 'edit' ? props.task.titulo : '',
  )
  const [descricao, setDescricao] = useState(
    props.mode === 'edit' ? props.task.descricao : '',
  )
  const [status, setStatus] = useState<TaskStatus>(
    props.mode === 'edit' ? props.task.status : TaskStatus.PENDING,
  )
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSaving(true)
    setError(null)

    try {
      let savedTask: Task
      if (props.mode === 'create') {
        const newTask: NewTask = { titulo, descricao, status }
        savedTask = await createTask(newTask)
      } else {
        const taskId = props.task.id
        if (taskId === undefined) {
          throw new Error('Não foi possível identificar a tarefa.')
        }
        savedTask = await updateTask(taskId, { titulo, descricao })
      }
      props.onSaved(savedTask)
    } catch (requestError: unknown) {
      setError(errorMessage(requestError))
    } finally {
      setSaving(false)
    }
  }

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{ display: 'flex', flexDirection: 'column', gap: 2, p: 3 }}
    >
      {error && <Alert severity="error">{error}</Alert>}
      <TextField
        label="Título"
        value={titulo}
        onChange={(event) => setTitulo(event.target.value)}
        required
        disabled={saving}
      />
      <TextField
        label="Descrição"
        value={descricao}
        onChange={(event) => setDescricao(event.target.value)}
        required
        multiline
        minRows={3}
        disabled={saving}
      />
      {props.mode === 'create' && (
        <TextField
          select
          label="Status"
          value={status}
          onChange={(event) => setStatus(event.target.value as TaskStatus)}
          disabled={saving}
        >
          <MenuItem value={TaskStatus.PENDING}>Pendente</MenuItem>
          <MenuItem value={TaskStatus.IN_PROGRESS}>Em andamento</MenuItem>
          <MenuItem value={TaskStatus.COMPLETED}>Concluída</MenuItem>
        </TextField>
      )}
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 1 }}>
        {props.onCancel && (
          <Button onClick={props.onCancel} disabled={saving}>
            Cancelar
          </Button>
        )}
        <Button type="submit" variant="contained" disabled={saving}>
          {saving
            ? 'Salvando...'
            : props.mode === 'create'
              ? 'Criar tarefa'
              : 'Salvar'}
        </Button>
      </Box>
    </Box>
  )
}
