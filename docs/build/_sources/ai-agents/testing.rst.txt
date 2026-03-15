Testing for AI Agents
=====================

Current Test State
------------------

Tests are **minimal** — ``tests/test_basic.py`` contains 4 structural tests:

1. Version string existence
2. ``VdsEngine`` import
3. ``open_dataset`` method presence
4. ``__all__`` exports

**No integration tests** that open real VDS files exist.

Test File Location
~~~~~~~~~~~~~~~~~~

.. code-block:: text

   tests/
     test_basic.py      # Minimal structural tests
     __init__.py        # Empty

Running Tests
-------------

All Tests
~~~~~~~~~

.. code-block:: bash

   uv run pytest

With Coverage
~~~~~~~~~~~~~

.. code-block:: bash

   uv run pytest --cov=vdsxarray

Specific Markers
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Skip slow tests
   uv run pytest -m "not slow"

   # Skip integration tests
   uv run pytest -m "not integration"

   # Only integration tests
   uv run pytest -m integration

Pytest Configuration
--------------------

In ``pyproject.toml``:

.. code-block:: toml

   [tool.pytest.ini_options]
   testpaths = ["tests"]
   python_files = "test_*.py"
   python_functions = "test_*"
   addopts = [
       "--strict-markers",
       "--strict-config",
       "--verbose",
   ]
   markers = [
       "slow: marks tests as slow",
       "integration: marks tests as integration tests",
   ]

Coverage Configuration
----------------------

.. code-block:: toml

   [tool.coverage.run]
   source = ["vdsxarray"]
   omit = [
       "*/tests/*",
       "*/test_*",
   ]

   [tool.coverage.report]
   exclude_lines = [
       "pragma: no cover",
       "def __repr__",
       "raise AssertionError",
       "raise NotImplementedError",
   ]

Testing Strategy
----------------

Unit Tests
~~~~~~~~~~

**Purpose**: Test individual functions/classes in isolation

**Approach**: Mock ``ovds_utils.vds.VDS`` to avoid file I/O

**Example**:

.. code-block:: python

   from unittest.mock import Mock
   import pytest
   from vdsxarray.vds import get_annotated_coordinates
   import numpy as np

   def test_get_annotated_coordinates():
       """Test coordinate extraction from VDS axes"""
       # Create mock VDS object
       mock_vds = Mock()
       mock_vds.shape = (100, 200, 300)

       # Mock axes
       mock_axis_0 = Mock()
       mock_axis_0.coordinate_min = 1000
       mock_axis_0.coordinate_max = 1099

       mock_axis_1 = Mock()
       mock_axis_1.coordinate_min = 2000
       mock_axis_1.coordinate_max = 2199

       mock_axis_2 = Mock()
       mock_axis_2.coordinate_min = 0.0
       mock_axis_2.coordinate_max = 1196.0

       mock_vds.axes = [mock_axis_0, mock_axis_1, mock_axis_2]

       # Test coordinate extraction
       inlines, xlines, samples = get_annotated_coordinates(mock_vds)

       assert len(inlines) == 100
       assert inlines[0] == 1000
       assert inlines[-1] == 1099
       assert inlines.dtype == np.int16

       assert len(xlines) == 200
       assert xlines.dtype == np.int16

       assert len(samples) == 300
       assert samples.dtype == np.float32

Integration Tests
~~~~~~~~~~~~~~~~~

**Purpose**: Test with real VDS files

**Marker**: ``@pytest.mark.integration``

**Important**: Do NOT commit VDS files to repository (they're large)

**Example**:

.. code-block:: python

   import pytest
   import xarray as xr

   @pytest.mark.integration
   def test_open_real_vds_file():
       """Test opening an actual VDS file"""
       # Requires VDS file at this path
       # Not run in CI unless file is available
       ds = xr.open_dataset("test_data.vds", engine="vds")

       assert "Amplitude" in ds.data_vars
       assert set(ds.dims) == {"inline", "crossline", "sample"}
       assert ds.Amplitude.chunks is not None

Slow Tests
~~~~~~~~~~

**Purpose**: Tests that take significant time

**Marker**: ``@pytest.mark.slow``

**Example**:

.. code-block:: python

   import pytest

   @pytest.mark.slow
   def test_large_dataset_performance():
       """Test performance with large dataset"""
       ds = xr.open_dataset("large_survey.vds", engine="vds")

       # Time subset operation
       import time
       start = time.time()
       subset = ds.sel(inline=slice(1000, 1100))
       elapsed = time.time() - start

       assert elapsed < 1.0  # Should be fast (metadata only)

Test Organization
-----------------

Recommended structure:

.. code-block:: text

   tests/
     __init__.py
     test_basic.py           # Import, version checks
     test_coordinates.py     # Coordinate extraction tests
     test_backend_array.py   # VdsBackendArray tests
     test_engine.py          # VdsEngine tests
     test_integration.py     # Integration tests (with real files)
     conftest.py             # Shared fixtures

Mocking VDS Objects
-------------------

Example mock VDS object:

.. code-block:: python

   from unittest.mock import Mock, MagicMock
   import numpy as np

   def create_mock_vds(shape=(100, 200, 300)):
       """Create mock VDS object for testing"""
       mock_vds = Mock()
       mock_vds.shape = shape

       # Create mock axes
       axes = []
       for i, size in enumerate(shape):
           axis = Mock()
           axis.coordinate_min = i * 1000
           axis.coordinate_max = i * 1000 + size - 1
           axes.append(axis)

       mock_vds.axes = axes

       # Mock data access
       def getitem(key):
           # Return random data for any slice
           return np.random.rand(*[
               k.stop - k.start if isinstance(k, slice) else 1
               for k in key
           ]).astype(np.float32)

       mock_vds.__getitem__ = MagicMock(side_effect=getitem)

       return mock_vds

   # Usage
   def test_something():
       mock_vds = create_mock_vds(shape=(50, 100, 150))
       # Use mock_vds in tests

Test Examples
-------------

Test VdsBackendArray
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def test_vds_backend_array_shape():
       """Test VdsBackendArray reports correct shape"""
       mock_vds = create_mock_vds(shape=(100, 200, 300))
       backend_array = VdsBackendArray(mock_vds, dtype=np.float32)

       assert backend_array.shape == (100, 200, 300)
       assert backend_array.dtype == np.float32

   def test_vds_backend_array_indexing():
       """Test VdsBackendArray indexing"""
       mock_vds = create_mock_vds()
       backend_array = VdsBackendArray(mock_vds, dtype=np.float32)

       # Test slice indexing
       result = backend_array[0:10, 0:20, 0:30]
       assert result.shape == (10, 20, 30)

Test VdsEngine
~~~~~~~~~~~~~~

.. code-block:: python

   def test_vds_engine_guess_can_open():
       """Test VdsEngine.guess_can_open()"""
       engine = VdsEngine()

       assert engine.guess_can_open("file.vds") is True
       assert engine.guess_can_open("file.nc") is False
       assert engine.guess_can_open("file.zarr") is False

   @pytest.mark.integration
   def test_vds_engine_open_dataset():
       """Test VdsEngine.open_dataset() with real file"""
       engine = VdsEngine()
       ds = engine.open_dataset("test_data.vds")

       assert isinstance(ds, xr.Dataset)
       assert "Amplitude" in ds.data_vars

Test Coordinate Extraction
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def test_coordinate_extraction():
       """Test coordinate array generation"""
       mock_vds = create_mock_vds(shape=(10, 20, 30))

       inlines, xlines, samples = get_annotated_coordinates(mock_vds)

       # Check lengths match shape
       assert len(inlines) == 10
       assert len(xlines) == 20
       assert len(samples) == 30

       # Check data types
       assert inlines.dtype == np.int16
       assert xlines.dtype == np.int16
       assert samples.dtype == np.float32

       # Check coordinate ranges
       assert inlines[0] == 0  # coordinate_min from mock
       assert inlines[-1] == 9  # coordinate_max from mock

Fixtures
--------

Create reusable fixtures in ``conftest.py``:

.. code-block:: python

   import pytest
   from unittest.mock import Mock

   @pytest.fixture
   def mock_vds():
       """Fixture providing mock VDS object"""
       mock = Mock()
       mock.shape = (100, 200, 300)
       # ... setup mock axes, etc.
       return mock

   @pytest.fixture
   def small_mock_vds():
       """Fixture providing small mock VDS for fast tests"""
       mock = Mock()
       mock.shape = (10, 20, 30)
       # ... setup mock axes, etc.
       return mock

   # Usage in tests
   def test_with_fixture(mock_vds):
       backend_array = VdsBackendArray(mock_vds, dtype=np.float32)
       assert backend_array.shape == (100, 200, 300)

Testing Checklist
-----------------

When adding new functionality:

1. ✓ Write unit tests with mocked VDS objects
2. ✓ Test edge cases (empty arrays, single values)
3. ✓ Test error handling
4. ✓ Add integration test if applicable (with marker)
5. ✓ Ensure tests pass locally
6. ✓ Check test coverage (aim for >80%)
7. ✓ Update docstrings if behavior changes

CI/CD Testing
-------------

Tests run automatically in CI pipeline on:

- Push to ``main``
- Pull requests
- Manual workflow dispatch

CI runs:

- ``uv run pytest`` (all tests)
- Linting checks
- Type checking (mypy)

Known Test Gaps
---------------

Current gaps that should be filled:

1. No tests for ``VdsBackendArray`` indexing
2. No tests for ``VdsEngine.open_dataset()``
3. No tests for coordinate extraction
4. No tests for chunking behavior
5. No tests for error handling
6. No integration tests with real VDS files

Next Steps
----------

- Review :doc:`development` for code style
- Check :doc:`guardrails` for critical constraints
- See :doc:`architecture` for component details
