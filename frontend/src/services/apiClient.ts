import { env } from '../config/env'

export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${env.apiUrl}${path}`, {
    headers: { Accept: 'application/json' },
  })

  if (!response.ok) {
    throw new ApiError(
      `Falha na requisição (HTTP ${response.status})`,
      response.status,
    )
  }

  return (await response.json()) as T
}

export async function postJson<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${env.apiUrl}${path}`, {
    method: 'POST',
    headers: { 
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body),
  })

  if (!response.ok) {
    throw new ApiError(
      `Falha na requisição (HTTP ${response.status})`,
      response.status,
    )
  }

  return (await response.json()) as T
}

export async function putJson<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${env.apiUrl}${path}`, {
    method: 'PUT',
    headers: { 
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body),
  })

  if (!response.ok) {
    throw new ApiError(
      `Falha na requisição (HTTP ${response.status})`,
      response.status,
    )
  }

  return (await response.json()) as T
}

export async function deleteJson<T>(path: string): Promise<T> {
  const response = await fetch(`${env.apiUrl}${path}`, {
    method: 'DELETE',
    headers: { 
      'Accept': 'application/json',
    },
  })

  if (!response.ok) {
    throw new ApiError(
      `Falha na requisição (HTTP ${response.status})`,
      response.status,
    )
  }

  return (await response.json()) as T
}