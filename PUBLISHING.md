# Publishing to PyPI

This document describes how to publish vdsxarray to PyPI.

## Automated Publishing (Recommended)

The project is set up with GitHub Actions for automated testing, building, and publishing.

### Setup Required Secrets

1. **PyPI API Token**:
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token with scope for this project
   - Add it as a GitHub secret named `PYPI_API_TOKEN`

2. **TestPyPI API Token** (optional):
   - Go to https://test.pypi.org/manage/account/token/
   - Create a new API token
   - Add it as a GitHub secret named `TEST_PYPI_API_TOKEN`

### Release Process

1. **Update version numbers**:
   - `pyproject.toml` → `project.version`
   - `vdsxarray/__init__.py` → `__version__`
   - `CHANGELOG.md` → Add new release section

2. **Create and push a version tag**:
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```

3. **The automation will**:
   - Validate version consistency
   - Run all tests across Python versions
   - Build the package
   - Create a GitHub release
   - Publish to PyPI

### GitHub Actions Workflows

- **`ci-cd.yml`**: Main CI/CD pipeline
  - Runs tests on Python 3.9, 3.10, 3.11
  - Linting and formatting checks
  - Builds packages
  - Publishes to TestPyPI on main branch pushes
  - Publishes to PyPI on releases

- **`release.yml`**: Release validation and GitHub release creation
  - Validates version consistency across files
  - Checks CHANGELOG.md entries
  - Creates GitHub releases with release notes

- **`dependencies.yml`**: Dependency management
  - Weekly dependency updates
  - Security audits

## Manual Publishing (Fallback)

### Prerequisites

1. Install publishing dependencies:
```bash
uv sync --group publish
```

2. Set up PyPI account and get API token:
   - Create account at https://pypi.org/
   - Generate API token in account settings
   - Store token securely

## Build and Publish Process

### 1. Update Version
Update version in:
- `pyproject.toml` (project.version)
- `vdsxarray/__init__.py` (__version__)
- `CHANGELOG.md` (add new release section)

### 2. Test the Build
```bash
# Clean previous builds
rm -rf dist/ build/

# Build the package
uv run python -m build

# Check the built packages
ls dist/
```

### 3. Test Installation Locally
```bash
# Install from local build
pip install dist/vdsxarray-*.whl

# Test import
python -c "import vdsxarray; print(vdsxarray.__version__)"
```

### 4. Upload to TestPyPI (Optional)
```bash
# Upload to test PyPI first
uv run twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ vdsxarray
```

### 5. Upload to PyPI
```bash
# Upload to production PyPI
uv run twine upload dist/*
```

### 6. Verify Publication
- Check package appears at: https://pypi.org/project/vdsxarray/
- Test installation: `pip install vdsxarray`

## Automation with GitHub Actions

For automated publishing, create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## Security Notes

- Never commit API tokens to version control
- Use environment variables or GitHub secrets for tokens
- Consider using trusted publishing with OIDC for GitHub Actions
