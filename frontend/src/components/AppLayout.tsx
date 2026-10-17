import AppBar from '@mui/material/AppBar'
import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Container from '@mui/material/Container'
import Menu from '@mui/material/Menu'
import MenuItem from '@mui/material/MenuItem'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import AccountCircleIcon from '@mui/icons-material/AccountCircle'
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown'
import { useEffect, useState } from 'react'
import { useLocation, useNavigate, Outlet } from 'react-router-dom'
import { ApiError, clearAccessToken, getAccessToken } from '../services/apiClient'
import {
  getCurrentUser,
  logout,
} from '../services/authtenticationService'
import type { UserResponse } from '../types/auth'

function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : 'Ocorreu um erro inesperado.'
}

export function AppLayout() {
  const [user, setUser] = useState<UserResponse | null>(null)
  const [menuAnchor, setMenuAnchor] = useState<HTMLElement | null>(null)
  const [loggingOut, setLoggingOut] = useState(false)
  const [authError, setAuthError] = useState<string | null>(null)
  const location = useLocation()
  const navigate = useNavigate()

  useEffect(() => {
    if (!getAccessToken()) {
      return
    }

    let active = true
    getCurrentUser()
      .then((currentUser) => {
        if (active) {
          setUser(currentUser)
          setAuthError(null)
        }
      })
      .catch((requestError: unknown) => {
        if (!active) {
          return
        }
        if (requestError instanceof ApiError && requestError.status === 401) {
          clearAccessToken()
          setUser(null)
          return
        }
        setAuthError(errorMessage(requestError))
      })

    return () => {
      active = false
    }
  }, [location.pathname])

  async function handleLogout() {
    setMenuAnchor(null)
    setLoggingOut(true)
    setAuthError(null)
    try {
      await logout()
    } catch {
      setAuthError(
        'A sessão foi encerrada neste dispositivo, mas não foi possível confirmar a saída no servidor.',
      )
    } finally {
      setUser(null)
      setLoggingOut(false)
      navigate('/login', { replace: true })
    }
  }

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Aplicação
          </Typography>
          {user && (
            <>
              <Button
                color="inherit"
                startIcon={<AccountCircleIcon />}
                endIcon={<ArrowDropDownIcon />}
                aria-haspopup="menu"
                onClick={(event) => setMenuAnchor(event.currentTarget)}
              >
                {user.username}
              </Button>
              <Menu
                anchorEl={menuAnchor}
                open={Boolean(menuAnchor)}
                onClose={() => setMenuAnchor(null)}
              >
                <MenuItem disabled>{user.email}</MenuItem>
                <MenuItem
                  onClick={() => void handleLogout()}
                  disabled={loggingOut}
                >
                  Sair
                </MenuItem>
              </Menu>
            </>
          )}
        </Toolbar>
      </AppBar>
      {authError && (
        <Container maxWidth="md" sx={{ pt: 2 }}>
          <Alert severity="warning">{authError}</Alert>
        </Container>
      )}
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Outlet />
      </Container>
    </Box>
  )
}
