# REFS-PUBLIC.md

Public external references for `dot-github` (the `casonk/.github` repo).

## GitHub Actions (pinned in reusable workflows)

| Action | Pin | Purpose |
|---|---|---|
| `actions/checkout` | `@v6` | Repository checkout |
| `actions/setup-python` | `@v6` | Python environment setup |
| `actions/upload-artifact` | `@v4` | Artifact storage (CI outputs) |
| `actions/download-artifact` | `@v4` | Artifact retrieval (publish job) |
| `gitleaks/gitleaks-action` | `@v2` | Secret detection on push/PR |
| `pypa/gh-action-pypi-publish` | `@release/v1` | OIDC-based PyPI publishing |
| `ruby/setup-ruby` | `@v1` | Ruby/Jekyll environment setup |

## External Services

| Service | URL | Purpose |
|---|---|---|
| PyPI | https://pypi.org | Python package registry |
| Gitleaks | https://github.com/gitleaks/gitleaks | Secret detection CLI and action |
