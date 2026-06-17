# LESSONSLEARNED.md

Tracked durable lessons for `dot-github` (the `casonk/.github` repo).
Unlike `CHATHISTORY.md`, this file should keep only reusable lessons that should change how future sessions work in this repo.

## How To Use

- Read this file after `AGENTS.md` and before `CHATHISTORY.md` when resuming work.
- Add lessons that generalize beyond a single session.
- Keep entries concise and action-oriented.
- Do not use this file for transient status updates or full session logs.
- Before final reporting for meaningful work, either add any durable lesson
  discovered during the request or explicitly report why no durable lesson was
  added.

## Lessons

- Reusable workflow changes on `main` take effect immediately for every calling repo — treat merges to `main` as a portfolio-wide deploy, not just a local change.
- Calling repos reference workflows via `@main` (not a semver tag), so Dependabot on individual calling repos will not generate `github-actions` PRs — no conflict with the central Dependabot here.
- When a new action version (e.g., `actions/checkout@v7`) is released, the single Dependabot PR here is the only update needed; all callers inherit it automatically on next run.
- Document the repository around its real execution, curation, or integration flow instead of only the top-level folder list.
- Keep tracked examples, fixtures, and `.example` templates scrubbed of real paths, usernames, hostnames, account identifiers, or other instance-specific values; real operator data belongs only in gitignored local config.
