For AI Coding Agents
====================

.. warning::
   **This section is intended exclusively for AI coding agents.**

   Human contributors should refer to :doc:`../contributing` instead.

.. admonition:: About This Section
   :class: important

   This documentation provides comprehensive guidance for AI coding agents working on the vdsxarray codebase. It includes architecture details, development conventions, testing strategies, and critical guardrails.

Welcome, AI Agent! This section contains everything you need to effectively contribute to the vdsxarray project.

Quick Reference
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Topic
     - Description
   * - :doc:`architecture`
     - Core architecture, file structure, and component interactions
   * - :doc:`development`
     - Code style, conventions, commit messages, and development workflow
   * - :doc:`testing`
     - Testing strategies, current state, and how to write tests
   * - :doc:`guardrails`
     - Critical constraints and things you must NOT do

Contents
--------

.. toctree::
   :maxdepth: 2

   architecture
   development
   testing
   guardrails

Project Identity
----------------

**vdsxarray** is an xarray backend engine for reading VDS (Volume Data Store) seismic data files.

- **Language**: Python (3.9–3.11)
- **Build system**: Hatchling
- **Package manager**: uv
- **Version source**: ``pyproject.toml`` (``project.version``)

Entry Point
~~~~~~~~~~~

Registered as an xarray backend:

.. code-block:: toml

   [project.entry-points."xarray.backends"]
   vds = "vdsxarray.vds:VdsEngine"

Users call:

.. code-block:: python

   xr.open_dataset("file.vds", engine="vds")

Domain Context: VDS & Seismic Data
-----------------------------------

VDS (Volume Data Store) is a cloud-optimized format for 3D seismic survey data.

Core abstraction is a **3D volume** with three axes:

.. list-table::
   :header-rows: 1

   * - Dimension
     - Axis Index
     - Description
     - dtype
   * - ``inline``
     - 0
     - Survey line direction
     - ``int16``
   * - ``crossline``
     - 1
     - Perpendicular to inline
     - ``int16``
   * - ``sample``
     - 2
     - Time or depth (vertical axis)
     - ``float32``

Volume data itself is ``float32`` amplitude values.

Key Dependencies
~~~~~~~~~~~~~~~~

- **openvds** (>=3.4.6): Bluware's C++ SDK with Python bindings
- **ovds-utils** (>=0.3.1): Python wrapper around openvds (primary interface)
- **xarray** (>=2024.7.0): Backend engine protocol
- **dask** (>=2024.8.0): Lazy/chunked loading

.. important::
   The code uses ``ovds_utils.vds.VDS`` exclusively. It does **not** call ``openvds`` directly.

Development Commands
--------------------

Setup
~~~~~

.. code-block:: bash

   uv sync --group dev --group test

Run Tests
~~~~~~~~~

.. code-block:: bash

   uv run pytest

Linting
~~~~~~~

.. code-block:: bash

   # Check (all three must pass)
   uv run ruff check .
   uv run black --check .
   uv run isort --check-only .

   # Auto-fix
   uv run ruff check . --fix
   uv run black .
   uv run isort .

Known Issues
------------

Review these before making changes:

1. **Version mismatch**: ``__init__.py`` has ``__version__ = "1.0.0"`` but ``pyproject.toml`` says ``1.0.1``
2. **Commented chunking logic**: ``estimate_chunk_size`` utility is imported but not used
3. **Stub function**: ``get_cdp_coordinates()`` returns ``None``
4. **Coordinate docstring mismatch**: Documentation vs. implementation may differ
5. **Dimension order inconsistency**: Between ``utils.py`` and ``VdsEngine``
6. **Silent exception swallowing**: VDS cleanup uses bare ``except: pass``

See :doc:`architecture` for full details.

Critical Guardrails
-------------------

.. danger::

   **DO NOT:**

   - Add dependencies without approval
   - Change entry-point name (``xarray.backends.vds``)
   - Change dimension names (``inline``, ``crossline``, ``sample``)
   - Suppress type errors with ``# type: ignore``
   - Require real VDS files in tests (use mocks)
   - Eagerly load full volumes into memory
   - Use Python 3.10+ exclusive syntax

See :doc:`guardrails` for complete list.

Next Steps
----------

1. Read :doc:`architecture` to understand the codebase structure
2. Review :doc:`development` for code style and conventions
3. Check :doc:`testing` before writing tests
4. Keep :doc:`guardrails` in mind at all times

Navigation
----------

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: Architecture
      :link: architecture
      :link-type: doc

      Repository structure, core components, and data flow

   .. grid-item-card:: Development
      :link: development
      :link-type: doc

      Code style, conventions, and commit messages

   .. grid-item-card:: Testing
      :link: testing
      :link-type: doc

      Current test state and testing strategies

   .. grid-item-card:: Guardrails
      :link: guardrails
      :link-type: doc

      Critical constraints and forbidden operations
