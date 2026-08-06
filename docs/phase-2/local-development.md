# TaskFlow Phase 2 Local Development

- **Document ID:** TF-P2-LOCAL-DEV-001
- **Version:** 1.0
- **Last updated:** 2026-08-05
- **Status:** Phase 2 development guide

TaskFlow is a fictional demonstration SaaS product. This guide runs only the Next.js foundation and
FastAPI health API; no external service or real customer data is required.

## Prerequisites

- Git
- Node.js **20.9 or newer** and npm
- Python **3.12**
- `uv` for Python environments and dependency management
- Docker Engine and the Docker Compose plugin, only for the optional container workflow

Confirm the main tool versions:

```bash
node --version
npm --version
python3 --version
uv --version
docker --version
docker compose version
```

The Docker commands are optional when developing directly on the host.

## Install uv

Install `uv` using the official Astral installation instructions or an appropriate package manager.
For example, a machine with `pipx` can use:

```bash
pipx install uv
```

Do not replace the uv-managed backend environment with a committed virtual environment. The
repository pins Python 3.12 in `backend/.python-version` and backend dependencies in
`backend/uv.lock`.

## Install Dependencies

From the repository root:

```bash
npm ci
npm --prefix frontend ci
uv --directory backend sync
```

The first command installs root orchestration tooling. The second installs frontend packages. The
third creates or updates `backend/.venv` from the uv lockfile.

## Environment-File Setup

Copy the committed examples to ignored local files:

```bash
cp frontend/.env.example frontend/.env.local
cp backend/.env.example backend/.env
```

PowerShell equivalents:

```powershell
Copy-Item frontend/.env.example frontend/.env.local
Copy-Item backend/.env.example backend/.env
```

For standard host development, the example defaults already use:

```dotenv
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
FRONTEND_ORIGIN=http://localhost:3000
```

For GitHub Codespaces host development, replace those two values with the forwarded URLs:

```dotenv
NEXT_PUBLIC_API_BASE_URL=https://<codespace-name>-8000.app.github.dev
FRONTEND_ORIGIN=https://<codespace-name>-3000.app.github.dev
```

When the backend is started from a Codespace terminal, it automatically derives the forwarded
frontend origin from `CODESPACE_NAME` and `GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN`. Therefore a
local `backend/.env` is not required just for CORS. An explicit `FRONTEND_ORIGIN` still takes
priority when a custom frontend port or origin is used.

The domain comes from `GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN`; do not hardcode one specific
Codespace name in committed files. `NEXT_PUBLIC_` values are included in browser code. Never put
`GROQ_API_KEY`, `SUPABASE_SECRET_KEY`, `DATABASE_URL`, or another server secret in the frontend
environment file.

Codespaces ports are private by default. The frontend health request includes the Codespaces
authentication cookie, and the backend permits credentials only from its exact configured frontend
origin. Do not put `GITHUB_TOKEN` in a frontend environment file and do not make the API port public
just to run this health check.

Leave all Groq, Supabase, and database values empty during Phase 2. Never commit either local
environment file.

## Frontend Commands

Run these from `frontend/`:

```bash
npm run dev
npm run lint
npm run typecheck
npm run test
npm run build
npm run start
```

`npm run dev` starts the App Router development server. `npm run start` requires a successful
production build first.

## Backend Commands

Run these from `backend/`:

```bash
uv sync
uv run fastapi dev app/main.py --port 8000
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest
```

The backend starts without Groq, Supabase, or PostgreSQL credentials.

## Root Commands

Run these from the repository root:

| Command | Purpose |
| --- | --- |
| `npm run dev` | Run frontend and backend development servers together. |
| `npm run dev:frontend` | Run only Next.js. |
| `npm run dev:backend` | Run only FastAPI on port 8000. |
| `npm run lint` | Run frontend ESLint and backend Ruff. |
| `npm run format:backend` | Format backend Python files with Ruff. |
| `npm run format:backend:check` | Check backend formatting without changing files. |
| `npm run typecheck` | Run frontend TypeScript and backend mypy checks. |
| `npm run test` | Run frontend and backend tests once. |
| `npm run build` | Create the frontend production build. |
| `npm run validate:phase2` | Run the complete automated Phase 2 validator. |

The Phase 2 validator uses only the Python standard library to orchestrate structure, environment,
scope, backend, frontend, and optional Docker checks. It does not repair failures or rewrite source
files.

## URLs and Health Checks

### Host development

- Frontend: `http://localhost:3000`
- API root: `http://localhost:8000/`
- API health: `http://localhost:8000/api/v1/health`
- API readiness: `http://localhost:8000/api/v1/readiness`
- Interactive API documentation: `http://localhost:8000/docs`

### Docker in this Codespaces setup

Compose maps frontend host port 3000 to container port 3000 and API host port 8001 to container port
8000. The separate host-development backend may therefore continue using port 8000.

- Local frontend mapping: `http://localhost:3000`
- Local API mapping: `http://localhost:8001`
- Local API documentation: `http://localhost:8001/docs`
- Codespaces frontend: `https://<codespace-name>-3000.app.github.dev`
- Codespaces API: `https://<codespace-name>-8001.app.github.dev`
- Codespaces API documentation: `https://<codespace-name>-8001.app.github.dev/docs`

Compose defaults to localhost so it remains valid outside Codespaces. Before starting Compose in a
Codespace, export the browser-visible forwarded origins:

```bash
export FRONTEND_ORIGIN="https://${CODESPACE_NAME}-3000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
export NEXT_PUBLIC_API_BASE_URL="https://${CODESPACE_NAME}-8001.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
docker compose up
```

Check the Codespaces **Ports** panel for visibility and the exact forwarded addresses.

## Test, Lint, Type-Check, and Build Commands

From the repository root, the normal quality sequence is:

```bash
npm run lint
npm run format:backend:check
npm run typecheck
npm run test
npm run build
npm run validate:phase2
python3 scripts/validate_phase_1.py
git diff --check
```

Equivalent targeted commands are available as `lint:frontend`, `lint:backend`,
`typecheck:frontend`, `typecheck:backend`, `test:frontend`, and `test:backend` root scripts.

The frontend production build is intentionally independent of backend availability. The health
request runs only after the client component mounts in a browser.

## Docker Commands

From the repository root:

```bash
docker compose config
docker compose build
docker compose up
docker compose up -d
docker compose ps
docker compose logs -f api web
docker compose down
```

No Docker env file is required; Codespaces values can be exported in the current shell. Compose does
not configure Groq, Supabase, or a database. The development containers do not use an automatic
restart policy.

Override a conflicting host port when needed:

```bash
API_HOST_PORT=8002 docker compose up -d
WEB_HOST_PORT=3001 docker compose up -d
```

Container ports remain 8000 for the API and 3000 for the frontend. In Codespaces, update the
exported `NEXT_PUBLIC_API_BASE_URL` or `FRONTEND_ORIGIN` to use the same overridden host port before
starting Compose.

## Common Troubleshooting

### `address already in use`

Another process owns the published host port. Inspect listeners and containers:

```bash
ss -ltnp
docker compose ps
docker ps
```

Stop the process only when it is safe, or set `API_HOST_PORT`/`WEB_HOST_PORT` to an unused port. The
default Docker API host port is 8001 specifically so a host FastAPI process can keep port 8000.

### Frontend shows `API unavailable`

- Open the configured `/api/v1/health` URL directly and confirm it returns status `ok`.
- Confirm `NEXT_PUBLIC_API_BASE_URL` uses the host-visible or forwarded API URL, not the container
  service name.
- Confirm `FRONTEND_ORIGIN` exactly matches the browser's frontend origin.
- If `FRONTEND_ORIGIN` is unset, confirm the backend was started inside the Codespace terminal so
  the standard `CODESPACE_NAME` and `GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN` variables are
  available.
- In Codespaces, check that the API port is forwarded and accessible in the Ports panel.
- Open the private API forwarded URL once if Codespaces asks you to authenticate the port.
- Restart the frontend after changing a `NEXT_PUBLIC_` value.

### Backend rejects configuration

- Start from `backend/.env.example` and keep empty external-service values empty.
- Use valid absolute HTTP or HTTPS URLs where URL fields are configured.
- Do not add quotes, spaces, or real credentials unless a later phase explicitly requires them.

### Dependencies are missing or stale

```bash
npm ci
npm --prefix frontend ci
uv --directory backend sync --locked
```

Use `npm ci` rather than changing the lockfile during normal setup. Keep both `package-lock.json`
files and `backend/uv.lock` committed.

### Docker cannot access its daemon or cache

Confirm the Docker daemon is running and that the current user can access it. In a managed
environment, Docker operations may require the host's approved Docker permissions. Do not weaken
socket permissions globally as a shortcut.

### A constrained environment cannot write the uv cache

Point uv to a writable temporary cache for that shell:

```bash
export UV_CACHE_DIR=/tmp/taskflow-uv-cache
```

This changes only the cache location; it does not replace `backend/.venv` or alter the lockfile.
