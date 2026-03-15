# Contributing to VDS Xarray Backend

Thank you for your interest in contributing to vdsxarray! This document provides guidelines for contributing to the project.

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/gavargas22/vds-xarray-backend.git
   cd vds-xarray-backend
   ```

2. **Install dependencies**:
   ```bash
   uv sync --group dev --group test
   ```

3. **Install pre-commit hooks** (optional but recommended):
   ```bash
   uv add --dev pre-commit
   uv run pre-commit install
   ```

## Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**

3. **Run tests**:
   ```bash
   uv run pytest tests/ -v
   ```

4. **Run linting and formatting**:
   ```bash
   uv run ruff check vdsxarray/ tests/
   uv run black vdsxarray/ tests/
   uv run isort vdsxarray/ tests/
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **Push and create a pull request**:
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

- We use [Black](https://black.readthedocs.io/) for code formatting
- We use [Ruff](https://docs.astral.sh/ruff/) for linting
- We use [isort](https://pycqa.github.io/isort/) for import sorting
- Line length is set to 88 characters
- Follow PEP 8 guidelines

## Testing

- Write tests for new features and bug fixes
- Ensure all tests pass before submitting a PR
- Aim for good test coverage
- Place tests in the `tests/` directory
- Use descriptive test names

## Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test-related changes
- `refactor:` for code refactoring
- `chore:` for maintenance tasks

Example:
```
feat: add support for reading VDS metadata

- Extract coordinate information from VDS headers
- Add metadata validation
- Update tests and documentation
```

## Pull Request Process

1. **Ensure your PR has a clear title and description**
2. **Reference any related issues** using `Fixes #123` or `Closes #123`
3. **Ensure all checks pass** (tests, linting, etc.)
4. **Request review** from maintainers
5. **Address any feedback** promptly

## Reporting Issues

When reporting issues, please include:

- vdsxarray version
- Python version
- Operating system
- Steps to reproduce the issue
- Expected vs actual behavior
- Relevant code snippets or error messages

## Questions?

Feel free to open an issue for questions or reach out to the maintainers.

Thank you for contributing! 🚀
