// Componente responsável por renderizar o formulário de login do usuário.
import React, { useState } from "react"
import { Box, Button, Link, TextField } from "@mui/material"
import type { LoginRequest } from "@/types/auth"
import { login } from "@/services/authtenticationService"

export default function LoginForm() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    const request: LoginRequest = { email, password }
    try {
      const response = await login(request)
      console.log("Login successful:", response)
    } catch (error) {
      console.error("Login failed:", error)
    }
  }

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{ display: "flex", flexDirection: "column", gap: 2 }}
    >
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