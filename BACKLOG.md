# BACKLOG.md — dot-github (`casonk/.github`)

Portfolio backlog for this repository. Pending items are candidates for execution —
manually or via crew-chief. Entries sourced from archility audit are tagged
`[archility:YYYY-MM-DD]`; manual entries use `[manual:YYYY-MM-DD]`.

The archility twice-weekly job populates this file automatically via `archility audit --write-backlog`.
To execute a backlog item with crew-chief: `crew-chief agent "Work on item: <item text>"`.
Mark items `[x]` when complete and move them to Done.

## Pending

- [ ] [manual:2026-10-15] **Ask GitHub Support to purge pre-rewrite commits** — this
  repository's published history was rewritten (most recently on 2026-10-15,
  to remove per-commit AI attribution trailers). GitHub keeps serving the old
  commits to anyone with a hash, and through the read-only `refs/pull/*` refs
  of earlier pull requests, until Support garbage-collects them. The request
  is filed once for the whole portfolio from traction-control's backlog; mark
  this done when an old hash returns 404 here. Never push an old clone's
  history back.

## In Progress

## Done

- [x] [manual:2026-08-27] Serve issue and pull-request templates as account-wide
  community-health defaults from this repository.
- [x] [manual:2026-08-28] Add the `## Sudo Boundary` section to `AGENTS.md`.
- [x] [manual:2026-08-28] Correct the public Gitleaks reference to the
  baseline-aware CLI implementation and add the Tier-1 architecture blueprint
  with editable PlantUML and draw.io diagrams.
