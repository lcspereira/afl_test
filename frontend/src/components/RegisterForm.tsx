// Componente responsável por renderizar o formulário de registro do usuário.
import React, { useState } from "react"
import { Button, Link, Stack, TextField } from "@mui/material"
import type { RegisterRequest } from "@/types/auth"
import { register } from "@/services/authtenticationService"

export default function RegisterForm() {
  const [username, setUsername] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    const request: RegisterRequest = { username, email, password }
    try {
      const response = await register(request)
      console.log("Registration successful:", response)
    } catch (error) {
      console.error("Registration failed:", error)
    }
  }

  return (
    <Stack component="form" onSubmit={handleSubmit} spacing={2}>
      <TextField
        label="Nome de usuário"
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        fullWidth
      />
      <TextField
        label="Email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        fullWidth
      />
      <TextField
        label="Senha"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        fullWidth
      />
      <Button type="submit" variant="contained">Registrar</Button>
      <Link href="/login" underline="hover">
        Já tem uma conta? Faça login aqui.
      </Link>
    </Stack>
  )
}