# TaskFlow RAG Assistant

TaskFlow RAG Assistant is a portfolio project for a SaaS customer-support assistant that will use retrieval-augmented generation (RAG) to answer product questions with source citations. **TaskFlow is a fictional demonstration SaaS product**; its documentation and evaluation data do not describe a real business or contain real customer information.

## Planned Technology Stack

- Next.js and TypeScript
- Tailwind CSS
- FastAPI
- LangChain and LangGraph
- Groq API
- Supabase PostgreSQL with pgvector
- Supabase Auth and Storage
- BGE-M3 embeddings
- Docling document parsing
- Server-Sent Events for streaming

## Current Phase

The project is in **Phase 1: planning and content design**. This phase establishes the product facts, architecture, fictional knowledge base, evaluation data, and UI wireframes needed to guide later implementation.

Phase 1 deliverables will be organized as follows:

- `docs/phase-1/` for plans, specifications, architecture notes, and wireframes.
- `sample-data/knowledge-base/` for consistent fictional support documentation.
- `sample-data/evaluation/` for machine-readable evaluation questions and expected results.
- `scripts/` for future validation utilities used during repository development.

No production frontend, backend, database, authentication flow, or RAG pipeline is implemented yet. Application dependencies are intentionally not installed during Phase 1.
