---
Document ID: TF-KB-ACCOUNT-SECURITY-001
Title: Account and Security
Version: 1.0
Status: Approved
Last Updated: 2026-08-06
Product: TaskFlow (Fictional Demonstration SaaS Product)
Intended Audience: TaskFlow customers and workspace users
---

# Account and Security

TaskFlow is a fictional demonstration SaaS product. This article summarizes approved account and security facts without making undocumented compliance or product claims.

## Login

The approved product information does not define TaskFlow's login identifier, sign-in screens, session duration, or detailed login procedure. Contact TaskFlow support for current sign-in instructions or help with login access.

Business customers may use SAML single sign-on as described below. SAML SSO is not available on Starter or Pro.

## Password Reset

The password-reset workflow, reset-link behavior, and account-recovery requirements are not documented in the approved product information. Contact support for the current password-reset procedure. Do not send a password or two-factor authentication code to support.

## Two-Factor Authentication

Two-factor authentication is available on **Starter, Pro, and Business**. The setup method, supported authentication factors, recovery process, and enforcement options are not documented. Contact support for current setup or recovery instructions.

## User Roles

TaskFlow provides these roles:

- Workspace Owner
- Administrator
- Member
- Viewer

Detailed permissions for each role are not documented. The approved product information states only that a Workspace Owner or Administrator must reauthorize a disconnected integration. Contact support rather than assuming other permissions from a role name.

## SAML Single Sign-On

SAML single sign-on is available **only on the Business plan**. It is not included on Starter or Pro. Configuration steps, identity-provider compatibility, and SAML administration permissions are not documented; contact support for current SAML setup guidance.

## Data Encryption

TaskFlow data is encrypted in transit using TLS and encrypted at rest. No additional encryption methods, key-management details, or security guarantees are documented.

## Session-Security Recommendations

The following are user-security recommendations, not claims about undocumented TaskFlow controls:

- Enable two-factor authentication.
- Keep account credentials and authentication codes private.
- Use a trusted device when accessing an account.
- Sign out after using a shared device.
- Contact support if account access appears unexpected.

TaskFlow session timeouts, device-management features, and session-revocation controls are not documented.

## Compliance Claims

TaskFlow does not claim compliance with regulations that are not documented. The approved product information does not identify regulatory certifications, audit standards, data-residency commitments, or compliance guarantees. Contact support for clarification, but do not treat the absence of documentation as evidence of compliance.
