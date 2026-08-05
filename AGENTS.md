# Repository Guidelines

## Project Scope

TaskFlow RAG Assistant is a portfolio-quality customer-support RAG assistant planned around LangChain, LangGraph, Groq, FastAPI, Next.js, and Supabase. TaskFlow is a **fictional demonstration SaaS product**. Never present it as a real company or use real customer data.

The repository is in **Phase 1 only**. Work is limited to planning, fictional business documentation, evaluation data, and UI wireframes. Do not implement the frontend, backend, database, or RAG pipeline. Do not install application dependencies.

## Repository Organization

Place files only in their designated locations:

- `docs/phase-1/`: plans, architecture notes, product specifications, and UI wireframes.
- `sample-data/knowledge-base/`: fictional TaskFlow support and business documents.
- `sample-data/evaluation/`: evaluation questions and expected-answer data.

Use Markdown for human-readable documentation and JSON for machine-readable evaluation data. Do not add implementation directories such as `src/`, `app/`, or `api/` during Phase 1.

## Content Standards

Write in clear, concise, professional English. Keep every fictional business fact consistent across planning documents, knowledge-base content, evaluation data, and wireframes. Pricing, policies, usage limits, and product features must come from the approved product facts; do not invent or silently revise them.

Every knowledge-base document must include a unique document ID, title, version, and last-updated date. Use stable, descriptive IDs and ISO dates, for example `TF-KB-BILLING-001` and `2026-08-05`.

Design RAG responses to include source citations. Evaluation cases should verify both factual correctness and citation behavior. The future Thinking panel may show only the workflow statuses defined in `docs/phase-1/rag-behavior-spec.md`, such as `Searching the knowledge base` and `Preparing a cited response`; it must never reveal private chain-of-thought or hidden reasoning.

## Security and Privacy

Use fictional, non-identifying examples only. Never create or commit API keys, credentials, secrets, production URLs, or customer records. Do not place sensitive values in Markdown, JSON, screenshots, or wireframes.

## Validation

Run all validation checks available for the files changed before declaring work complete. At minimum, check Markdown structure, JSON syntax where applicable, internal consistency, required knowledge-base metadata, and `git diff --check`. Do not claim a check passed unless it was run.

## Commits and Reviews

Keep changes focused on the requested Phase 1 artifact. Use short imperative commit subjects, such as `Add approved TaskFlow product facts`. Pull requests should describe the artifact, its source of truth, validation performed, and any effect on other Phase 1 documents.

At the end of every task, report assumptions, files changed, and validation performed. Explicitly state when there were no assumptions or when no automated check was available.
