# Changelog

## [Unreleased]

### Added
- `python-ci.yml` can measure coverage and upload it to Codecov. Opt in with
  `coverage: true`. Coverage is measured on the last Python in the matrix only and
  uploaded with the `CODECOV_TOKEN` secret (the caller passes
  `secrets: CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}`) or, with
  `coverage-use-oidc: true`, GitHub OIDC (the calling job then needs
  `permissions: id-token: write`). With neither, coverage is measured and the upload
  is skipped with a notice. Inputs: `coverage`, `coverage-source`, `coverage-use-oidc`,
  `coverage-fail-on-error`. Off by default, so existing callers are unchanged.
- `python-ci.yml` takes an optional `runs-on` input (default `ubuntu-latest`, so
  existing callers are unchanged). `ubuntu-latest` is now Ubuntu 26.04, which has
  no Python 3.9; a caller that still tests 3.9 can pass `ubuntu-24.04`.

### Fixed
- Added `python-build.yml` so callers can run the PyPI upload in their own
  workflow. PyPI rejects OIDC tokens issued to a reusable publish job.
  **Calling-repo impact:** migrate `python-publish.yml` callers to a reusable
  build job and a local publish job; the latter references two actions directly.

### Added
- `templates/python/.pre-commit-config.yaml`: canonical pre-commit config for
  Python repos. `python-ci.yml` runs `pre-commit run --all-files`
  unconditionally, so a calling repo without that file fails before reaching
  its own code — a requirement that was previously undocumented. The template
  omits the deprecated `black` hook: `ruff-format` covers the same ground, and
  `black` 26.x requires Python `>=3.10`, so on a repo with a 3.9 floor the hook
  cannot install at all. **Calling-repo impact:** none. Existing configs keep
  working; repos with a `>=3.10` floor need no change.
- README now documents `install-check.yml` in the workflow table with a caller
  example, and the pre-commit requirement above.
- `install-check.yml` reusable workflow: installs a repo from a clean runner on
  Linux, macOS **and Windows**, then asserts every shipped package imports and
  every `[project.scripts]` entry point actually runs. Complements
  `python-ci.yml` rather than replacing it — that one imports the source tree,
  this one exercises the installed distribution, and they fail independently.
  **Calling-repo impact:** opt-in. Nothing changes until a repo adds the job.
- `scripts/verify_install.py`: the check `install-check.yml` runs. Also usable
  standalone after any `pip install -e .`, on any OS.
- `python-ci.yml` reusable workflow: matrix Python CI with pre-commit and pytest, inputs for `python-versions`, `install-extra`, `skip-install`, `run-pytest`
- `secret-scan.yml` reusable workflow: Gitleaks on push/PR and scheduled full-history scan with baseline
- `python-publish.yml` reusable workflow: two-job build + publish to PyPI via OIDC trusted publishing
- `shell-ci.yml` reusable workflow: ShellCheck + optional test script
- `docs-ci.yml` reusable workflow: Jekyll/Ruby site build with configurable Ruby version
- `.github/dependabot.yml`: weekly `github-actions` ecosystem updates scoped to this repo only
- Community health defaults: `CONTRIBUTING.md` (includes Dependabot conflict-handling strategy), `CODE_OF_CONDUCT.md`, `SECURITY.md`
- Portfolio governance baseline: `AGENTS.md`, `LESSONSLEARNED.md`, `REFS-PUBLIC.md`
