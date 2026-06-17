# Security Policy

## Reporting a Vulnerability

Please do **not** open a public issue for security vulnerabilities.

Report security concerns privately by emailing **casonk@umich.edu**. Include a description of the issue, steps to reproduce, and any relevant context. You will receive a response within 7 days.

## Scope

This repository contains reusable GitHub Actions workflows and community health files. Security concerns include:

- Workflow steps that could expose secrets to untrusted code
- Supply-chain risks from pinned third-party actions
- Permissions granted to workflow jobs

## Supported Versions

Only the current `main` branch is actively maintained. Pin to `@main` for the latest fixes, or reference a specific commit SHA for stability.
