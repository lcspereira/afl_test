// Componente responsável por renderizar o formulário de login do usuário.
import React, { useState } from "react"
import { Alert, Box, Button, Link, TextField } from "@mui/material"
import type { LoginRequest } from "@/types/auth"
import { login } from "@/services/authtenticationService"
import { useNavigate } from "react-router-dom"

export default function LoginForm() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    setError(null)
    const request: LoginRequest = { email, password }
    try {
      await login(request)
      navigate('/')
    } catch (error) {
      console.error("Login failed:", error)
      setError('Não foi possível entrar. Verifique seu e-mail e senha.')
    }
  }

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{ display: "flex", flexDirection: "column", gap: 2 }}
    >
      {error && <Alert severity="error">{error}</Alert>}
      <TextField
        type="email"
        id="email"
        label="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <TextField
        type="password"
        id="password"
        label="Senha"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <Button type="submit" variant="contained">Login</Button>
      <Link href="/register">Não tem uma conta? Registre-se aqui.</Link>
    </Box>
  )
}