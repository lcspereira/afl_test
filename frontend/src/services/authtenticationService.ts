// Serviço responsável por lidar com a autenticação do usuário.

import type { AuthResponse, LoginRequest, RegisterRequest } from "@/types/auth"
import { postJson } from './apiClient'

export function login(request: LoginRequest): Promise<AuthResponse> {
  return postJson("/auth/token", request)
}

export function register(request: RegisterRequest): Promise<AuthResponse> {
  return postJson("/auth/register", request)
}

export function logout(): Promise<void> {
  return postJson("/auth/logout", {})
}