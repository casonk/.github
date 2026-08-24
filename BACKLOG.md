# BACKLOG.md — dot-github (`casonk/.github`)

Portfolio backlog for this repository. Pending items are candidates for execution —
manually or via crew-chief. Entries sourced from archility audit are tagged
`[archility:YYYY-MM-DD]`; manual entries use `[manual:YYYY-MM-DD]`.

The archility twice-weekly job populates this file automatically via `archility audit --write-backlog`.
To execute a backlog item with crew-chief: `crew-chief agent "Work on item: <item text>"`.
Mark items `[x]` when complete and move them to Done.

## Pending

- [ ] [manual:2026-08-23] **Serve default community health files from this
  repo.** Highest-leverage item in the portfolio's convention backlog. Six
  repos are missing `.github/ISSUE_TEMPLATE/` and
  `.github/PULL_REQUEST_TEMPLATE.md`. GitHub can serve those, plus
  `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and `SECURITY.md`, as account-wide
  defaults from the `.github` repo — closing the column in one place instead
  of six.
  **Verify the visibility interaction before relying on it.** Defaults are
  documented to propagate from a public `.github` repo to public repos, and
  this portfolio is private-first; confirm the private-repo behavior rather
  than assuming it, and fall back to per-repo copies if it does not hold.

- [ ] [manual:2026-08-23] **Add a `## Sudo Boundary` section to `AGENTS.md`.**
  It is the one shared convention this repo is missing —
  `scripts/check_agents_md.py` in traction-control flags it. The check wants
  both halves in any wording: a denial of `sudo` to the agent and a handoff of
  the exact command to the user. Template:
  `../traction-control/docs/templates/AGENTS.md`.

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
