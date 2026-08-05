# TaskFlow Product Overview

- **Document ID:** TF-P1-PRODUCT-001
- **Version:** 1.0
- **Last updated:** 2026-08-05
- **Status:** Authoritative Phase 1 product-facts source

This document is the source of truth for TaskFlow product facts in all remaining Phase 1 documents, knowledge-base articles, evaluation data, and UI wireframes. Content created later must not contradict or extend these facts without an approved update to this document.

## Product Summary

TaskFlow is a fictional project and task management SaaS product. It is created only to demonstrate the TaskFlow RAG Assistant and does not represent a real company or service.

TaskFlow provides projects, tasks, team collaboration, comments, file attachments, and integrations.

## Target Customers

TaskFlow is intended for:

- Small agencies
- Consultants
- Remote teams

## Core Capabilities

The approved core capabilities are:

- Creating and managing projects and tasks
- Team collaboration through comments
- Adding file attachments
- Connecting supported integrations
- Protecting accounts with two-factor authentication

Availability and limits vary by plan as described below.

## User Roles

TaskFlow has four user roles:

- Workspace Owner
- Administrator
- Member
- Viewer

Detailed permissions for each role are not documented. A Workspace Owner or Administrator must reauthorize a disconnected integration.

## Plans

All prices are per user per month.

| Feature | Starter | Pro | Business |
| --- | --- | --- | --- |
| Price | $12 | $24 | $39 |
| Team members | Maximum 10 | Unlimited | Unlimited |
| Active projects | Maximum 5 | Unlimited | Unlimited |
| Workspace storage | 5 GB | 100 GB | 500 GB |
| Support | Email support | Priority email support | Priority email and priority chat support |
| Two-factor authentication | Included | Included | Included |
| Custom fields | Not included | Included | Included |
| API access | Not included | Included | Included |
| Slack integration | Not included | Included | Included |
| Google Drive integration | Not included | Included | Included |
| GitHub integration | Not included | Included | Included |
| SAML single sign-on | Not included | Not included | Included |
| Audit logs | Not included | Not included | Included |
| Advanced user roles | Not included | Not included | Included |

The Business plan includes everything in Pro in addition to its Business-only capabilities and higher storage allowance.

## Billing

- Monthly and annual billing are available.
- Annual billing provides a 20 percent discount.
- A 14-day free trial is available without a credit card.
- Subscriptions renew automatically unless cancelled.
- After cancellation, customers retain access until the end of the current billing period.

## Refunds

- A first-time paid subscription is eligible for a refund when the customer requests it within 7 calendar days of the first payment.
- Subscription renewals are normally non-refundable.
- Duplicate payments and confirmed billing errors are refundable.
- Customers submit refund requests through billing support.

## Security

- Two-factor authentication is available on every plan.
- SAML single sign-on is available only on the Business plan.
- Data is encrypted in transit using TLS and encrypted at rest.
- TaskFlow does not claim compliance with regulations that are not documented.

## Integrations

- Slack, Google Drive, and GitHub integrations are available on Pro and Business.
- API access is available on Pro and Business.
- Integration synchronization may take up to five minutes.
- A disconnected integration must be reauthorized by a Workspace Owner or Administrator.

## File Limits

The maximum size of an individual file attachment is 100 MB. Supported file-type examples include:

- PDF
- DOCX
- PNG
- JPG
- ZIP

Support for file types not listed here is undocumented.

## Explicitly Unsupported or Undocumented Claims

The following capabilities are explicitly unavailable:

- API access and custom fields on Starter
- Slack, Google Drive, and GitHub integrations on Starter
- SAML single sign-on on Starter and Pro
- Audit logs and advanced user roles on Starter and Pro

The following subjects are not documented and must not be asserted as TaskFlow facts:

- Regulatory compliance or security certifications
- Uptime guarantees or service-level agreements
- Data residency, retention, deletion, backup, or disaster-recovery policies
- Exact permissions for each user role
- Support operating hours or response-time guarantees
- Integrations other than Slack, Google Drive, and GitHub
- Support for file types beyond the listed examples
- Any product feature, policy, price, or limit not stated in this document
