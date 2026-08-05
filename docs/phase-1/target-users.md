# TaskFlow RAG Assistant Target Users

- **Document ID:** TF-P1-USERS-001
- **Version:** 1.0
- **Last updated:** 2026-08-05
- **Status:** Phase 1 planning document

This document defines the intended users of the TaskFlow RAG Assistant. The permissions below describe planned access to the assistant, not the undocumented permissions of TaskFlow's Workspace Owner, Administrator, Member, and Viewer product roles.

## Primary Persona

### Customer: Maya Chen

- **Role:** Operations lead at a fictional small agency using TaskFlow.
- **Goals:** Find accurate answers quickly, compare plans, understand account setup, connect supported tools, and make informed cancellation decisions.
- **Common questions:** "Which plan supports custom fields?" "How do I set up two-factor authentication?" "Can I connect GitHub on Starter?" "What happens to access after cancellation?"
- **Pain points:** Product information can take time to locate, plan differences may be easy to confuse, and unsupported answers can create costly misunderstandings.
- **How the assistant helps:** Provides concise answers grounded in approved documents, streams responses, cites sources, preserves conversation context, and clearly identifies information that is not documented.
- **Required permissions:** Authenticated access to ask support questions, view citations and process statuses, and access the customer's own assistant conversation history. No knowledge-base management permission.

Maya is the primary persona because customer self-service is the assistant's central use case.

## Secondary Personas

### Support Agent: Daniel Brooks

- **Role:** Support employee at the fictional TaskFlow company.
- **Goals:** Give customers consistent answers, verify facts before responding, and distinguish approved policy from undocumented claims.
- **Common questions:** "Is a renewal refundable?" "Which plans include API access?" "Who can reauthorize a disconnected integration?" "What is the maximum attachment size?"
- **Pain points:** Repeatedly searching documentation is slow, similar plan details can be confused, and inconsistent wording can reduce customer trust.
- **How the assistant helps:** Retrieves relevant approved content, summarizes it with citations, maintains context across follow-up questions, and refuses to invent missing policy details.
- **Required permissions:** Authenticated access to ask questions, view citations and process statuses, and retain the agent's own assistant conversation history. No permission to upload, delete, or reprocess source documents.

### Knowledge Administrator: Priya Shah

- **Role:** Administrator responsible for the fictional assistant's approved source-document collection.
- **Goals:** Keep source material current, add approved documents, reprocess existing documents when needed, remove obsolete documents, and maintain a reliable knowledge base.
- **Common questions:** "Which version of this document is active?" "Has this document finished processing?" "Which source supports this answer?" "Can an obsolete document be removed?"
- **Pain points:** Stale or duplicate sources can create conflicting answers, missing metadata weakens traceability, and unclear document status makes maintenance difficult.
- **How the assistant helps:** Provides an administrative document-management interface for listing, uploading, deleting, and reprocessing approved sources, while exposing document and processing statuses without private chain-of-thought.
- **Required permissions:** Authenticated access to the administrative document-management interface and permission to list, upload, delete, and reprocess approved source documents. Also requires standard assistant access for verifying answers and citations.

Daniel and Priya are secondary personas because they support answer consistency and knowledge quality while the primary experience remains customer self-service.

## Users Outside the MVP

The MVP is not designed for:

- Anonymous public users without authorized assistant access
- Users seeking general advice unrelated to TaskFlow support documentation
- Users expecting the assistant to execute account, billing, cancellation, or integration changes
- External systems attempting to control the assistant through CRM integrations or other automation
- Voice-only users
- Operators of website-crawling or OCR ingestion workflows
- Organizations requiring a multi-tenant assistant deployment

These exclusions describe assistant scope only and do not add or change TaskFlow product facts.

## Privacy Note

Maya Chen, Daniel Brooks, and Priya Shah are entirely fictional personas created for this portfolio demonstration. They do not represent real customers, employees, or administrators. No real customer data or personally identifying information may be used in persona materials, evaluation data, documents, screenshots, or wireframes.
