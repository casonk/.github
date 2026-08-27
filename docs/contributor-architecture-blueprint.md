# Contributor Architecture Blueprint

`casonk/.github` is the portfolio's shared GitHub configuration repository.
It has two deployment surfaces: account-wide community-health defaults and
reusable workflow definitions. A merge to `main` can therefore affect every
repository that inherits a default or calls a workflow at `@main`.

## Components

1. Community-health defaults
   - Root-level `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md`, plus
     the issue and pull-request templates, supply GitHub defaults when a
     repository does not carry an override.
   - A repository-local file always takes precedence. The default mechanism is
     deliberately additive; it does not rewrite a caller repository.
2. Reusable workflows
   - `python-ci.yml`, `install-check.yml`, `shell-ci.yml`, `docs-ci.yml`,
     `secret-scan.yml`, and `python-publish.yml` are called by sibling
     repositories with `uses: casonk/.github/.github/workflows/<name>@main`.
   - Inputs choose supported behavior such as Python versions or an optional
     test command. Reusable workflows own action pins and common validation.
3. Secret scanning
   - The reusable and self-hosted scans download the pinned Gitleaks CLI and
     run one full-history scan. When present, `.gitleaks-baseline.json` is
     passed directly to the CLI, keeping accepted historical findings stable.
4. Change control
   - Dependabot proposes updates to action pins in this repository only.
   - `pre-commit run --all-files` is the local gate before a change is pushed.
   - Because callers use `@main`, review workflow and default-file changes as
     portfolio-wide deployments, then observe caller CI after merge.

## Flow

```text
Maintainer change
   ├── community-health default ──> GitHub renders it for inheriting repos
   └── reusable workflow ──> caller references @main ──> caller CI executes
                                               │
                                               └── validation / artifacts
```

The editable diagrams in `docs/diagrams/` mirror this flow. Keep them aligned
with the workflow files and the default-file set when either changes.
