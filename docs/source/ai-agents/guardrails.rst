Guardrails for AI Agents
========================

.. danger::

   **Critical Constraints**

   These are hard boundaries. Violating them will break the package for users or cause serious issues.

Public API Constraints
----------------------

DO NOT Change Entry-Point Name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: toml

   # In pyproject.toml - DO NOT MODIFY
   [project.entry-points."xarray.backends"]
   vds = "vdsxarray.vds:VdsEngine"

**Why**: Downstream users depend on ``engine="vds"``

**Impact**: Changing this breaks all existing code

DO NOT Change Dimension Names
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # These are part of the public API contract
   dims = ("inline", "crossline", "sample")  # DO NOT CHANGE

**Why**: Users' code assumes these dimension names

**Impact**: Breaking change for all users

.. code-block:: python

   # User code depends on these names
   section = ds.sel(inline=1500)  # Would break if renamed
   time_slice = ds.sel(sample=100)  # Would break if renamed

DO NOT Add Dependencies Without Approval
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Current core dependencies**:

- xarray >=2024.7.0
- openvds >=3.4.6
- ovds-utils >=0.3.1
- dask >=2024.8.0

**Why**: Dependencies affect all users

**Impact**: Installation issues, conflicts, bloat

**Process**: Ask for approval before adding ANY new dependency

Data Handling Constraints
--------------------------

DO NOT Eagerly Load Full Volumes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # BAD - Never do this
   all_data = vds_reader[:]  # Loads entire volume into memory!
   dataset = xr.Dataset({"Amplitude": all_data})

   # GOOD - Always use lazy loading
   backend_array = VdsBackendArray(vds_reader, dtype)
   lazy_data = indexing.LazilyIndexedArray(backend_array)
   dataset = xr.Dataset({"Amplitude": lazy_data})

**Why**: Preserve lazy loading — core feature

**Impact**: Memory errors on large datasets

DO NOT Break Lazy Evaluation Chain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Preserve lazy loading** — never eagerly compute unless explicitly requested.

.. code-block:: python

   # BAD
   def open_dataset(...):
       data = backend_array[:]  # Computes immediately
       return xr.Dataset({"Amplitude": data})

   # GOOD
   def open_dataset(...):
       lazy_data = indexing.LazilyIndexedArray(backend_array)
       return xr.Dataset({"Amplitude": lazy_data})

Code Quality Constraints
-------------------------

DO NOT Suppress Type Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # BAD
   result = some_function()  # type: ignore

   # BAD
   result: Any = some_function()

   # GOOD
   result: np.ndarray = some_function()  # Correct type

**Why**: Type safety prevents bugs

**Process**: Fix type errors properly, don't hide them

DO NOT Use Python 3.10+ Exclusive Syntax
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Target**: Python 3.9 minimum

.. code-block:: python

   # BAD - Python 3.10+ only
   def func(x: int | str):  # Union syntax
       pass

   match value:  # match statement
       case 1:
           pass

   # GOOD - Python 3.9 compatible
   from typing import Union

   def func(x: Union[int, str]):
       pass

   if value == 1:
       pass

**Why**: Package supports Python 3.9–3.11

**Impact**: Import errors for Python 3.9 users

Testing Constraints
-------------------

DO NOT Require Real VDS Files in Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # BAD - Requires real file
   def test_open_dataset():
       ds = xr.open_dataset("real_file.vds", engine="vds")
       assert ds is not None

   # GOOD - Use mocks
   def test_open_dataset():
       mock_vds = Mock()
       mock_vds.shape = (100, 200, 300)
       # ... test with mock

**Why**: VDS files are large, can't commit to repo

**Process**: Mock ``ovds_utils.vds.VDS`` in unit tests

DO NOT Commit Large Test Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Rule**: Never commit VDS files to repository

**Why**: VDS files are 10s-100s of MB

**Alternative**: Use ``@pytest.mark.integration`` for tests requiring real files

Documentation Constraints
--------------------------

DO NOT Remove Docstrings
~~~~~~~~~~~~~~~~~~~~~~~~~

**All public functions** must have NumPy-style docstrings

.. code-block:: python

   # BAD
   def get_coordinates(vds):
       return vds.axes

   # GOOD
   def get_coordinates(vds):
       """
       Extract coordinates from VDS object.

       Parameters
       ----------
       vds : VDS
           VDS object containing axes

       Returns
       -------
       list
           List of coordinate arrays
       """
       return vds.axes

DO NOT Change Public Function Signatures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # BAD - Breaking change
   def open_dataset(filename, new_required_param):
       pass

   # GOOD - Maintain compatibility
   def open_dataset(filename, new_param=None):
       pass

**Why**: Breaking changes affect all users

**Process**: Add new parameters as optional with defaults

Architecture Constraints
------------------------

DO NOT Call openvds Directly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # BAD
   import openvds
   handle = openvds.open(filename)

   # GOOD
   from ovds_utils.vds import VDS
   vds = VDS(path=filename)

**Why**: Code uses ``ovds_utils`` wrapper exclusively

**Impact**: Inconsistent interface, harder to mock

DO NOT Change Dimension Order
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # DO NOT CHANGE - This is fixed
   dims = ("inline", "crossline", "sample")
   shape = (n_inlines, n_crosslines, n_samples)

**Why**: Dimension order is part of public API

**Impact**: All downstream code assumes this order

Error Handling Constraints
---------------------------

DO NOT Silently Swallow Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # BAD
   try:
       vds.accessor.commit()
   except:
       pass  # Silent failure

   # GOOD
   try:
       vds.accessor.commit()
   except Exception as e:
       logging.warning(f"Failed to commit VDS accessor: {e}")

   # Or even better
   try:
       vds.accessor.commit()
   except Exception as e:
       raise RuntimeError(f"Failed to commit VDS accessor: {e}") from e

**Exception**: The current code DOES have silent swallowing in VDS cleanup. If you touch that code, fix it.

Performance Constraints
-----------------------

DO NOT Load Metadata Eagerly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Open files fast** — extract only essential metadata

.. code-block:: python

   # GOOD - Extract only what's needed
   def open_dataset(filename):
       vds = VDS(path=filename)
       coords = get_annotated_coordinates(vds)  # Minimal extraction
       # ... create dataset
       return ds

DO NOT Create Huge Default Chunks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Current default**: 128×128×128 (~8.4 MB)

**Don't**: Change to 512×512×512 (512 MB chunks!)

**Why**: Large chunks hurt performance and memory

Version Control Constraints
----------------------------

DO NOT Edit CHANGELOG Directly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Process**:

1. Make code changes
2. Update CHANGELOG in same commit
3. Use conventional commit format

DO NOT Force-Push to main
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Rule**: Never force-push to ``main`` branch

**Why**: Breaks others' work, loses history

Known Issues to Avoid
----------------------

Version Mismatch
~~~~~~~~~~~~~~~~

**Issue**: ``__init__.py`` has ``__version__ = "1.0.0"`` but ``pyproject.toml`` says ``1.0.1``

**Rule**: ``pyproject.toml`` is the source of truth

**If you update version**: Update BOTH files

Commented Code
~~~~~~~~~~~~~~

**Issue**: ``estimate_chunk_size`` is imported but commented out

**If you enable it**: Fix the dimension order mismatch first (see :doc:`architecture`)

Stub Functions
~~~~~~~~~~~~~~

**Issue**: ``get_cdp_coordinates()`` returns ``None``

**If you implement it**: Write tests first, ensure it's actually needed

Silent Exception Swallowing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Issue**: VDS cleanup uses ``except Exception: pass``

**If you touch that code**: Add proper logging or error handling

Summary: The Absolute Don'ts
-----------------------------

1. ❌ Add dependencies without approval
2. ❌ Change entry-point name (``xarray.backends.vds``)
3. ❌ Change dimension names (``inline``, ``crossline``, ``sample``)
4. ❌ Suppress type errors with ``# type: ignore``
5. ❌ Require real VDS files in tests
6. ❌ Eagerly load full volumes into memory
7. ❌ Use Python 3.10+ exclusive syntax
8. ❌ Change public function signatures without defaults
9. ❌ Call ``openvds`` directly (use ``ovds_utils``)
10. ❌ Silently swallow errors

Quick Reference
---------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Constraint
     - Reason
   * - Don't change ``engine="vds"``
     - Breaks all user code
   * - Don't change dimension names
     - Public API contract
   * - Don't add dependencies
     - Affects all users
   * - Don't eager-load data
     - Breaks lazy loading
   * - Don't suppress type errors
     - Hides bugs
   * - Don't use 3.10+ syntax
     - Breaks Python 3.9 support
   * - Don't require VDS files in tests
     - Can't commit to repo
   * - Don't call openvds directly
     - Inconsistent with codebase
   * - Don't change dim order
     - Public API contract

Next Steps
----------

- Review :doc:`architecture` for codebase structure
- Check :doc:`development` for code style
- See :doc:`testing` for test strategies

When in Doubt
-------------

**Ask first** before:

- Adding dependencies
- Changing public APIs
- Modifying dimension names/order
- Changing entry-point configuration
- Making breaking changes
