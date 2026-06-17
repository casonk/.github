# AGENTS.md — dot-github (casonk/.github)

This is the `casonk/.github` repository: GitHub account-level community health files and portfolio-wide reusable CI/CD workflows.

## Purpose

- **Community health defaults**: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` at repo root are displayed by GitHub for any `casonk` repo that lacks its own copy.
- **Reusable workflows**: `.github/workflows/*.yml` are callable from any `casonk` repo via `uses: casonk/.github/.github/workflows/<name>@main`.
- **Dependabot**: `.github/dependabot.yml` keeps action version pins current weekly. This is the ONLY repo in the portfolio where `github-actions` ecosystem Dependabot is configured.

## Portfolio Standards

Portfolio-wide governance lives in `./util-repos/traction-control`. Read `traction-control/AGENTS.md` for cross-repo conventions, baseline requirements, and operating rules.

## Shared Utilities Available

Standard implementations for common portfolio capabilities:
- `./util-repos/archility` — architecture toolchain bootstrap/render, Graphviz diagrams, agentic architecture authoring
- `./util-repos/auto-pass` — KeePassXC-backed password management and secret retrieval
- `./util-repos/clockwork` — shared cron and systemd scheduler manifest rendering
- `./util-repos/tachometer` — repo and resource profiling, manifest-driven local profile conventions
- `./util-repos/nordility` — NordVPN CLI/API automation
- `./util-repos/shock-relay` — cross-platform messaging relay (Signal, Telegram, Twilio, Gmail)
- `./util-repos/short-circuit` — WireGuard VPN setup and configuration
- `./util-repos/snowbridge` — SMB-based private file sharing
- `./util-repos/dyno-lab` — unified test bench utilities (fixtures, mocks, schema validation)
- `./util-repos/crew-chief` — local Ollama LLM service and zero-dependency Python client

## Editing Reusable Workflows

1. Changes to `.github/workflows/` on `main` take effect immediately for every calling repo — treat this as a portfolio-wide deploy.
2. Test in a branch or fork before merging.
3. Update `CHANGELOG.md` and note any calling-repo impact.

## Dependabot Conflict Strategy

| Situation | Action |
|---|---|
| Dependabot PR here bumps an action version | Review and merge — propagates to all callers |
| Dependabot PR on an individual repo for `github-actions` | Close with label `superseded` — the repo has an unmigrated inline workflow |
| Reusable workflow and an individual repo's CI diverge | Migrate the individual repo; remove its inline action pins |

Never add a `github-actions` Dependabot entry to a calling repo that has migrated.

## Local CI Verification — dot-github

This repo has no Python source. Before pushing:

```bash
pre-commit run --all-files
```

## Session Continuity

- Read `LESSONSLEARNED.md` and `CHATHISTORY.md` before resuming work here.
- Update `CHATHISTORY.md` (gitignored) after meaningful sessions.
- Capture new durable lessons in `LESSONSLEARNED.md`.
