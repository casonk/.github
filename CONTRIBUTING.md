# Contributing

Thank you for considering a contribution to this project.

## Ground Rules

- Follow the [Code of Conduct](CODE_OF_CONDUCT.md).
- Open an issue before submitting a large change so the approach can be agreed on first.
- Write clear commit messages using [Conventional Commits](https://www.conventionalcommits.org/).
- Run `pre-commit run --all-files` and ensure all checks pass before opening a pull request.

## Reusable Workflow Changes

When editing a workflow in `.github/workflows/`:

1. The change applies **immediately to every portfolio repo** that calls `@main` — treat it as a deploy.
2. Test the workflow logic in an isolated branch or fork before merging to `main`.
3. Add a note to `CHANGELOG.md` describing the change and any calling-repo impact.

## Dependabot Conflict Strategy

Dependabot is enabled on this repo only (for `github-actions` ecosystem). After a calling repo migrates to use these reusable workflows, it no longer pins action versions directly, so Dependabot on calling repos will not generate `github-actions` PRs.

**Rules:**

| Situation | Action |
|---|---|
| Dependabot PR appears on *this* repo bumping an action | Review and merge — this propagates to all callers |
| Dependabot PR appears on an *individual repo* for `github-actions` | Close it with label `superseded` — the repo likely still has an inline workflow that needs migrating |
| Reusable workflow and an individual repo's inline CI diverge | Migrate the individual repo to the reusable workflow; delete the inline action pins |

**Never add** a `github-actions` Dependabot entry to a calling repo that has already migrated. The canonical pin lives here.
