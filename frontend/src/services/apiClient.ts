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
