# AGENTS.md

> For AI coding agents working on this repository. Not intended for human contributors — see `CONTRIBUTING.md` for that.

---

## Project Identity

**vdsxarray** — An xarray backend engine for reading VDS (Volume Data Store) seismic data files. Registered as an xarray backend entry-point so users can call `xr.open_dataset("file.vds", engine="vds")`.

- **Language**: Python (3.9–3.11)
- **Build system**: Hatchling
- **Package manager**: uv
- **Version**: Defined in `pyproject.toml` (`project.version`). The `__init__.py` version string exists but is **not the source of truth** — see Known Issues.

---

## Domain Primer — VDS & Seismic Data

VDS (Volume Data Store) is a cloud-optimized format for storing 3D seismic survey data, developed by Bluware/OSDU. The core abstraction is a **3D volume** with three axes:

| Dimension   | Axis Index | Description                        | dtype     |
|-------------|------------|------------------------------------|-----------|
| `inline`    | 0          | Survey line direction              | `int16`   |
| `crossline` | 1          | Perpendicular to inline            | `int16`   |
| `sample`    | 2          | Time or depth (vertical axis)      | `float32` |

The volume data itself is `float32` amplitude values.

**Key libraries this project depends on:**

- **`openvds`** (>= 3.4.6) — Bluware's C++ SDK with Python bindings for VDS file access.
- **`ovds-utils`** (>= 0.3.1) — A Python convenience wrapper around `openvds`. Provides the `VDS` class used throughout this codebase. This is the primary interface to VDS data — the code does **not** call `openvds` directly.
- **`xarray`** (>= 2024.7.0) — The backend engine protocol (`BackendEntrypoint`) that this package implements.
- **`dask`** (>= 2024.8.0) — Used for lazy/chunked loading of seismic volumes.

When working with this code, understand that axis ordering in VDS files and in the xarray Dataset may not match. The `get_annotated_coordinates` function maps VDS axes to the `(inline, crossline, sample)` dimension order used throughout the Dataset.

---

## Repository Structure

```
vdsxarray/
  __init__.py        # Package exports: VdsEngine, __version__
  vds.py             # Core module — engine, backend array, coordinate extraction
  utils.py           # Metadata extraction, chunk size estimation (partially used)
tests/
  test_basic.py      # Unit tests (import, version, structure checks)
scripts/
  release.sh         # Release automation script
docs/                # User-facing documentation (markdown)
notebooks/           # Jupyter notebooks (examples/exploration)
.github/workflows/   # CI/CD — build, tag, publish to Artifactory + GitHub Releases
```

### Core Architecture (all in `vdsxarray/vds.py`)

1. **`get_annotated_coordinates(vds)`** — Extracts inline/crossline/sample coordinate arrays from VDS axis metadata using `np.linspace`.

2. **`VdsBackendArray(BackendArray)`** — Wraps a `VDS` reader object for xarray's lazy indexing protocol. Implements `__getitem__` via `explicit_indexing_adapter` and a `_raw_indexing_method` that translates xarray index types (slices, arrays, ints) into VDS slice reads.

3. **`VdsEngine(BackendEntrypoint)`** — The xarray backend engine. Registered as entry-point `xarray.backends.vds`. `open_dataset()` opens a VDS file, builds coordinates, wraps in `LazilyIndexedArray`, and returns a chunked `xr.Dataset` (128x128x128 chunks).

4. **`get_cdp_coordinates(vds)`** — Stub function (returns `None`). Placeholder for future CDP coordinate calculation.

### Utilities (`vdsxarray/utils.py`)

- `get_vds_metadata(vds)` — Extracts shape, axis info, data type into a dict.
- `estimate_chunk_size(shape, target_mb=64)` — Calculates roughly-cubic chunk sizes. Currently **commented out** in `vds.py` (hardcoded 128x128x128 is used instead).

---

## Development Commands

```bash
# Setup
uv sync --group dev --group test

# Run tests
uv run pytest

# Linting (all three must pass)
uv run ruff check .
uv run black --check .
uv run isort --check-only .

# Auto-fix lint issues
uv run ruff check . --fix
uv run black .
uv run isort .
```

Pre-commit hooks are configured (`.pre-commit-config.yaml`) and run: trailing whitespace fix, YAML/TOML checks, ruff (with `--fix`), ruff-format, and mypy.

---

## Code Style & Conventions

- **Formatter**: Black (line-length 88)
- **Linter**: Ruff — rules: E, W, F, I, B, C4, UP. E501 ignored (Black handles line length).
- **Import sorting**: isort (profile: black)
- **Type checking**: mypy (configured in pre-commit, `--ignore-missing-imports`, targets `vdsxarray/`)
- **Docstrings**: NumPy-style (see existing docstrings in `vds.py` for examples)
- **Target Python**: 3.9 minimum — do not use syntax/features exclusive to 3.10+ (e.g., `match` statements, `X | Y` union types in annotations)
- **Quote style**: Double quotes (per Black default)

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add CDP coordinate extraction
fix: handle empty VDS axes gracefully
docs: update technical overview
test: add integration tests for VdsEngine
refactor: extract coordinate logic to utils
chore: bump openvds dependency
```

---

## Testing

### Current State

Tests are minimal — `tests/test_basic.py` contains 4 structural tests:
- Version string existence
- `VdsEngine` import
- `open_dataset` method presence
- `__all__` exports

There are **no integration tests** that open real VDS files. The `@pytest.mark.integration` marker is configured but unused.

### Testing Direction

Integration tests should be added. When writing tests:

- Use `pytest` with markers `slow` and `integration` for tests requiring VDS files.
- Test data should not be committed to the repo (VDS files are large).
- Mock `ovds_utils.vds.VDS` for unit tests that exercise `VdsBackendArray` and `VdsEngine` logic without file I/O.
- Use `pytest-cov` for coverage (source: `vdsxarray/`, omits test files).

### Running Tests

```bash
uv run pytest                          # All tests
uv run pytest -m "not slow"            # Skip slow tests
uv run pytest -m "not integration"     # Skip integration tests
uv run pytest --cov=vdsxarray          # With coverage
```

---

## CI/CD & Release

### Pipeline (`.github/workflows/build-and-publish-wheels.yml`)

Triggers on push to `main` or manual dispatch. Steps:

1. **create-tag** — Reads version from `pyproject.toml`, creates/updates a git tag.
2. **build-wheels** — Builds wheel using `uv` + Python 3.11.
3. **collect-and-publish** — Creates a GitHub Release with checksums.
4. **upload-to-artifactory** — Publishes wheel to internal JFrog Artifactory (`dgeo-team-pypi/vdsxarray/{VERSION}/`).

### Release Process

Version is the **single source of truth** in `pyproject.toml` → `project.version`. Pushing to `main` triggers the full pipeline automatically. Manual release is also available via `./scripts/release.sh`.

### Important CI Details

- Artifactory upload uses a self-hosted EC2 runner (started/stopped per build).
- Secrets required: `PAT_TOKEN`, AWS credentials, Artifactory credentials.
- The pipeline force-pushes tags — existing tags for the same version are overwritten.

---

## Known Issues

1. **Version mismatch**: `__init__.py` has `__version__ = "1.0.0"` but `pyproject.toml` says `1.0.1`. The pyproject.toml is authoritative. The `__init__.py` version should be updated or derived dynamically.

2. **Commented-out chunking logic**: In `VdsEngine.open_dataset()`, the `estimate_chunk_size` utility is imported and called in commented-out code (lines ~187–194). Hardcoded 128x128x128 chunks are used instead.

3. **Stub function**: `get_cdp_coordinates()` is defined but unimplemented (returns `None`).

4. **Coordinate docstring/code mismatch**: The docstring for `get_annotated_coordinates` says axis 0 = samples, axis 1 = crosslines, axis 2 = inlines. But the code does: `inlines = vds.axes[0]`, `xlines = vds.axes[1]`, `samples = vds.axes[2]` — which is the inverse mapping. The variable naming and actual axis semantics may need verification against real VDS files.

5. **`utils.py` dimension order inconsistency**: `estimate_chunk_size` returns keys `{'sample': ..., 'crossline': ..., 'inline': ...}` mapping shape indices 0→sample, 1→crossline, 2→inline. But `VdsEngine` uses dimension order `(inline, crossline, sample)`. If the util is un-commented, the chunk dict keys won't match the Dataset dimension ordering.

6. **Silent exception swallowing**: In `VdsEngine.open_dataset()`, the VDS cleanup block (`vds.accessor.commit()` / `removeReference()`) uses a bare `except Exception: pass`. If cleanup fails, there's no logging or warning.

---

## Guardrails for Agents

- **Do not add dependencies** without explicit approval. The dependency set is intentionally small.
- **Do not change the entry-point name** (`xarray.backends.vds`) — downstream users depend on `engine="vds"`.
- **Do not change dimension names** (`inline`, `crossline`, `sample`) — these are the public API contract.
- **Do not suppress type errors** with `as any`, `# type: ignore`, or equivalent. Fix them properly.
- **Mock `ovds_utils.vds.VDS`** in tests rather than requiring real VDS files.
- **Preserve lazy loading** — never eagerly load the full volume into memory. All data access must go through `VdsBackendArray` → dask.
- **Test against Python 3.9** syntax constraints. No walrus operators in comprehensions, no `match`, no `type X = Y`.
