// Serviço responsável por lidar com a autenticação do usuário.

import type {
  AuthResponse,
  LoginRequest,
  RegisterRequest,
  UserResponse,
} from '@/types/auth'
import {
  clearAccessToken,
  getJson,
  postJson,
  postNoContent,
} from './apiClient'

export async function login(request: LoginRequest): Promise<AuthResponse> {
  const response = await postJson<AuthResponse>('/auth/token', request)
  // setAccessToken(response.access_token)
  return response
}

export function register(request: RegisterRequest): Promise<UserResponse> {
  return postJson<UserResponse>('/auth/register', request)
}

export function getCurrentUser(): Promise<UserResponse> {
  return getJson<UserResponse>('/users/me')
}

export async function logout(): Promise<void> {
  try {
    await postNoContent('/auth/logout', {})
  } finally {
    clearAccessToken()
  }
}