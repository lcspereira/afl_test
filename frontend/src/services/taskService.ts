import { deleteJson, getJson, postJson, putJson } from './apiClient'

export const TaskStatus = {
  PENDING: 'pendente',
  IN_PROGRESS: 'em andamento',
  COMPLETED: 'concluida',
} as const

export type TaskStatus = (typeof TaskStatus)[keyof typeof TaskStatus]

export interface Task {
  id?: number
  titulo: string
  descricao: string
  status: TaskStatus
  id_usuario?: number
  data_criacao?: string
}

export type NewTask = Pick<Task, 'titulo' | 'descricao' | 'status'>
export type TaskUpdate = Partial<NewTask>

export function getTasks(): Promise<Task[]> {
  return getJson<Task[]>('/tasks/')
}

export function createTask(task: NewTask): Promise<Task> {
  return postJson<Task>('/tasks/', task)
}

export function updateTask(id: number, updates: TaskUpdate): Promise<Task> {
  return putJson<Task>(`/tasks/${id}`, updates)
}

export function deleteTask(id: number): Promise<Task> {
  return deleteJson<Task>(`/tasks/${id}`)
}
