#!/usr/bin/env python3
"""Resolve the Python versions a CI matrix should test, so no repo hard-codes them.

``--spec`` is what the caller passed as ``python-versions``:

* a JSON array (``["3.10", "3.12"]``) is passed through unchanged;
* ``auto``       -> the newest ``--count`` (default 3) supported CPython minors;
* ``auto-edges`` -> the declared ``requires-python`` floor (else the oldest supported minor) and the
  newest supported minor: an install-check's floor and ceiling.

"Supported" means released and not yet end-of-life according to endoflife.date, narrowed by the
repository's own ``requires-python`` (a ``>=X.Y`` floor and a ``<X.Y`` ceiling). When the feed is
unreachable a built-in list is used and a warning is printed, so CI still runs.

Prints a JSON array on stdout; with ``--github-output FILE`` it also appends ``versions=<json>``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

FEED = "https://endoflife.date/api/python.json"
FALLBACK = ["3.12", "3.13", "3.14", "3.15"]


def minor_key(minor: str) -> tuple[int, int]:
    major, _, rest = minor.partition(".")
    return int(major), int(rest)


def fetch_cycles(retries: int = 3) -> list[dict]:
    last: Exception | None = None
    for attempt in range(retries):
        try:
            request = urllib.request.Request(FEED, headers={"User-Agent": "casonk-dot-github"})
            with urllib.request.urlopen(request, timeout=20) as response:  # noqa: S310
                return json.load(response)
        except Exception as exc:  # pylint: disable=broad-except
            last = exc
            time.sleep(2**attempt)
    raise RuntimeError(f"endoflife.date unreachable: {last}")


def supported_minors(cycles: list[dict], today: date) -> list[str]:
    now = today.isoformat()
    found = []
    for cycle in cycles:
        minor = str(cycle.get("cycle", ""))
        released = str(cycle.get("releaseDate") or "9999-12-31")
        eol = cycle.get("eol")
        alive = eol is False or (isinstance(eol, str) and eol > now)
        if re.fullmatch(r"3\.\d+", minor) and released <= now and alive:
            found.append(minor)
    return sorted(found, key=minor_key)


def requires_python_bounds(pyproject: Path) -> tuple[str | None, str | None]:
    """(floor, ceiling) minors from ``requires-python`` (``>=3.10,<3.15``), else (None, None)."""
    try:
        text = pyproject.read_text(encoding="utf-8")
    except OSError:
        return None, None
    match = re.search(r'^\s*requires-python\s*=\s*["\']([^"\']+)["\']', text, re.MULTILINE)
    if not match:
        return None, None
    spec = match.group(1)
    floor = re.search(r">=\s*(3\.\d+)", spec)
    ceiling = re.search(r"<\s*(3\.\d+)(?!\.\d*[1-9])", spec)
    return (floor.group(1) if floor else None, ceiling.group(1) if ceiling else None)


def resolve(
    spec: str,
    cycles: list[dict] | None,
    pyproject: Path,
    count: int = 3,
    today: date | None = None,
) -> tuple[list[str], str | None]:
    """Returns (versions, warning)."""
    spec = spec.strip()
    if spec.startswith("["):
        return [str(v) for v in json.loads(spec)], None
    if spec not in {"auto", "auto-edges"}:
        raise ValueError(f"python-versions must be a JSON array, 'auto' or 'auto-edges', got {spec!r}")
    warning = None
    if cycles is None:
        candidates = list(FALLBACK)
        warning = "endoflife.date unreachable; using the built-in Python list"
    else:
        candidates = supported_minors(cycles, today or date.today())
    floor, ceiling = requires_python_bounds(pyproject)
    if floor:
        candidates = [c for c in candidates if minor_key(c) >= minor_key(floor)]
    if ceiling:
        candidates = [c for c in candidates if minor_key(c) < minor_key(ceiling)]
    if not candidates:
        return ([floor] if floor else [FALLBACK[-1]]), warning
    if spec == "auto-edges":
        # The floor a repo declares is what it claims to support, so test it even once it is EOL.
        return sorted({floor or candidates[0], candidates[-1]}, key=minor_key), warning
    return candidates[-count:], warning


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--spec", required=True)
    parser.add_argument("--pyproject", default="pyproject.toml")
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument("--github-output")
    args = parser.parse_args(argv)
    cycles = None
    if not args.spec.strip().startswith("["):
        try:
            cycles = fetch_cycles()
        except RuntimeError:
            cycles = None
    versions, warning = resolve(args.spec, cycles, Path(args.pyproject), args.count)
    if warning:
        print(f"::warning title=Python versions::{warning}", file=sys.stderr)
    out = json.dumps(versions)
    print(out)
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as handle:
            handle.write(f"versions={out}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
