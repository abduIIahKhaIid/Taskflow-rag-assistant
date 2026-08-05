# TaskFlow RAG Assistant Project Brief

- **Document ID:** TF-P1-BRIEF-001
- **Version:** 1.0
- **Last updated:** 2026-08-05
- **Status:** Phase 1 planning document

## 1. Project Name

TaskFlow RAG Assistant

## 2. Project Summary

TaskFlow RAG Assistant is a portfolio-quality SaaS customer-support knowledge assistant for TaskFlow, a fictional project and task management product for small agencies, consultants, and remote teams. The assistant will answer questions from approved TaskFlow documents, cite its sources, stream responses, retain conversational context, and decline to invent information that the approved documentation does not support.

## 3. Business Problem

Customers need fast, consistent answers about product features, plans, billing, refunds, security, integrations, and file limits. Manually locating and interpreting support documents creates friction and can produce inconsistent answers. A trustworthy assistant must make approved information easier to access without presenting unsupported claims as facts.

## 4. Proposed Solution

Build a retrieval-augmented customer-support assistant grounded exclusively in approved TaskFlow documents. The assistant will retrieve relevant passages, generate a concise answer, display source citations, and refuse or qualify answers when evidence is insufficient. A separate admin document-management interface will support the future management of approved source documents.

## 5. Main Portfolio Objective

Demonstrate an end-to-end, production-minded RAG design that combines grounded retrieval, controlled orchestration, streaming responses, citations, conversation history, evaluation, secure document handling, and a polished SaaS interface.

## 6. Target Audience

The primary audience is TaskFlow users from small agencies, consulting practices, and remote teams who need product-support answers. A secondary audience is authorized support administrators responsible for managing the assistant's approved documents. TaskFlow and all associated users and data are fictional.

## 7. Core User Journey

1. A user opens the assistant and asks a TaskFlow support question.
2. A collapsible Thinking panel displays approved process statuses such as `Searching the knowledge base` and `Preparing a cited response`. It never exposes private chain-of-thought.
3. The system retrieves relevant content from approved TaskFlow documents.
4. The answer streams token by token and includes citations to its supporting sources.
5. The user asks follow-up questions within the same preserved conversation history.
6. When the documents do not support a claim, the assistant clearly says that the information is unavailable instead of inventing an answer.
7. In a separate authorized workflow, an administrator manages approved source documents through the document-management interface.

## 8. Expected Business Value

The assistant is intended to reduce the effort required to find product information, improve answer consistency, and make self-service support more useful. Citations and explicit handling of unsupported questions are intended to improve trust and make answers easier to verify. No quantitative business outcome is assumed during Phase 1.

## 9. Planned Technology Stack

- Next.js and TypeScript for the web interface
- Tailwind CSS for interface styling
- FastAPI for the application API
- LangChain for document and retrieval workflows
- LangGraph for controlled assistant orchestration
- Groq API for language-model inference
- Supabase PostgreSQL with pgvector for application data and vector retrieval
- Supabase Auth and Storage for authentication and approved document storage
- BGE-M3 embeddings for document and query representations
- Docling for document parsing
- Server-Sent Events for token and process-status streaming

## 10. Phase 1 Purpose

Phase 1 defines the project before implementation. Its deliverables are planning documents, consistent fictional business documentation, machine-readable evaluation data, and UI wireframes. No frontend, backend, database, authentication, document pipeline, or RAG implementation will be built, and no application dependencies will be installed during this phase.

## 11. Future Implementation Overview

A future ingestion workflow will parse approved documents with Docling, create BGE-M3 embeddings, and store searchable vectors in Supabase PostgreSQL with pgvector. LangChain and LangGraph will coordinate retrieval and response generation through the Groq API. FastAPI will expose authenticated services and stream answer tokens and process statuses over Server-Sent Events. A Next.js and TypeScript interface styled with Tailwind CSS will provide chat, citations, conversation history, the collapsible Thinking panel, and administrative document management. Supabase Auth and Storage will support access control and source-file storage.

## 12. Constraints and Assumptions

- `product-overview.md` is the authoritative source for TaskFlow product facts.
- Only approved TaskFlow documents may ground an answer.
- TaskFlow is fictional, and no real customer data, credentials, or secrets may be used.
- Answers must cite sources and must not invent unsupported information.
- The Thinking panel is limited to process statuses and must not reveal private reasoning.
- Website crawling, OCR, CRM integrations, multi-tenancy, voice input, and external automation are outside the MVP scope.
- Detailed behavior not established by approved Phase 1 documents remains undecided rather than assumed.

## 13. Definition of Project Success

Phase 1 succeeds when its plans, fictional knowledge base, evaluation data, and wireframes provide a consistent and testable implementation blueprint. The completed project succeeds when users can ask TaskFlow support questions, receive accurate streamed answers grounded in approved documents, inspect useful citations, continue contextual conversations, and receive clear refusals for unsupported claims. It must also provide status-only progress updates and an authorized document-management workflow without exposing sensitive data or private chain-of-thought.

## 14. Open Decisions

The following details remain deliberately unresolved and must not be presented as approved product facts or implemented MVP behavior until they are decided:

- **Product operations:** Exact procedures for TaskFlow login, password reset, workspace creation, invitations, project creation, task assignment, initial integration authorization, plan changes, and cancellation.
- **Product-role permissions:** Permissions for Workspace Owner, Administrator, Member, and Viewer beyond reauthorizing a disconnected integration.
- **Billing operations:** Currency, annual totals, taxes, proration, charge dates, renewal notices, cancellation notice requirements, and refund-processing details.
- **Support operations:** Support addresses, operating hours, response targets, and contact procedures for the documented support channels.
- **RAG configuration:** Chunk size and overlap, retrieval candidate count, relevance thresholds, and evaluation pass thresholds.
- **Assistant administration:** Knowledge-source upload-size limits, final document-processing status vocabulary, and the approved workflow for replacing a source with a new version.
- **Assistant account data:** Password policy, account recovery, session duration, and conversation-history retention or deletion rules.

Until these decisions are approved and reconciled across affected artifacts, the assistant must follow the no-answer behavior or direct customers to support where the approved knowledge-base documents explicitly require it.
