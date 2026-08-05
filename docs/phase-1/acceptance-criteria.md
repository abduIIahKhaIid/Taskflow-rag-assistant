# TaskFlow Phase 1 Acceptance Criteria

- **Document ID:** TF-P1-ACCEPTANCE-001
- **Version:** 1.0
- **Last updated:** 2026-08-05
- **Status:** Phase 1 review checklist

TaskFlow is a fictional demonstration SaaS product. This checklist records the current repository state: `[x]` means the criterion has evidence and was verified; `[ ]` means evidence is missing or the criterion remains unresolved.

## Project Definition

- [x] **Product and business problem are clear.** `product-overview.md` defines TaskFlow, and `project-brief.md` describes the customer-support problem and proposed RAG solution.
- [x] **MVP scope is clearly bounded.** `project-scope.md` separates the future MVP from current Phase 1 work and defines its completion boundary.
- [x] **Out-of-scope features are documented.** `project-scope.md` lists explicit exclusions and scope-control rules.

## Knowledge Base

- [x] **Five approved documents exist.** `sample-data/knowledge-base/` contains five Markdown source documents with `Approved` status.
- [x] **Every document has metadata.** Each source contains a unique document ID, title, version, status, last-updated date, product, and intended audience.
- [x] **Pricing and policy facts are consistent.** Plan prices, limits, billing, cancellation, refund, security, and integration facts match `product-overview.md`.
- [x] **No real customer information exists.** The source documents contain fictional product content and no real customer records.
- [x] **Unsupported claims are not presented as facts.** Undocumented procedures, compliance claims, guarantees, and product behavior are identified as undocumented rather than inferred.

## RAG Behavior

- [x] **Citation behavior is specified.** `rag-behavior-spec.md` defines inline markers, source labels, citation opening, and source-verification rules.
- [x] **No-answer behavior is specified.** The standard no-answer response and its usage boundary are defined.
- [x] **Ambiguous-question behavior is specified.** The assistant must ask one concise clarification instead of guessing.
- [x] **Follow-up-question behavior is specified.** Conversation context may resolve references but cannot serve as factual evidence.
- [x] **Thinking statuses do not expose private reasoning.** Only approved workflow statuses are visible; prompts and private chain-of-thought are prohibited.

## Evaluation

- [x] **Exactly 30 test cases exist.** `test-questions.json` contains 30 cases across all required categories.
- [x] **Test IDs are unique.** IDs run uniquely and sequentially from `TQ-001` through `TQ-030`.
- [x] **JSON is valid.** The evaluation file parses successfully and every item contains the required fields.
- [x] **Expected sources exist.** Every referenced source ID matches an approved knowledge-base document.
- [x] **Unsupported questions have no expected source.** All four unsupported cases use `no_answer` and an empty source list.

## UI

- [x] **Chat, admin, and mobile wireframes exist.** `ui-wireframes.md` covers the main chat, document administration, and mobile chat layouts.
- [x] **Streaming, citations, and status-panel states are covered.** Dedicated wireframes define token streaming, Stop Generation, citation inspection, and status-only Thinking behavior.

## Portfolio

- [x] **Product is clearly labeled fictional.** Planning, knowledge-base, evaluation, and UI documents identify TaskFlow as a fictional demonstration product.
- [x] **Technology stack matches the project plan.** The planned stack consistently includes Next.js, TypeScript, Tailwind CSS, FastAPI, LangChain, LangGraph, Groq API, Supabase PostgreSQL with pgvector, Supabase Auth and Storage, BGE-M3, Docling, and Server-Sent Events.

## Phase 1 Completion Definition

**Phase 1 is complete only when all validation checks pass and the documents contain no unresolved contradictions.**

Current decision: **Complete.** All checklist criteria have evidence, available repository validation checks pass, and no unresolved content contradiction was found. Any later change to product facts, scope, source documents, evaluation data, or wireframes requires the affected criteria to be reviewed again.
