import { env } from '../config/env'

export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

const ACCESS_TOKEN_KEY = 'access_token'

export function setAccessToken(token: string): void {
  window.localStorage.setItem(ACCESS_TOKEN_KEY, token)
}

export function getAccessToken(): string | null {
  return typeof window === 'undefined'
    ? null
    : window.localStorage.getItem(ACCESS_TOKEN_KEY)
}

export function clearAccessToken(): void {
  if (typeof window !== 'undefined') {
    window.localStorage.removeItem(ACCESS_TOKEN_KEY)
  }
}

function requestHeaders(jsonBody = false): Record<string, string> {
  const headers: Record<string, string> = {
    Accept: 'application/json',
  }
  if (jsonBody) {
    headers['Content-Type'] = 'application/json'
  }

  const accessToken = getAccessToken()
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`
  }

  return headers
}

export async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${env.apiUrl}${path}`, {
    headers: requestHeaders(),
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
    headers: requestHeaders(true),
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

export async function postNoContent(
  path: string,
  body: unknown,
): Promise<void> {
  const response = await fetch(`${env.apiUrl}${path}`, {
    method: 'POST',
    headers: requestHeaders(true),
    body: JSON.stringify(body),
  })

  if (!response.ok) {
    throw new ApiError(
      `Falha na requisição (HTTP ${response.status})`,
      response.status,
    )
  }
}

export async function putJson<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${env.apiUrl}${path}`, {
    method: 'PUT',
    headers: requestHeaders(true),
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
    headers: requestHeaders(),
  })

  if (!response.ok) {
    throw new ApiError(
      `Falha na requisição (HTTP ${response.status})`,
      response.status,
    )
  }

  return (await response.json()) as T
}