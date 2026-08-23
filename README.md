# casonk/.github

GitHub account-level configuration for the casonk portfolio: default community health files and reusable CI/CD workflows shared across all repositories.

## Reusable Workflows

Call these from any repository in the `casonk` account using `uses: casonk/.github/.github/workflows/<name>@main`.

| Workflow | Purpose | Key Inputs |
|---|---|---|
| `python-ci.yml` | Matrix Python CI: install, pre-commit, pytest | `python-versions`, `install-extra`, `run-pytest` |
| `install-check.yml` | Installs the package on Linux/macOS/Windows, then asserts every shipped module imports and every console script runs | `python-versions`, `operating-systems`, `install-extra` |
| `secret-scan.yml` | Gitleaks secret scanning (push/PR + scheduled full history) | `gitleaks-version` |
| `python-publish.yml` | Build and publish to PyPI on release | `package-name` |
| `shell-ci.yml` | ShellCheck + optional test script | `run-tests`, `test-script` |
| `docs-ci.yml` | Jekyll / Ruby site build | `ruby-version`, `build-command` |

### Example: Python CI caller

```yaml
# .github/workflows/ci.yml  (in a Python package repo)
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    uses: casonk/.github/.github/workflows/python-ci.yml@main
    with:
      python-versions: '["3.10", "3.12"]'
```

### Example: Install check caller

`python-ci` imports the source tree on ubuntu. `install-check` installs the
distribution the way a user would and then runs its console scripts, on all
three operating systems. The two fail independently: `pip` writes a launcher
for `foo = pkg.cli:main` without checking that `pkg.cli` exists, so a repo can
have a green test suite and a command that dies on first use.

```yaml
# .github/workflows/ci.yml  (in a Python package repo)
jobs:
  install-check:
    uses: casonk/.github/.github/workflows/install-check.yml@main
    with:
      # Floor and ceiling of requires-python is usually enough; this job is
      # about packaging, not behaviour.
      python-versions: '["3.11", "3.14"]'
      install-extra: dev
```

On a **private** repo, consider dropping macOS — Actions minutes are billed and
macOS runners bill at 10x against Windows' 2x:

```yaml
      operating-systems: '["ubuntu-latest", "windows-latest"]'
```

### Pre-commit configuration

`python-ci.yml` runs `pre-commit run --all-files` unconditionally, so **every
repo calling it needs a `.pre-commit-config.yaml`**. Without one the job fails
before it reaches your code:

```
InvalidConfigError: .pre-commit-config.yaml is not a file
```

Copy [`templates/python/.pre-commit-config.yaml`](templates/python/.pre-commit-config.yaml)
to the repo root as a starting point.

That template has **no `black` hook**, unlike the configs currently in most
Python repos here. `ruff-format` covers the same ground — across repos where
both ran, black passed on every file after ruff-format had formatted it — and
`black` 26.x requires Python `>=3.10`. Since pre-commit builds each hook an
environment from the running interpreter, a repo with a 3.9 floor cannot
install the hook at all:

```
ERROR: Package 'black' requires a different Python: 3.9.25 not in '>=3.10'
```

Existing repos with a `>=3.10` floor are unaffected and need no change.

### Example: Secret scan caller

```yaml
# .github/workflows/secret-scan.yml  (in any repo)
name: Secret Scan
on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: "0 3 * * 0"
  workflow_dispatch:

jobs:
  scan:
    uses: casonk/.github/.github/workflows/secret-scan.yml@main
```

### Example: Python publish caller

```yaml
# .github/workflows/python-publish.yml  (in a Python package repo)
name: Publish to PyPI
on:
  release:
    types: [published]

jobs:
  publish:
    uses: casonk/.github/.github/workflows/python-publish.yml@main
    with:
      package-name: my-package
```

## Version Pinning Strategy

All action version pins (`actions/checkout`, `actions/setup-python`, etc.) live **only inside the reusable workflows in this repo**. Dependabot is configured here to keep those pins current weekly. Calling repos do not pin action versions directly — they delegate entirely to these workflows via `@main`.

This means:
- A single Dependabot PR here bumps the action version for every repo in the portfolio simultaneously.
- Calling repos never need per-repo Dependabot PRs for `github-actions` ecosystem updates.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the Dependabot conflict-handling rules.

## Community Health Files

The files `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md` at the root of this repo serve as portfolio-wide defaults. GitHub displays them for any `casonk` repo that does not have its own copy.

## Portfolio Standards

Portfolio-wide governance is maintained in [`./util-repos/traction-control`](https://github.com/casonk/traction-control).

## License

MIT — see [LICENSE](LICENSE).
