# TaskFlow RAG Assistant Evaluation Questions

- **Version:** 1.0
- **Last Updated:** 2026-08-06
- **Product:** TaskFlow (Fictional Demonstration SaaS Product)
- **Canonical Data:** `test-questions.json`

This review document mirrors the 30 machine-readable evaluation cases. Detailed `required_facts`, `forbidden_claims`, and evaluator notes remain in the JSON file.

## Distribution

| Category | Cases |
| --- | ---: |
| Direct | 12 |
| Multi-document | 5 |
| Conversational follow-up | 5 |
| Ambiguous | 4 |
| Unsupported | 4 |
| **Total** | **30** |

## Direct Answerable Questions

| ID | Question | Expected behavior | Expected answer summary | Expected source document IDs |
| --- | --- | --- | --- | --- |
| TQ-001 | What does the Starter plan cost each month, and what are its team, project, and storage limits? | `answer` | Starter costs $12 per user per month and supports a maximum of 10 team members, 5 active projects, and 5 GB of workspace storage. | `TF-KB-PLANS-BILLING-001` |
| TQ-002 | What discount does TaskFlow offer for annual billing? | `answer` | Annual billing provides a 20 percent discount. | `TF-KB-PLANS-BILLING-001` |
| TQ-003 | Can I try TaskFlow without entering a credit card? | `answer` | Yes. TaskFlow offers a 14-day free trial without a credit card. | `TF-KB-PLANS-BILLING-001` |
| TQ-004 | Which TaskFlow plans include API access? | `answer` | API access is available on Pro and Business and is not available on Starter. | `TF-KB-INTEGRATIONS-001` |
| TQ-005 | Which integrations are available on the Pro plan? | `answer` | Pro includes Slack, Google Drive, and GitHub integrations. | `TF-KB-INTEGRATIONS-001` |
| TQ-006 | Is two-factor authentication available on every TaskFlow plan? | `answer` | Yes. Two-factor authentication is available on Starter, Pro, and Business. | `TF-KB-ACCOUNT-SECURITY-001` |
| TQ-007 | Can I use SAML single sign-on on the Pro plan? | `answer` | No. SAML single sign-on is available only on Business and is not included on Pro or Starter. | `TF-KB-ACCOUNT-SECURITY-001` |
| TQ-008 | What user roles does TaskFlow provide? | `answer` | TaskFlow provides Workspace Owner, Administrator, Member, and Viewer roles; detailed permissions are not documented. | `TF-KB-ACCOUNT-SECURITY-001` |
| TQ-009 | What is the maximum size of one TaskFlow file attachment? | `answer` | The maximum individual file-attachment size is 100 MB. | `TF-KB-GETTING-STARTED-001` |
| TQ-010 | When do I lose access after cancelling a TaskFlow subscription? | `answer` | Customers retain access until the end of the current billing period after cancellation. | `TF-KB-CANCELLATION-REFUNDS-001` |
| TQ-011 | I made my first TaskFlow payment five days ago. Can I request a refund? | `answer` | Yes. A first-time paid subscription can receive a refund when requested within 7 calendar days of the first payment, and the request must go through billing support. | `TF-KB-CANCELLATION-REFUNDS-001` |
| TQ-012 | Do subscriptions renew automatically, and are renewal payments refundable? | `answer` | Subscriptions automatically renew unless cancelled, and renewal payments are normally non-refundable. | `TF-KB-CANCELLATION-REFUNDS-001` |

All direct cases have an empty conversation context.

## Multi-Document Questions

| ID | Question | Expected behavior | Expected answer summary | Expected source document IDs |
| --- | --- | --- | --- | --- |
| TQ-013 | What is the Pro monthly price, and how long can Google Drive synchronization take? | `answer` | Pro costs $24 per user per month, includes Google Drive, and integration synchronization may take up to five minutes. | `TF-KB-PLANS-BILLING-001`, `TF-KB-INTEGRATIONS-001` |
| TQ-014 | Which plan includes SAML SSO, what is its monthly price, and how is TaskFlow data encrypted? | `answer` | Business is the only plan with SAML SSO, costs $39 per user per month, and TaskFlow data is encrypted in transit using TLS and encrypted at rest. | `TF-KB-PLANS-BILLING-001`, `TF-KB-ACCOUNT-SECURITY-001` |
| TQ-015 | What is the file-attachment size limit, and can a first-time payment be refunded after six days? | `answer` | An individual attachment may be up to 100 MB, and a first-time paid subscription can receive a refund when requested within 7 calendar days, so six days is within the documented window. | `TF-KB-GETTING-STARTED-001`, `TF-KB-CANCELLATION-REFUNDS-001` |
| TQ-016 | Can Starter use GitHub, and what is the maximum size of an individual file attachment? | `answer` | Starter does not include GitHub integration, and the maximum size of an individual file attachment is 100 MB. | `TF-KB-INTEGRATIONS-001`, `TF-KB-GETTING-STARTED-001` |
| TQ-017 | What roles exist in TaskFlow, and how long can integration synchronization take after reauthorization? | `answer` | TaskFlow has Workspace Owner, Administrator, Member, and Viewer roles. After reauthorization, integration synchronization may take up to five minutes. | `TF-KB-ACCOUNT-SECURITY-001`, `TF-KB-INTEGRATIONS-001` |

All multi-document cases have an empty conversation context.

## Conversational Follow-Up Questions

### TQ-018

- **Previous user:** How much does the Pro plan cost?
- **Previous assistant:** Pro costs $24 per user per month.
- **Question:** Does it include custom fields too?
- **Expected behavior:** `answer`
- **Expected answer summary:** Yes. The Pro plan includes custom fields.
- **Expected source document IDs:** `TF-KB-PLANS-BILLING-001`

### TQ-019

- **Previous user:** Is Google Drive available on Pro?
- **Previous assistant:** Yes. Google Drive is available on Pro and Business.
- **Question:** How long can it take to sync?
- **Expected behavior:** `answer`
- **Expected answer summary:** Google Drive integration synchronization may take up to five minutes.
- **Expected source document IDs:** `TF-KB-INTEGRATIONS-001`

### TQ-020

- **Previous user:** I made my first TaskFlow payment six days ago and want to cancel. Will I keep access?
- **Previous assistant:** Yes. After cancellation, you retain access until the end of your current billing period.
- **Question:** Can that payment be refunded?
- **Expected behavior:** `answer`
- **Expected answer summary:** A first-time paid subscription can receive a refund when requested within 7 calendar days, so a request after six days is within the documented window and must be submitted through billing support.
- **Expected source document IDs:** `TF-KB-CANCELLATION-REFUNDS-001`

### TQ-021

- **Previous user:** Does the Business plan include two-factor authentication?
- **Previous assistant:** Yes. Two-factor authentication is available on Business and every other TaskFlow plan.
- **Question:** Is SAML available on that plan too?
- **Expected behavior:** `answer`
- **Expected answer summary:** Yes. SAML SSO is available on Business, and Business is the only plan that includes it.
- **Expected source document IDs:** `TF-KB-ACCOUNT-SECURITY-001`

### TQ-022

- **Previous user:** Which plan has a maximum of five active projects?
- **Previous assistant:** Starter has a maximum of five active projects.
- **Question:** And how many team members does that one allow?
- **Expected behavior:** `answer`
- **Expected answer summary:** Starter allows a maximum of 10 team members.
- **Expected source document IDs:** `TF-KB-GETTING-STARTED-001`

## Ambiguous Questions

| ID | Question | Expected behavior | Expected answer summary | Expected source document IDs |
| --- | --- | --- | --- | --- |
| TQ-023 | What does the plan include? | `clarify` | Ask which plan the user means: Starter, Pro, or Business. | None |
| TQ-024 | Can I connect it to TaskFlow? | `clarify` | Ask which integration the user wants to connect and which TaskFlow plan they use. | None |
| TQ-025 | Can they reauthorize it? | `clarify` | Ask which user role and disconnected integration the user means. | None |
| TQ-026 | Can I get my money back? | `clarify` | Ask whether the charge was a first payment, renewal, duplicate payment, or suspected billing error and, for a first payment, when it occurred. | None |

All ambiguous cases have an empty conversation context and require a concise clarification before answering.

## Unsupported Questions

Every unsupported case must return exactly: **I could not find this information in the available TaskFlow documentation.** It must not include a fabricated citation.

| ID | Question | Expected behavior | Expected source document IDs |
| --- | --- | --- | --- |
| TQ-027 | Can I pay for TaskFlow with cryptocurrency? | `no_answer` | None |
| TQ-028 | Is TaskFlow HIPAA compliant? | `no_answer` | None |
| TQ-029 | Does TaskFlow provide a custom mobile app for my company? | `no_answer` | None |
| TQ-030 | What uptime service-level agreement does TaskFlow guarantee? | `no_answer` | None |

All unsupported cases have an empty conversation context and no expected source document IDs.
