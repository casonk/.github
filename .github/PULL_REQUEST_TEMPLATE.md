<!--
Account-wide default. Any repository without its own
.github/PULL_REQUEST_TEMPLATE.md gets this one.
-->

## Description

<!-- What does this PR do, and why is it needed? -->

## Changes

-

## Testing

<!-- How was this validated? Name the commands you actually ran. -->

- [ ] `pre-commit run --all-files` passes
- [ ] Tests pass, or the repo has none and this says so
- [ ] Verified from the main checkout, not only from a worktree

## Checklist

- [ ] No secrets, credentials, or private keys committed
- [ ] No local-only files committed (`CHATHISTORY.md`, `REFS-LOCAL.md`, `*.local.*`)
- [ ] No absolute local paths, internal hostnames, or private repository names in tracked files
- [ ] Tracked examples and fixtures use synthetic placeholders, not real values
- [ ] Any durable lesson was recorded, or this states why none was
- [ ] Commit messages follow conventional format
