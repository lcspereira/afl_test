import type { HealthResponse } from '../types/health'
import { getJson } from './apiClient'

export function fetchHealth(): Promise<HealthResponse> {
  return getJson<HealthResponse>('/health')
}
