// Componente responsável por renderizar o formulário de registro do usuário.
import React, { useState } from "react"
import { Alert, Button, Link, Stack, TextField } from "@mui/material"
import type { RegisterRequest } from "@/types/auth"
import { register } from "@/services/authtenticationService"

export default function RegisterForm() {
  const [username, setUsername] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [feedback, setFeedback] = useState<{
    message: string
    severity: "success" | "error"
  } | null>(null)
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    setFeedback(null)
    setSubmitting(true)
    const request: RegisterRequest = { username, email, password }
    try {
      await register(request)
      setFeedback({
        message: "Cadastro realizado com sucesso. Você já pode fazer login.",
        severity: "success",
      })
    } catch {
      setFeedback({
        message:
          "Não foi possível realizar o cadastro. Verifique os dados ou tente novamente.",
        severity: "error",
      })
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Stack component="form" onSubmit={handleSubmit} spacing={2}>
      {feedback && (
        <Alert severity={feedback.severity}>{feedback.message}</Alert>
      )}
      <TextField
        label="Nome de usuário"
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        fullWidth
        required
        slotProps={{ htmlInput: { minLength: 3, maxLength: 50 } }}
      />
      <TextField
        label="Email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        fullWidth
        required
      />
      <TextField
        label="Senha"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        fullWidth
        required
        slotProps={{ htmlInput: { minLength: 8, maxLength: 128 } }}
      />
      <Button type="submit" variant="contained" disabled={submitting}>
        {submitting ? "Cadastrando..." : "Registrar"}
      </Button>
      <Link href="/login" underline="hover">
        Já tem uma conta? Faça login aqui.
      </Link>
    </Stack>
  )
}