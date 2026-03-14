Contributing
============

Thank you for your interest in contributing to vdsxarray!

For Humans
----------

This section is for human contributors. If you're an AI coding agent, please see :doc:`ai-agents/index`.

Getting Started
---------------

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up your development environment

Development Setup
-----------------

.. code-block:: bash

   git clone https://github.com/YOUR_USERNAME/vds-xarray-backend.git
   cd vds-xarray-backend
   uv sync --group dev --group test

Code Style
----------

We use:

- **Black** for code formatting
- **Ruff** for linting
- **isort** for import sorting
- **mypy** for type checking

Run all checks:

.. code-block:: bash

   uv run black --check .
   uv run ruff check .
   uv run isort --check-only .

Auto-fix issues:

.. code-block:: bash

   uv run black .
   uv run ruff check . --fix
   uv run isort .

Testing
-------

Run tests:

.. code-block:: bash

   uv run pytest

With coverage:

.. code-block:: bash

   uv run pytest --cov=vdsxarray

Commit Messages
---------------

Follow `Conventional Commits <https://www.conventionalcommits.org/>`_:

.. code-block:: text

   feat: add new feature
   fix: resolve bug
   docs: update documentation
   test: add tests
   refactor: improve code structure

Pull Requests
-------------

1. Create a feature branch
2. Make your changes
3. Add tests
4. Update documentation
5. Submit a pull request

For more details, see :doc:`CONTRIBUTING`.

Questions?
----------

Open an issue on `GitHub <https://github.com/gavargas22/vds-xarray-backend/issues>`_.
