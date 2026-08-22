# Changelog

## [Unreleased]

### Added
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
