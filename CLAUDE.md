# CLAUDE.md

> Guidance for Claude Code and other AI assistants working in this repository.
> For human contributors, see `CONTRIBUTING.md`. For other AI agents, see `AGENTS.md`.

---

## Project Overview

**vdsxarray** — An xarray backend engine for reading VDS (Volume Data Store) seismic data files.

Users access it via: `xr.open_dataset("file.vds", engine="vds")`

- **Language**: Python 3.9–3.11
- **Build system**: Hatchling
- **Package manager**: uv
- **Version source of truth**: `pyproject.toml` → `project.version` (currently `1.0.1`)
- **Package name on PyPI**: `vdsxarray`

---

## Domain Background

VDS is a cloud-optimized format for 3D seismic survey data (Bluware/OSDU). The data model is a **3D volume** with three named axes:

| Dimension   | Axis Index | Type      | Description                   |
|-------------|------------|-----------|-------------------------------|
| `inline`    | 0          | `int16`   | Survey line direction         |
| `crossline` | 1          | `int16`   | Perpendicular to inline       |
| `sample`    | 2          | `float32` | Time or depth (vertical axis) |

Amplitude values are `float32`. This dimension order (`inline`, `crossline`, `sample`) is the **public API contract** and must not change.

---

## Repository Structure

```
vdsxarray/
  __init__.py        # Exports: VdsEngine, __version__ (= "1.0.0" — see Known Issues)
  vds.py             # Core: VdsEngine, VdsBackendArray, coordinate extraction
  utils.py           # Helpers: get_vds_metadata, estimate_chunk_size
tests/
  test_basic.py      # Structural unit tests (import, version, attribute checks)
docs/                # User-facing markdown documentation
  README.md          # Documentation hub and quick-start
  TECHNICAL-OVERVIEW.md
  USER-GUIDE.md
  WHY-XARRAY.md
  RELEASE-GUIDE.md
notebooks/           # Jupyter example notebooks
scripts/
  release.sh         # Release automation script
.github/             # CI/CD (workflows not yet present in repo)
pyproject.toml       # Project metadata, dependencies, tool config
AGENTS.md            # AI agent guidance (more detailed domain notes)
CONTRIBUTING.md      # Human contributor guide
```

---

## Core Architecture

All key logic lives in `vdsxarray/vds.py`:

### 1. `get_annotated_coordinates(vds)`
Extracts inline/crossline/sample coordinate arrays from VDS axis metadata using `np.linspace`. Maps `vds.axes[0]` → inline, `vds.axes[1]` → crossline, `vds.axes[2]` → sample.

> **Known issue**: The docstring states the opposite axis order from the code. Do not "fix" based on the docstring alone — verify against real VDS files first.

### 2. `VdsBackendArray(BackendArray)`
Wraps a `VDS` reader for xarray's lazy indexing protocol.
- `__getitem__` uses `explicit_indexing_adapter`
- `_raw_indexing_method` translates xarray index types (slices, arrays, ints) to VDS slice reads
- Returns squeezed arrays to remove singleton dimensions

### 3. `VdsEngine(BackendEntrypoint)`
The xarray backend entry point (registered as `xarray.backends.vds`).
- `open_dataset()`: Opens VDS, builds coordinates, wraps data in `LazilyIndexedArray`, returns chunked `xr.Dataset` with 128×128×128 dask chunks
- `guess_can_open()`: Returns `True` for `.vds` file extensions

### 4. `get_cdp_coordinates(vds)` — **Stub, returns `None`**

### Utilities (`vdsxarray/utils.py`)
- `get_vds_metadata(vds)` — shape, axes_info, dtype dict
- `estimate_chunk_size(shape, target_mb=64)` — cubic chunk calculator (currently **commented out** in `vds.py`; 128×128×128 hardcoded instead)

---

## Development Workflow

### Setup
```bash
uv sync --group dev --group test
```

### Run Tests
```bash
uv run pytest                        # All tests
uv run pytest -m "not slow"          # Skip slow tests
uv run pytest -m "not integration"   # Skip integration tests
uv run pytest --cov=vdsxarray        # With coverage
```

### Linting (all three must pass before committing)
```bash
uv run ruff check .
uv run black --check .
uv run isort --check-only .
```

### Auto-fix Lint Issues
```bash
uv run ruff check . --fix
uv run black .
uv run isort .
```

### Pre-commit Hooks
Configured in `.pre-commit-config.yaml`. Runs: trailing-whitespace, YAML/TOML checks, ruff (with `--fix`), ruff-format, mypy.

---

## Code Style Conventions

| Tool     | Config                                      |
|----------|---------------------------------------------|
| Black    | line-length 88, target py39/py310/py311     |
| Ruff     | rules E,W,F,I,B,C4,UP; ignore E501, B008   |
| isort    | profile: black, line_length: 88             |
| mypy     | `--ignore-missing-imports`, targets `vdsxarray/` |

- **Docstrings**: NumPy style (see existing examples in `vds.py`)
- **Quotes**: Double quotes (Black default)
- **Python minimum**: 3.9 — no `match`, no `X | Y` union syntax in annotations, no walrus operators in comprehensions

---

## Commit Message Format

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

## Testing Guidelines

**Current state**: 4 structural unit tests in `tests/test_basic.py` (import, version, attributes, exports). No integration tests exist yet.

**Adding tests**:
- Use `@pytest.mark.slow` and `@pytest.mark.integration` for tests requiring VDS files
- Do **not** commit VDS test data (files are too large)
- **Mock `ovds_utils.vds.VDS`** for unit tests that exercise `VdsBackendArray` / `VdsEngine` logic without file I/O
- Use `pytest-cov` for coverage reporting

---

## Dependencies

**Runtime** (do not add without explicit approval):
- `xarray>=2024.7.0` — backend protocol
- `dask>=2024.8.0` — lazy/chunked loading
- `openvds>=3.4.6` — C++ SDK with Python bindings (do not call directly)
- `ovds-utils>=0.3.1` — Python wrapper; **primary interface** used in this codebase

**Dev/test**: pytest, pytest-cov, black, ruff, isort, mypy, ipykernel, matplotlib, scipy

---

## CI/CD & Release

The pipeline (`.github/workflows/build-and-publish-wheels.yml`) triggers on push to `main`:
1. Reads version from `pyproject.toml`, creates a git tag
2. Builds wheel with uv + Python 3.11
3. Creates a GitHub Release with checksums
4. Uploads wheel to JFrog Artifactory

Manual release: `./scripts/release.sh`

**Secrets required**: `PAT_TOKEN`, AWS credentials, Artifactory credentials (managed externally).

---

## Known Issues

1. **Version mismatch**: `vdsxarray/__init__.py` has `__version__ = "1.0.0"` but `pyproject.toml` says `1.0.1`. The `pyproject.toml` is authoritative.

2. **Hardcoded chunk size**: `estimate_chunk_size()` in `utils.py` is implemented but commented out in `vds.py`. Chunks are hardcoded as 128×128×128.

3. **Stub function**: `get_cdp_coordinates()` is defined but always returns `None`.

4. **Axis order mismatch in docstring**: `get_annotated_coordinates` docstring says axis 0=sample, 1=crossline, 2=inline, but the code maps axis 0→inline, 1→crossline, 2→sample. Do not "fix" without real-file validation.

5. **Dimension order inconsistency in utils**: `estimate_chunk_size` returns keys in `{sample, crossline, inline}` order (index 0→sample), but `VdsEngine` uses `(inline, crossline, sample)` order.

6. **Silent exception swallowing**: VDS cleanup block in `VdsEngine.open_dataset()` uses bare `except Exception: pass` with no logging.

---

## Hard Rules for AI Assistants

- **Do not add runtime dependencies** without explicit approval.
- **Do not rename the entry point** `xarray.backends.vds` — downstream users depend on `engine="vds"`.
- **Do not rename dimensions** `inline`, `crossline`, `sample` — these are the public API.
- **Do not suppress type errors** with `# type: ignore` or casts to `Any` — fix them properly.
- **Never eagerly load volume data** — all data access must flow through `VdsBackendArray` → dask.
- **Do not call `openvds` directly** — always use `ovds-utils` (`ovds_utils.vds.VDS`).
- **Mock VDS in unit tests** rather than requiring real VDS files.
- **Stay within Python 3.9 syntax** — no `match`, no `X | Y` type unions, no 3.10+ features.
- **Do not push to `main` directly** — changes go through branches and PRs.
