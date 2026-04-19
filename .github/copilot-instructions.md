# Copilot Instructions

## Python Style

- Prefer module-level imports over function- or method-level imports.
- All new code must include type annotations (PEP 484). Use `from __future__ import annotations` only when needed for forward references.
- Use `|` for union types (e.g. `int | None`) rather than `Optional[int]` or `Union[int, None]`.
- Prefer `@cached_property` (from `functools`) over manual caching patterns where appropriate.
- Format code with Black (run `bash lint.sh`). Do not hand-format; let Black decide line breaks and spacing.
- Follow existing naming conventions: `snake_case` for functions, methods, variables; `PascalCase` for classes.
- License header `# SPDX-License-Identifier: GPL-2.0+` must appear at the top of every new source file.

## Tests

- Every new public method or class must have corresponding pytest tests.
- Tests live in `tests/` with the prefix `test_`. Group related tests in a class named `TestXxx`.
- Use an `autouse=True` fixture named `load` to set up `gf.Module` instances; use `os.path.join` for paths (Windows compatibility).
- Prefer plain `assert` statements; use `pytest.raises` for expected exceptions.
- Computationally expensive or repetitive tests (e.g. looping over many files) must be guarded with `@pytest.mark.skipif` when running under coverage (check `os.environ["PYTEST_COVERAGE"] == "1"`).
- Run tests with `python -m pytest` (parallel via pytest-xdist by default).

## Test Fortran Sources

- Fortran test sources go in `tests/src/` with a `.f90` extension; all code must live inside a `module`.
- Pre-compiled plain-text modules go in `tests/txt/` with a `.mod.txt` extension (extracted via `gunzip < file.mod > file.mod.txt`).
- Do not commit binary `.mod` files; only compiled `.mod` files produced at test-time (in `tests/build/`) are acceptable.
- Add new `.f90` files to `tests/Makefile` and new `.mod.txt` files to `tests/txt/README`.

## Type Checking

- The project uses mypy for static analysis (`extras: types`). New code must be mypy-clean.
- Avoid `Any` unless interfacing with truly untyped external data; prefer narrowing with `isinstance` guards.

## Security

- Never call `eval` or `exec` on module file content; all parsing must use the existing `bracket_split` / regex approach.
- Validate external inputs (file paths, version strings) at the boundary (`gf.Module.__init__`), not deep in parsing helpers.
