# BACKLOG.md — dot-github (`casonk/.github`)

Portfolio backlog for this repository. Pending items are candidates for execution —
manually or via crew-chief. Entries sourced from archility audit are tagged
`[archility:YYYY-MM-DD]`; manual entries use `[manual:YYYY-MM-DD]`.

The archility twice-weekly job populates this file automatically via `archility audit --write-backlog`.
To execute a backlog item with crew-chief: `crew-chief agent "Work on item: <item text>"`.
Mark items `[x]` when complete and move them to Done.

## Pending

- [ ] [manual:2026-08-23] **Correct `REFS-PUBLIC.md:13`,** which still
  documents `gitleaks-action@v2`. Nothing in the portfolio uses it, and it
  cannot consume a baseline file at all — the reason every repo runs the CLI
  with `--baseline-path` instead. Leaving it documented invites someone to
  adopt the action and silently lose baseline suppression.

- [ ] [manual:2026-08-23] **Close the remaining Tier-1 gaps:**
  `docs/contributor-architecture-blueprint.md` and
  `docs/diagrams/repo-architecture.{puml,drawio}`. The `.github/` templates are
  covered by the first item above rather than separately.

## In Progress

## Done

- [x] [manual:2026-08-27] Serve issue and pull-request templates as account-wide
  community-health defaults from this repository.
- [x] [manual:2026-08-28] Add the `## Sudo Boundary` section to `AGENTS.md`.
