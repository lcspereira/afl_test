import CssBaseline from '@mui/material/CssBaseline'
import { ThemeProvider } from '@mui/material/styles'
import { AppLayout } from './components/AppLayout'
import { HomePage } from './pages/HomePage'
import { theme } from './theme'

export function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppLayout>
        <HomePage />
      </AppLayout>
    </ThemeProvider>
  )
}
