# Contributor Architecture Blueprint

This document is the architecture map for `casonk/.github`.
Keep it aligned with the real repository layout and execution flow as the repo evolves.

## What This Repository Is

`.github` is GitHub's account-level configuration repository. It has no
application source and nothing to run — its "architecture" is the set of files
GitHub serves to every other repository in the account. There are two surfaces:

- **Reusable workflows** (`.github/workflows/*.yml`, `workflow_call`). Every
  repo's own `ci.yml` / `secret-scan.yml` calls these with `uses:
  casonk/.github/.github/workflows/<name>@main`. A merge to `main` here is a
  portfolio-wide deploy: the next run of every calling repo picks it up. The
  set covers Python CI, install-check, secret scanning, shell CI, docs CI, and
  PyPI publish.
- **Account-default community health files** (`CODE_OF_CONDUCT.md`,
  `CONTRIBUTING.md`, `SECURITY.md`, `.github/ISSUE_TEMPLATE/*`,
  `.github/PULL_REQUEST_TEMPLATE.md`). GitHub serves each of these to any repo
  in the account that does not ship its own copy — private repositories
  included. Editing them is also a portfolio-wide change.

Because both surfaces fan out to every repo, the blast radius of a change here
is the whole account, not this repository. `README.md` documents the concrete
contract; `templates/` holds seed configs consumers copy rather than inherit.

The `docs/diagrams/` sources below are the portfolio-standard starter layout,
kept for consistency with every other repo. For a configuration repository they
carry little structural signal — this section is the meaningful architecture.

## Standard Architecture Assets

- PlantUML source: `docs/diagrams/repo-architecture.puml`
- Draw.io source: `docs/diagrams/repo-architecture.drawio`
- Expected renders after `archility render`:
  - `docs/diagrams/repo-architecture.puml.svg`
  - `docs/diagrams/repo-architecture.puml.png`
  - `docs/diagrams/repo-architecture.drawio.svg`
  - `docs/diagrams/repo-architecture.drawio.png`
- Supplemental Python diagrams after `archility render`:
  - `docs/diagrams/python-import-deps-scripts-verify_install.svg` via `pydeps`
  - `docs/diagrams/python-classes.puml` via `pyreverse`
  - `docs/diagrams/python-classes.puml.svg`
  - `docs/diagrams/python-classes.puml.png`
- Supplemental tooling diagrams after `archility render`:
  - `docs/diagrams/tooling-integrations.puml` via `archility`
  - `docs/diagrams/tooling-integrations.puml.svg`
  - `docs/diagrams/tooling-integrations.puml.png`
- Shared toolchain owner: `../archility` from this repo

## Architecture Authoring Paths

- Programmatic path: `archility generate` builds this starter strictly from repository code and folder markers. This path is deterministic.
- Supplemental introspection path: `archility render` can also derive deterministic sidecar diagrams for detected Python packages/modules, shell scripts, SQL/schema files, and tooling entrypoints.
- Agentic path: an AI agent should inspect the full repository, understand the real execution and dependency boundaries, then rewrite or extend this starter into a repo-specific architecture. This path is intentionally non-deterministic.
- Keep the standard filenames and folder layout even when the agentic path replaces the starter content with a more unique architecture.

## Regeneration

```bash
cd ../archility
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m archility generate .
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m archility render .
```

## Current Focus Roots

- `.github/workflows/` — the reusable workflows every other repo calls
- `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE.md` — account defaults
- `templates/` — seed configs consumers copy rather than inherit
- `scripts/` — maintenance helpers for this repo

## Automation

- `.github/workflows/` holds the reusable, `workflow_call`-triggered workflows.
  They do not validate this repo so much as define the validation every other
  repo runs; `self-secret-scan.yml` is the exception that scans this repo itself.

## Contributor Notes

- Treat this file and the paired `docs/diagrams/` sources as the default architecture handoff surface.
- Treat the supplemental deterministic introspection diagrams as additive sidecars. They do not replace the repo-authored architecture blueprint or the paired repo-architecture sources.
- Expand this starter blueprint with repo-specific flow, dependency, and deployment details when the repository grows beyond the generated baseline.
- Update the blueprint and diagram sources together when folder structure, execution flow, or integration boundaries change.
