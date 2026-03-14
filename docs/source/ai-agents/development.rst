Development for AI Agents
==========================

Code Style & Conventions
-------------------------

Formatter
~~~~~~~~~

**Black** (line-length 88)

.. code-block:: bash

   uv run black .

Linter
~~~~~~

**Ruff** — rules: E, W, F, I, B, C4, UP

E501 ignored (Black handles line length)

.. code-block:: bash

   uv run ruff check .
   uv run ruff check . --fix

Import Sorting
~~~~~~~~~~~~~~

**isort** (profile: black)

.. code-block:: bash

   uv run isort .

Type Checking
~~~~~~~~~~~~~

**mypy** (configured in pre-commit)

- ``--ignore-missing-imports``
- Targets ``vdsxarray/`` directory

.. important::
   Do NOT suppress type errors with ``# type: ignore``. Fix them properly.

Docstrings
~~~~~~~~~~

**NumPy-style** docstrings

Example from ``vds.py``:

.. code-block:: python

   def get_annotated_coordinates(vds: VDS):
       """
       Extract coordinate arrays from a VDS object.

       Parameters
       ----------
       vds : VDS
           A VDS object containing axes information

       Returns
       -------
       tuple[np.ndarray, np.ndarray, np.ndarray]
           A tuple containing (inlines, xlines, samples)

       Notes
       -----
       The function assumes a 3D seismic volume.
       """

Target Python Version
~~~~~~~~~~~~~~~~~~~~~

**Python 3.9 minimum**

Do NOT use syntax exclusive to 3.10+:

- ❌ ``match`` statements
- ❌ ``X | Y`` union types in annotations
- ❌ Walrus operators in comprehensions (sometimes works, but avoid)

Use Python 3.9-compatible alternatives:

.. code-block:: python

   # Good (3.9+)
   from typing import Union
   def func(x: Union[int, str]):
       pass

   # Bad (3.10+)
   def func(x: int | str):
       pass

Quote Style
~~~~~~~~~~~

**Double quotes** (per Black default)

.. code-block:: python

   # Good
   message = "Hello, world"

   # Bad
   message = 'Hello, world'

Commit Messages
---------------

Follow `Conventional Commits <https://www.conventionalcommits.org/>`_:

Format
~~~~~~

.. code-block:: text

   <type>: <description>

   [optional body]

   [optional footer]

Types
~~~~~

- ``feat``: New feature
- ``fix``: Bug fix
- ``docs``: Documentation changes
- ``test``: Adding or updating tests
- ``refactor``: Code refactoring
- ``chore``: Maintenance tasks
- ``perf``: Performance improvements
- ``style``: Code style changes (formatting)
- ``ci``: CI/CD changes

Examples
~~~~~~~~

.. code-block:: text

   feat: add CDP coordinate extraction

   Implements get_cdp_coordinates() to calculate CDP locations
   from VDS inline/crossline metadata.

.. code-block:: text

   fix: handle empty VDS axes gracefully

   Previously crashed when VDS file had zero-length axes.
   Now returns empty coordinate arrays.

.. code-block:: text

   docs: update technical overview

   Added section on coordinate system mapping.

.. code-block:: text

   test: add integration tests for VdsEngine

   Tests cover basic file opening, coordinate extraction,
   and lazy loading behavior.

.. code-block:: text

   refactor: extract coordinate logic to utils

   Moved get_annotated_coordinates to utils module for
   better organization.

.. code-block:: text

   chore: bump openvds dependency

   Updated openvds from 3.4.6 to 3.5.0 for bug fixes.

Pre-commit Hooks
----------------

Configured in ``.pre-commit-config.yaml``:

- Trailing whitespace fix
- YAML/TOML validation
- Ruff (with ``--fix``)
- Ruff format
- mypy

Hooks run automatically on commit.

Development Workflow
--------------------

1. Setup Environment
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/gavargas22/vds-xarray-backend.git
   cd vds-xarray-backend
   uv sync --group dev --group test

2. Create Feature Branch
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git checkout -b feature/my-feature

3. Make Changes
~~~~~~~~~~~~~~~

- Follow code style conventions
- Write tests for new functionality
- Update documentation as needed
- Ensure type hints are correct

4. Run Tests
~~~~~~~~~~~~

.. code-block:: bash

   uv run pytest

5. Run Linters
~~~~~~~~~~~~~~

.. code-block:: bash

   uv run ruff check .
   uv run black --check .
   uv run isort --check-only .

6. Fix Issues
~~~~~~~~~~~~~

.. code-block:: bash

   uv run ruff check . --fix
   uv run black .
   uv run isort .

7. Commit Changes
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git add .
   git commit -m "feat: add new feature"

8. Push and Create PR
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git push origin feature/my-feature

Code Organization Principles
-----------------------------

Keep It Simple
~~~~~~~~~~~~~~

- Avoid premature optimization
- Don't add features not explicitly requested
- One function, one purpose

Preserve Lazy Loading
~~~~~~~~~~~~~~~~~~~~~~

**Critical**: Never eagerly load full volumes into memory.

All data access must go through ``VdsBackendArray`` → Dask.

.. code-block:: python

   # Good
   subset = ds.sel(inline=slice(1000, 1200))
   result = subset.Amplitude.mean().compute()

   # Bad - don't do this
   all_data = ds.Amplitude.values  # Loads entire volume!

Coordinate-Aware
~~~~~~~~~~~~~~~~

Use coordinate-based selection over index-based:

.. code-block:: python

   # Good
   section = ds.sel(inline=1500)

   # Less clear
   section = ds.isel(inline=500)

Error Handling
~~~~~~~~~~~~~~

Provide informative error messages:

.. code-block:: python

   # Good
   try:
       vds = VDS(path=str(filename))
   except Exception as e:
       raise ValueError(f"Failed to open VDS file {filename}: {e}")

   # Bad
   try:
       vds = VDS(path=str(filename))
   except:
       pass

Testing Guidelines
------------------

See :doc:`testing` for comprehensive testing strategies.

Key points:

- Mock ``ovds_utils.vds.VDS`` in unit tests
- Don't commit VDS files to repository (too large)
- Use ``@pytest.mark.integration`` for tests requiring real files
- Use ``@pytest.mark.slow`` for time-consuming tests

Documentation
-------------

Update documentation when:

- Adding new features
- Changing public API
- Fixing bugs that affect documented behavior

Documentation locations:

- ``docs/`` - User-facing documentation (RST/Markdown)
- Docstrings - API documentation (NumPy style)
- ``CHANGELOG.md`` - Version history
- ``README.md`` - Project overview

Version Management
------------------

**Source of truth**: ``pyproject.toml`` → ``project.version``

**Known issue**: ``__init__.py`` has different version

When updating version:

1. Update ``pyproject.toml`` → ``project.version``
2. Update ``vdsxarray/__init__.py`` → ``__version__``
3. Update ``CHANGELOG.md``
4. Commit with message: ``chore: bump version to X.Y.Z``

Dependencies
------------

**Core dependencies** (do not change without approval):

- xarray >=2024.7.0
- openvds >=3.4.6
- ovds-utils >=0.3.1
- dask >=2024.8.0

**Dev dependencies**:

- ipykernel, matplotlib, scipy

**Test dependencies**:

- pytest, pytest-cov

**Publish dependencies**:

- build, twine

To add dependency:

1. Ask for approval first
2. Add to ``pyproject.toml``
3. Run ``uv sync``
4. Document reason in commit message

Common Patterns
---------------

Opening VDS Files
~~~~~~~~~~~~~~~~~

.. code-block:: python

   try:
       vds = VDS(path=str(filename_or_obj))
   except Exception as e:
       raise ValueError(f"Failed to open VDS file {filename_or_obj}: {e}")

Creating Coordinates
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   coords = np.linspace(
       start=axis.coordinate_min,
       stop=axis.coordinate_max,
       num=shape[axis_index],
       dtype=dtype
   )

Wrapping in Lazy Array
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   backend_array = VdsBackendArray(vds_reader=vds, dtype=Formats.R32)
   data = indexing.LazilyIndexedArray(backend_array)

Creating Dataset
~~~~~~~~~~~~~~~~

.. code-block:: python

   data_array = xr.DataArray(
       data=data,
       coords=coords,
       dims=dims,
       name=name,
       attrs=attrs
   )
   ds = xr.Dataset({name: data_array})
   ds.attrs = global_attrs
   return ds.chunk(chunks)

Next Steps
----------

- Review :doc:`testing` for test strategies
- Check :doc:`guardrails` for critical constraints
- See :doc:`architecture` for codebase structure
