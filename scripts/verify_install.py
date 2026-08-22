#!/usr/bin/env python3
"""Assert that an *already installed* distribution actually works.

Run this from a CI job after `pip install -e .`, on any OS. It reads the repo's
pyproject.toml and then checks the two things a plain `pip install` exit code
does not:

  1. every package the project ships can be imported
  2. every console script in [project.scripts] resolves and runs

Point 2 is the one that matters. `pip install` happily writes a launcher for
`foo = pkg.cli:main` without ever checking that `pkg.cli` exists, so a repo can
publish, install cleanly, and still crash the first time a user types its name.

Exits non-zero with a per-check report if anything fails.
"""

from __future__ import annotations

import argparse
import importlib
import shutil
import subprocess
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover - only taken on 3.9/3.10 runners
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        sys.exit("need Python 3.11+, or `pip install tomli`, to read pyproject.toml")


def discover_modules(repo: Path) -> list[str]:
    for base in (repo / "src", repo):
        if not base.is_dir():
            continue
        found = [
            c.name
            for c in sorted(base.iterdir())
            if c.is_dir()
            and (c / "__init__.py").is_file()
            and not c.name.startswith((".", "_"))
            and c.name not in {"tests", "test"}
        ]
        if found:
            return found
    return []


def check_import(module: str) -> tuple[bool, str]:
    try:
        importlib.import_module(module)
    except Exception as exc:  # noqa: BLE001 - any import failure is a failure
        return False, f"{type(exc).__name__}: {exc}"
    return True, "imported"


def find_script(name: str) -> str | None:
    """Locate an installed console script.

    Look beside the running interpreter before falling back to PATH: scripts
    land in the same bin/Scripts directory as sys.executable, which is correct
    whether or not the venv was 'activated'. Relying on PATH alone reports a
    perfectly good install as broken when the caller invoked .venv/bin/python
    directly.
    """
    bindir = Path(sys.executable).parent
    for candidate in (bindir / name, bindir / f"{name}.exe"):
        if candidate.is_file():
            return str(candidate)
    return shutil.which(name)


def check_script(name: str, target: str, timeout: int) -> tuple[bool, str]:
    exe = find_script(name)
    if exe is None:
        return False, (f"console script {name!r} not found beside "
                       f"{Path(sys.executable).parent} or on PATH after install")
    try:
        proc = subprocess.run([exe, "--help"], capture_output=True, text=True,
                              timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, f"{name} --help timed out after {timeout}s"

    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()
        hint = tail[-1] if tail else f"exit {proc.returncode}"
        return False, f"{name} --help failed ({target}): {hint}"
    return True, f"{name} --help ok"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--repo", default=".", help="repo root (default: cwd)")
    p.add_argument("--timeout", type=int, default=60)
    p.add_argument("--skip-scripts", action="store_true")
    args = p.parse_args()

    repo = Path(args.repo).resolve()
    pyproject = repo / "pyproject.toml"
    if not pyproject.is_file():
        print(f"no pyproject.toml in {repo} — nothing to verify")
        return 0

    with pyproject.open("rb") as fh:
        project = tomllib.load(fh).get("project", {})

    modules = discover_modules(repo)
    scripts = project.get("scripts", {})

    if not modules and not scripts:
        print(f"{project.get('name', repo.name)}: ships no package or console "
              f"script — nothing to verify")
        return 0

    print(f"verifying {project.get('name', repo.name)} on {sys.platform}, "
          f"python {sys.version.split()[0]}")

    failures: list[str] = []

    # Import from a neutral cwd: importing from the repo root can succeed via the
    # source tree even when the *installed* package is broken or missing.
    original = sys.path[:]
    sys.path = [p for p in sys.path if Path(p or ".").resolve() != repo]

    for module in modules:
        ok, detail = check_import(module)
        print(f"  [{'ok' if ok else 'FAIL'}] import {module}: {detail}")
        if not ok:
            failures.append(f"import {module}: {detail}")

    sys.path = original

    if not args.skip_scripts:
        for name, target in sorted(scripts.items()):
            ok, detail = check_script(name, target, args.timeout)
            print(f"  [{'ok' if ok else 'FAIL'}] {detail}")
            if not ok:
                failures.append(detail)

    if failures:
        print(f"\n{len(failures)} check(s) failed:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("\nall install checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
