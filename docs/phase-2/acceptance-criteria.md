# TaskFlow Phase 2 Acceptance Criteria

- **Document ID:** TF-P2-ACCEPTANCE-001
- **Version:** 1.0
- **Last updated:** 2026-08-05
- **Status:** Phase 2 review checklist

TaskFlow is a fictional demonstration SaaS product. In this checklist, `[x]` records repository
evidence verified during Phase 2 foundation work, while `[ ]` identifies work still required before
the entire phase can be closed.

## Frontend Initialization

- [x] A private Next.js application exists under `frontend/`.
- [x] The application uses the App Router, TypeScript, Tailwind CSS, and ESLint.
- [x] Frontend application code is under `frontend/src/`.
- [x] The application uses system fonts and does not depend on a remote font.
- [x] The Phase 2 screen is responsive and contains no chat interface or fabricated RAG output.

## Backend Initialization

- [x] A Python 3.12 FastAPI application exists under `backend/`.
- [x] `backend/pyproject.toml` and `backend/uv.lock` define the uv-managed environment.
- [x] Application modules are organized under `backend/app/`.
- [x] pytest, Ruff, and mypy configuration is present.
- [x] The backend starts without external credentials.

## API Health

- [x] `GET /` returns typed public API metadata.
- [x] `GET /api/v1/health` returns typed liveness information with HTTP 200.
- [x] `GET /api/v1/readiness` returns API-only Phase 2 readiness with HTTP 200.
- [x] Health and readiness responses contain no secret-like fields.
- [x] Readiness does not depend on Groq, Supabase, PostgreSQL, or another external service.
- [x] CORS permits the configured frontend origin and does not enable credentials for every origin.

## Frontend API Status

- [x] `SystemStatus` is a client component.
- [x] The health request begins only after the component mounts.
- [x] The component shows checking, connected, and unavailable states with accessible status text.
- [x] The request uses the configured public API base URL and `GET /api/v1/health`.
- [x] An `AbortController` and bounded timeout prevent endless loading.
- [x] Backend unavailability does not block static generation or a production build.

## Environment Security

- [x] Frontend and backend example environment files contain placeholders only.
- [x] `.env` and `.env.local` files are ignored while all `.env.example` files remain trackable.
- [x] Public frontend variables are distinguished from server-only configuration.
- [x] Groq, Supabase, and database configuration is optional in Phase 2.
- [x] Secret settings use masked types and are not returned by public endpoints.
- [x] No Groq or Supabase secret key is exposed through a `NEXT_PUBLIC_` variable.

## Testing

- [x] Vitest and React Testing Library cover loading, connected, unavailable, and configured-URL
  frontend status behavior.
- [x] pytest covers backend defaults, optional configuration, secret masking, caching, metadata,
  health, readiness, CORS, and response-field security.
- [x] Root scripts run frontend and backend tests once.
- [x] `scripts/validate_phase_2.py` exists and the root `validate:phase2` command passes.
- [x] The Phase 1 validator continues to pass without modifying Phase 1 artifacts.

## Linting

- [x] Frontend ESLint configuration and commands are present.
- [x] Backend Ruff enables `E`, `F`, `I`, `B`, and `UP` rules for Python 3.12.
- [x] Root scripts run both frontend and backend lint checks.
- [x] Ruff formatting and non-mutating formatting-check commands are available.

## Type Checking

- [x] The frontend uses strict TypeScript and provides a no-emit type-check command.
- [x] Backend mypy targets Python 3.12 and checks `backend/app`.
- [x] Backend functions are typed and unused-ignore/unreachable warnings are enabled.
- [x] The root type-check command runs both toolchains.

## Production Build

- [x] A root build command creates the frontend production build.
- [x] The build does not fetch backend health during static generation.
- [x] The production build passes without requiring the backend or external credentials.

## Docker Configuration

- [x] The frontend development image uses official Node 20 Alpine and locked `npm ci` installation.
- [x] The backend development image uses Python 3.12 slim and a pinned official uv image.
- [x] Compose defines `web` and `api`, valid localhost defaults, overridable host ports and origins,
  and frontend-to-API dependency ordering.
- [x] Docker configuration requires no environment file, database, Groq credential, or Supabase
  credential.
- [x] `docker compose config` resolves successfully.
- [x] Both development images build and the containerized API health endpoint responds successfully.

## Documentation

- [x] The architecture foundation documents responsibilities, communication, configuration
  boundaries, current structure, future locations, and disconnected external services.
- [x] The local-development guide documents prerequisites, setup, commands, URLs, Docker, and
  troubleshooting.
- [x] This checklist records the Phase 2 acceptance boundary.
- [x] Later-phase features are consistently described as planned rather than implemented.

## Scope Compliance

- [x] Every Phase 1 file remains preserved.
- [x] No authentication, document ingestion, parsing, embeddings, vector search, or pgvector is
  implemented.
- [x] No database table or migration is created.
- [x] No Groq, Supabase, PostgreSQL, LangChain, or LangGraph runtime connection is made.
- [x] No chat interface, conversation history, token streaming, or model response is implemented.
- [x] No real customer data, credential, `.env`, or `.env.local` file is committed.
- [x] No private chain-of-thought or hidden reasoning is displayed.

## Completion Gate

**Phase 2 is complete only when the frontend build, frontend tests, backend tests, linting and type
checking all pass.** All other checked requirements in this document must also remain satisfied, and
the automated Phase 2 validator must exist and pass before the phase is formally closed.

Current decision: **Complete.** The required application quality gates and the automated Phase 2
validator pass, while Phase 1 artifacts remain preserved. Any later foundation change requires the
affected checks and the complete validator to run again.
