# Frontend

Interface em React + TypeScript (Vite) com Material UI.

## Estrutura

```
src/
├── config/        # Leitura de variáveis de ambiente (VITE_API_URL)
├── types/         # Tipos dos contratos da API
├── services/      # Comunicação com a API (cliente HTTP e serviços)
├── components/    # Componentes reutilizáveis (layout, etc.)
├── pages/         # Páginas da aplicação
├── theme.ts       # Tema do Material UI
├── App.tsx        # Providers globais e composição da página
└── main.tsx       # Ponto de entrada
```

## Desenvolvimento

```bash
npm install
npm run dev      # servidor de desenvolvimento em http://localhost:5173
npm run build    # checagem de tipos (tsc) e build de produção
npm run lint     # oxlint
```

A URL da API é definida por `VITE_API_URL` (padrão: `http://localhost:8000/api/v1`).
