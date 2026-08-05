---
Document ID: TF-KB-INTEGRATIONS-001
Title: Integrations and Troubleshooting
Version: 1.0
Status: Approved
Last Updated: 2026-08-06
Product: TaskFlow (Fictional Demonstration SaaS Product)
Intended Audience: TaskFlow customers, workspace users, and support staff
---

# Integrations and Troubleshooting

TaskFlow is a fictional demonstration SaaS product. Its approved integrations are Slack, Google Drive, and GitHub. API access is also available on qualifying plans.

## Availability by Plan

| Capability | Starter | Pro | Business |
| --- | --- | --- | --- |
| Slack integration | Not available | Available | Available |
| Google Drive integration | Not available | Available | Available |
| GitHub integration | Not available | Available | Available |
| API access | Not available | Available | Available |

No integrations other than Slack, Google Drive, and GitHub are documented.

## Slack

The Slack integration is available on Pro and Business. It is not available on Starter. The approved product information does not define Slack features, connection screens, permissions, or notification behavior. Contact support for current connection guidance.

## Google Drive

The Google Drive integration is available on Pro and Business. It is not available on Starter. Folder selection, supported Drive operations, and connection steps are not documented. Contact support for current guidance.

## GitHub

The GitHub integration is available on Pro and Business. It is not available on Starter. Repository permissions, supported GitHub events, and connection steps are not documented. Contact support for current guidance.

## API Access

API access is available on Pro and Business and is not available on Starter. Authentication methods, endpoints, usage limits, and API documentation locations are not included in the approved product facts. Contact support for current API-access information.

## Authorization

An integration must remain authorized to stay connected. The exact initial authorization workflow, provider consent prompts, and roles allowed to create the first connection are not documented. Contact support rather than assuming an authorization procedure.

If an integration becomes disconnected, it must be reauthorized by a **Workspace Owner or Administrator**.

## Synchronization Window

Integration synchronization may take up to **five minutes**. A change that does not appear immediately is not necessarily a connection failure; allow the documented synchronization window before troubleshooting further.

## Reauthorize a Disconnected Integration

When TaskFlow identifies an integration as disconnected:

1. Confirm that the workspace is on Pro or Business.
2. Ask a Workspace Owner or Administrator to reauthorize the integration.
3. Allow up to five minutes for synchronization after reauthorization.
4. If the integration remains disconnected, contact support.

The exact navigation and provider-specific reauthorization prompts are not documented. Contact support for the current procedure rather than relying on assumed interface steps.

## Common Troubleshooting Steps

Use only the checks supported by the approved product information:

1. **Verify plan availability.** Slack, Google Drive, GitHub, and API access require Pro or Business.
2. **Allow synchronization time.** Wait up to five minutes for an integration change to synchronize.
3. **Check for a disconnected integration.** If it is disconnected, a Workspace Owner or Administrator must reauthorize it.
4. **Contact support when the issue continues.** Provider errors, permission requirements, connection logs, and detailed recovery steps are not documented.

Do not assume undocumented integration behavior, synchronization guarantees, API limits, or support response times.
