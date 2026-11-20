from __future__ import annotations

import importlib.util
from datetime import date
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "resolve_python_versions", Path(__file__).resolve().parents[1] / "scripts" / "resolve_python_versions.py"
)
rpv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rpv)

CYCLES = [
    {"cycle": "3.16", "releaseDate": "2027-10-01", "eol": "2032-10-31"},
    {"cycle": "3.15", "releaseDate": "2026-10-01", "eol": "2031-10-31"},
    {"cycle": "3.14", "releaseDate": "2025-10-07", "eol": "2030-10-31"},
    {"cycle": "3.13", "releaseDate": "2024-10-07", "eol": "2029-10-31"},
    {"cycle": "3.12", "releaseDate": "2023-10-02", "eol": "2028-10-31"},
    {"cycle": "3.9", "releaseDate": "2020-10-05", "eol": "2025-10-31"},
    {"cycle": "2.7", "releaseDate": "2010-07-03", "eol": "2020-01-01"},
]
TODAY = date(2026, 11, 20)


def pyproject(tmp_path: Path, requires: str | None) -> Path:
    path = tmp_path / "pyproject.toml"
    path.write_text("[project]\nname='x'\n" + (f'requires-python = "{requires}"\n' if requires else ""))
    return path


def run(spec, tmp_path, requires=None, cycles=CYCLES, **kw):
    return rpv.resolve(spec, cycles, pyproject(tmp_path, requires), today=TODAY, **kw)


def test_explicit_json_is_passed_through_untouched(tmp_path):
    assert run('["3.10", "3.12"]', tmp_path)[0] == ["3.10", "3.12"]


def test_auto_is_the_newest_three_released_supported_minors(tmp_path):
    assert run("auto", tmp_path)[0] == ["3.13", "3.14", "3.15"]


def test_a_new_release_shifts_the_window(tmp_path):
    versions, _ = rpv.resolve("auto", CYCLES, pyproject(tmp_path, None), today=date(2027, 11, 1))
    assert versions == ["3.14", "3.15", "3.16"]


def test_requires_python_floor_and_ceiling_are_respected(tmp_path):
    assert run("auto", tmp_path, ">=3.14")[0] == ["3.14", "3.15"]
    assert run("auto", tmp_path, ">=3.10,<3.15")[0] == ["3.12", "3.13", "3.14"]


def test_auto_edges_is_floor_and_ceiling(tmp_path):
    assert run("auto-edges", tmp_path, ">=3.10")[0] == ["3.10", "3.15"]  # declared floor, even if EOL
    assert run("auto-edges", tmp_path)[0] == ["3.12", "3.15"]  # no floor declared: oldest supported
    assert run("auto-edges", tmp_path, ">=3.15")[0] == ["3.15"]


def test_count_is_configurable(tmp_path):
    assert run("auto", tmp_path, count=2)[0] == ["3.14", "3.15"]


def test_unreachable_feed_falls_back_with_a_warning(tmp_path):
    versions, warning = rpv.resolve("auto", None, pyproject(tmp_path, None))
    assert versions == rpv.FALLBACK[-3:] and "unreachable" in warning


def test_nothing_satisfies_requires_python_returns_the_floor(tmp_path):
    assert run("auto", tmp_path, ">=3.99")[0] == ["3.99"]


def test_bad_spec_is_rejected(tmp_path):
    try:
        run("latest", tmp_path)
    except ValueError as exc:
        assert "auto" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected ValueError")


def test_bounds_parsing(tmp_path):
    assert rpv.requires_python_bounds(pyproject(tmp_path, ">=3.10")) == ("3.10", None)
    assert rpv.requires_python_bounds(pyproject(tmp_path, ">=3.10, <3.14")) == ("3.10", "3.14")
    assert rpv.requires_python_bounds(tmp_path / "missing.toml") == (None, None)
