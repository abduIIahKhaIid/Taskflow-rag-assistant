# Repository Guidelines

## Project Scope

TaskFlow RAG Assistant is a portfolio-quality customer-support RAG application for TaskFlow, a **fictional demonstration SaaS product**. Never present TaskFlow as a real company or use real customer data.

The repository is in **Phase 2: project foundation and local development setup**. Phase 2 establishes a tested Next.js frontend and FastAPI backend foundation, local configuration, development tooling, and setup documentation. It does not implement the RAG product features planned for later phases.

## Phase 2 Goals

Phase 2 work is limited to these outcomes:

- Initialize a Next.js TypeScript frontend.
- Initialize a FastAPI Python backend.
- Create typed configuration management with placeholder environment examples.
- Add backend health and readiness endpoints.
- Connect the frontend to the backend health endpoint.
- Add automated tests, linting, formatting, and type checking.
- Add root-level commands for common local development and validation workflows.
- Add development Docker configuration.
- Document local setup and development workflows.
- Create an automated Phase 2 validator.

Keep every change focused on one or more of these foundation goals.

## Repository Organization

Preserve every Phase 1 file exactly unless a later task explicitly authorizes an update. Do not delete, move, rename, or silently rewrite existing files under `docs/phase-1/` or `sample-data/`.

Use these locations for Phase 2 work:

- `frontend/`: Next.js application, frontend configuration, tests, and frontend container files.
- `frontend/src/`: all frontend application code.
- `backend/`: FastAPI application, `pyproject.toml`, backend configuration, tests, and backend container files.
- `docs/phase-2/`: Phase 2 architecture, setup, and development documentation.
- `scripts/`: repository validation utilities, including the Phase 2 validator.
- Repository root: shared development commands and Docker Compose configuration.
- `docs/phase-1/`: preserved Phase 1 plans, product specifications, and wireframes.
- `sample-data/knowledge-base/`: preserved fictional TaskFlow support documents.
- `sample-data/evaluation/`: preserved evaluation data.

Do not introduce feature-oriented implementation directories outside the frontend and backend foundations.

## Technical Baseline

### Frontend

- Use Node.js 20.9 or newer.
- Use Next.js App Router, TypeScript, Tailwind CSS, and ESLint.
- Keep all frontend application code under `frontend/src/`.
- Use Vitest and React Testing Library for frontend tests.
- Keep components and configuration fully typed, and organize imports consistently.
- Limit the Phase 2 UI to foundation behavior needed to demonstrate the backend health connection. Do not build the planned chat interface.

### Backend

- Use Python 3.12.
- Use `uv` with `backend/pyproject.toml` for dependency and environment management.
- Use FastAPI and Pydantic Settings.
- Use pytest for backend tests.
- Use Ruff for linting and formatting, and mypy for type checking.
- Keep application code and tests fully typed, with organized imports.
- Provide separate health and readiness endpoints with small, stable response contracts. The frontend health check must use the backend health endpoint rather than duplicating backend status logic.

### Configuration and Local Development

- Read runtime configuration from environment variables through typed configuration modules.
- Commit only environment example files containing obvious placeholder values.
- Never create or commit `.env` or `.env.local` files.
- Keep server-only values out of frontend bundles. Never expose a Supabase secret key or any other server credential through a public frontend environment variable.
- Provide root-level commands for setup, development, tests, linting, formatting checks, type checking, and full validation.
- Keep development Docker configuration reproducible and limited to the Phase 2 frontend and backend foundation.
- Document required tool versions, environment setup, commands, ports, and health checks in the Phase 2 local-setup documentation.

## Phase 2 Restrictions

During Phase 2, do not:

- Modify, delete, move, or replace any Phase 1 artifact.
- Create Supabase database tables or database migrations.
- Implement authentication or authorization.
- Implement document uploading, storage, parsing, chunking, or reprocessing.
- Create embeddings or implement vector search or pgvector.
- Call Groq or any other language model.
- Implement LangGraph nodes or a RAG workflow.
- Build a chat interface, conversation history, citations UI, feedback controls, or admin document UI.
- Implement token streaming or Server-Sent Events.
- Create real environment secrets, credentials, production URLs, or customer records.
- Commit `.env` or `.env.local` files.
- Expose a Supabase secret key in frontend code or public configuration.
- Display private chain-of-thought, hidden reasoning, prompts, or raw internal traces.

Do not install or configure LangChain, LangGraph, Groq, Supabase, pgvector, Docling, or embedding models during Phase 2 unless a later approved Phase 2 task explicitly demonstrates that a foundation-only package is required. Prefer leaving future-stack dependencies out until the phase that uses them.

## Future Stack Awareness

The planned future application will use LangChain, LangGraph, Groq, Supabase, pgvector, Docling, and open-source embeddings. Phase 2 may keep clean integration boundaries and configuration seams for that future work, but it must not implement, simulate, or claim those capabilities.

## Product Content, Security, and Privacy

The approved Phase 1 product facts remain authoritative. Do not invent or silently revise TaskFlow pricing, policies, features, usage limits, or support behavior in code, fixtures, examples, documentation, or tests.

Use only fictional, non-identifying examples. Never add API keys, access tokens, credentials, secrets, production endpoints, or real customer information. Example values must be unmistakable placeholders and must not resemble usable credentials.

Any visible operational status must be a concise system status. Never expose private chain-of-thought or hidden reasoning. The future Thinking panel remains limited to the workflow statuses approved in `docs/phase-1/rag-behavior-spec.md`.

## Code Quality and Testing

- Keep imports organized and application code fully typed.
- Do not suppress lint, type, test, or runtime errors without a nearby documented reason.
- Add or update tests for every implemented behavior.
- Keep health checks deterministic and independent of unavailable future services.
- Prefer small, explicit interfaces between frontend configuration, backend clients, and API routes.
- Do not declare an implementation task complete until all relevant tests, lint checks, formatting checks, and type checks have run successfully.

## Validation

Run every validation check relevant to the files changed before declaring work complete. Phase 2 implementation work should run, as applicable:

- Frontend tests, ESLint, formatting checks, TypeScript checks, and production build validation.
- Backend pytest, Ruff lint and format checks, and mypy.
- Docker configuration validation when Docker files change.
- The automated Phase 2 validator.
- The Phase 1 validator to confirm preserved artifacts remain valid.
- `git diff --check` for every task.

Validate JSON syntax and Markdown structure when those file types change. Do not claim a check passed unless it was actually run. If a relevant check cannot run, report the command, reason, and remaining risk.

## Commits and Reviews

Keep changes focused on the requested Phase 2 artifact. Use short imperative commit subjects, such as `Add backend health endpoints`. Pull requests should describe the foundation change, validation performed, configuration impact, and confirmation that Phase 1 artifacts and Phase 2 restrictions remain intact.

At the end of every task, report:

- Assumptions made, or explicitly state that there were none.
- Files changed.
- Commands executed and their outcomes.
- Any validation that was unavailable and why.
