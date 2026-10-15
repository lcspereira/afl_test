# Aplicação FastAPI + React

Esqueleto de aplicação com backend em FastAPI e frontend em React com Material UI, seguindo arquitetura limpa, princípios SOLID, desenvolvimento orientado a testes (TDD) e PEP 8.

## Tecnologias

- **Backend:** FastAPI, SQLAlchemy, SQLite, pydantic-settings, uv
- **Testes:** pytest, factory_boy, httpx2
- **Frontend:** React, TypeScript, Vite, Material UI
- **Infraestrutura:** Docker, docker-compose

## Estrutura do repositório

```
.
├── backend/
│   ├── app/
│   │   ├── core/              # Configurações (Settings) e utilitários centrais
│   │   ├── domain/            # Entidades, exceções e contratos de repositório (sem dependências de framework)
│   │   ├── application/       # Casos de uso: serviços (camada de regras de negócio) e portas
│   │   ├── infrastructure/    # Adaptadores: banco de dados (SQLAlchemy), repositórios e sessões
│   │   ├── interfaces/        # Interface HTTP: routers, schemas, dependências e tratadores de erro
│   │   └── main.py            # Composição da aplicação (create_app)
│   ├── tests/
│   │   ├── conftest.py        # Fixtures globais (settings, sessão de banco, cliente HTTP)
│   │   ├── factories/         # Fábricas factory_boy
│   │   ├── unit/              # Testes unitários
│   │   └── integration/       # Testes de integração
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── config/            # Variáveis de ambiente do frontend
│   │   ├── types/             # Tipos dos contratos da API
│   │   ├── services/          # Cliente HTTP e serviços de acesso à API
│   │   ├── components/        # Componentes reutilizáveis
│   │   └── pages/             # Páginas
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
└── .env.example
```

## Arquitetura do backend

As dependências apontam sempre para dentro (`interfaces` → `application` → `domain`), e `infrastructure` implementa os contratos definidos nas camadas internas.

| Camada | Responsabilidade |
|---|---|
| `domain` | Regras de negócio puras, exceções de domínio e interfaces de repositório. Não importa FastAPI nem SQLAlchemy. |
| `application` | Serviços (`services/`) que orquestram os casos de uso e portas (`ports.py`) que descrevem dependências externas. |
| `infrastructure` | Implementações concretas: engine e sessão do SQLAlchemy, modelos, repositórios e probes. |
| `interfaces` | Adaptação HTTP: routers, schemas Pydantic, injeção de dependências e mapeamento de erros de domínio para respostas HTTP. |

A composição acontece em `app/main.py`, na função `create_app`, que recebe as configurações e monta banco, middlewares, tratadores de erro e rotas.

## Como executar

### Localmente

Backend:

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

A API fica disponível em `http://localhost:8000`. A documentação interativa está em `http://localhost:8000/docs`.

Frontend:

```bash
cd frontend
npm install
npm run dev
```

O frontend fica disponível em `http://localhost:5173`.

### Com Docker

```bash
docker compose up --build
```

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`

O banco SQLite fica em um volume nomeado (`backend-data`), preservado entre reinicializações.

## Variáveis de ambiente

As variáveis do backend são lidas de ambiente ou do arquivo `backend/.env`. Veja `.env.example` como referência.

| Variável | Padrão | Descrição |
|---|---|---|
| `APP_NAME` | `Aplicação` | Nome da aplicação |
| `ENVIRONMENT` | `development` | Ambiente: `development`, `test` ou `production` |
| `DEBUG` | `false` | Modo de depuração |
| `API_PREFIX` | `/api/v1` | Prefixo das rotas da API |
| `DATABASE_URL` | `sqlite:///./data/app.db` | URL de conexão SQLAlchemy |
| `CORS_ORIGINS` | `["http://localhost:3000","http://localhost:5173"]` | Origens permitidas (lista JSON) |
| `VITE_API_URL` | `http://localhost:8000/api/v1` | URL da API usada pelo frontend (definida no build) |

## Testes e política de desenvolvimento

O projeto segue TDD: o teste deve ser escrito antes da implementação.

Política sobre testes:

- **Agentes de IA não escrevem nem modificam testes** (`test_*.py`), a menos que isso seja solicitado explicitamente.
- **Agentes de IA podem criar e modificar apenas fixtures**, como `conftest.py` e as fábricas em `tests/factories/`.
- Os testes são escritos pela equipe.

Executar a suíte de testes:

```bash
cd backend
uv run pytest
```

Verificar lint e formatação:

```bash
cd backend
uv run ruff check .
uv run ruff format --check .
```
