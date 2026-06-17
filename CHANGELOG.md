# Changelog

## [Unreleased]

### Added
- `python-ci.yml` reusable workflow: matrix Python CI with pre-commit and pytest, inputs for `python-versions`, `install-extra`, `run-pytest`
- `secret-scan.yml` reusable workflow: Gitleaks on push/PR and scheduled full-history scan with baseline
- `python-publish.yml` reusable workflow: two-job build + publish to PyPI via OIDC trusted publishing
- `shell-ci.yml` reusable workflow: ShellCheck + optional test script
- `docs-ci.yml` reusable workflow: Jekyll/Ruby site build with configurable Ruby version
- `.github/dependabot.yml`: weekly `github-actions` ecosystem updates scoped to this repo only
- Community health defaults: `CONTRIBUTING.md` (includes Dependabot conflict-handling strategy), `CODE_OF_CONDUCT.md`, `SECURITY.md`
- Portfolio governance baseline: `AGENTS.md`, `LESSONSLEARNED.md`, `REFS-PUBLIC.md`
