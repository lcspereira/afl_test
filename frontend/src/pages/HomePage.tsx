import Alert from '@mui/material/Alert'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CircularProgress from '@mui/material/CircularProgress'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import { useEffect, useState } from 'react'
import { fetchHealth } from '../services/healthService'
import type { HealthResponse } from '../types/health'

type HealthState =
  | { kind: 'loading' }
  | { kind: 'error'; message: string }
  | { kind: 'ready'; data: HealthResponse }

export function HomePage() {
  const [state, setState] = useState<HealthState>({ kind: 'loading' })

  useEffect(() => {
    let active = true

    fetchHealth()
      .then((data) => {
        if (active) setState({ kind: 'ready', data })
      })
      .catch((error: unknown) => {
        if (!active) return
        const message =
          error instanceof Error ? error.message : 'Erro desconhecido'
        setState({ kind: 'error', message })
      })

    return () => {
      active = false
    }
  }, [])

  if (state.kind === 'loading') {
    return <CircularProgress aria-label="Carregando status" />
  }

  if (state.kind === 'error') {
    return <Alert severity="error">{state.message}</Alert>
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="h2" gutterBottom>
          Status do sistema
        </Typography>
        <Stack spacing={1}>
          <Typography>API: {state.data.status}</Typography>
          <Typography>Banco de dados: {state.data.database}</Typography>
        </Stack>
      </CardContent>
    </Card>
  )
}
