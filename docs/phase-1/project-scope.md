# TaskFlow RAG Assistant Project Scope

- **Document ID:** TF-P1-SCOPE-001
- **Version:** 1.0
- **Last updated:** 2026-08-05
- **Status:** Phase 1 planning document

This document defines the boundary of the future TaskFlow RAG Assistant minimum viable product (MVP). It does not authorize implementation during Phase 1. TaskFlow is a fictional demonstration SaaS product, and `product-overview.md` remains the authority for its product facts.

## In Scope for MVP

### Access and Roles

- Email and password authentication
- Assistant-level Admin and User roles
- Role-based access to user chat and admin document-management functions

These assistant roles do not define or change TaskFlow's Workspace Owner, Administrator, Member, and Viewer product roles.

### Knowledge Management and Retrieval

- Upload of PDF, DOCX, TXT, and Markdown knowledge-source files
- Document processing status
- Text chunking
- Local open-source BGE-M3 embeddings
- Vector retrieval with Supabase PostgreSQL and pgvector
- Admin document list
- Delete and reprocess document actions

Knowledge-source upload formats are an assistant ingestion constraint. They are separate from the customer file-attachment examples and limits documented for the fictional TaskFlow product.

### RAG and Answer Behavior

- LangGraph RAG workflow
- Groq answer generation
- Source citations
- ChatGPT-style token-by-token answer streaming
- Collapsible Thinking panel showing process statuses only, never private chain-of-thought
- Unsupported-question handling that refuses or qualifies claims without approved evidence

### Chat Experience

- Conversation history
- Suggested questions
- Copy response
- Stop generation
- Regenerate response
- Positive and negative response feedback
- Responsive web interface

### Delivery and Quality

- Docker-ready FastAPI backend
- Basic machine-readable evaluation dataset covering grounded answers, citations, and unsupported questions

## Out of Scope for MVP

- Website crawling
- Scanned-document OCR
- Audio or voice interaction
- CRM integration
- Slack bot
- Multi-tenant enterprise architecture
- Payment processing
- Human support ticket escalation
- Model fine-tuning
- Native mobile applications
- Real production customer data
- Advanced analytics
- Regulated medical, legal, or financial data

Out-of-scope capabilities must not appear as implemented features, MVP acceptance criteria, or implied commitments.

## Future Enhancements

After the MVP is completed and evaluated, the team may assess selected out-of-scope capabilities or other improvements through a separate discovery and approval process. This section is directional only: no future enhancement is scheduled, funded, designed, or committed as part of the MVP.

## Assumptions

- Only approved, fictional TaskFlow documents will be ingested and used to generate answers.
- `product-overview.md` will remain the source of truth unless it is explicitly revised.
- BGE-M3 embeddings will run locally; Groq will provide answer-generation inference.
- Users will authenticate before accessing chat or administration features.
- Knowledge Administrators receive the assistant-level Admin role; customers and Support Agents receive the assistant-level User role unless a later approved access design states otherwise.
- Conversation history and feedback contain demonstration data only.
- Details not specified in approved Phase 1 documents remain undecided.

## Dependencies

- Complete, internally consistent TaskFlow knowledge-base documents with required metadata
- A basic evaluation dataset with expected facts, citations, and unsupported-answer behavior
- Next.js, TypeScript, and Tailwind CSS for the future responsive interface
- FastAPI, LangChain, LangGraph, Docling, and BGE-M3 for the future backend and ingestion workflow
- Supabase PostgreSQL with pgvector, Auth, and Storage
- Groq API access
- Server-Sent Events support for answer and status streaming
- Docker tooling for backend packaging and verification

No application dependencies, service accounts, API keys, or credentials are required or created during Phase 1.

## Third-Party Cost Exclusions

The project scope does not include a production operating budget or vendor cost estimate. Groq usage, Supabase paid services, hosting, domains, email delivery, monitoring, CI services, storage, network transfer, and local embedding compute may incur costs during later implementation or deployment. No free-tier availability or production pricing is assumed.

## Scope-Control Rules

1. A capability is in the MVP only when it appears in the In Scope section.
2. New or changed product facts must first be approved in `product-overview.md` and reconciled across affected Phase 1 artifacts.
3. Scope changes require a documented update to this file, affected designs, and evaluation coverage before implementation.
4. Out-of-scope items must not be introduced indirectly through UI copy, architecture, sample data, or acceptance criteria.
5. The assistant must use approved sources, cite answers, and handle insufficient evidence without invention.
6. The Thinking panel may expose operational statuses but never private chain-of-thought or hidden reasoning.
7. Phase 1 work remains limited to planning, fictional documentation, evaluation data, and wireframes.

## MVP Completion Boundary

The MVP is complete only when all in-scope capabilities are implemented and verified together:

- Email/password authentication and assistant Admin/User authorization protect the correct interfaces.
- Administrators can list, upload, delete, and reprocess supported source documents and inspect processing status.
- Approved document text is parsed, chunked, embedded locally, stored, and retrieved through pgvector.
- The LangGraph workflow produces grounded Groq answers with citations and clear unsupported-question handling.
- Answers and process statuses stream independently; the Thinking panel reveals no private reasoning.
- Users can use conversation history, suggested questions, copy, stop, regenerate, and feedback controls on responsive layouts.
- The FastAPI backend can be built and run with Docker.
- The basic evaluation dataset verifies agreed answer, citation, and refusal behavior.
- No out-of-scope feature or real production customer data is required for acceptance.

Completing Phase 1 documentation is a prerequisite for implementation, not completion of the MVP itself.
