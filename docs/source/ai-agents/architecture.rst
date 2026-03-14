Architecture for AI Agents
==========================

Repository Structure
--------------------

.. code-block:: text

   vdsxarray/
     __init__.py        # Package exports: VdsEngine, __version__
     vds.py             # Core module — engine, backend array, coordinates
     utils.py           # Metadata extraction, chunk size estimation
   tests/
     test_basic.py      # Unit tests (currently minimal)
   scripts/
     release.sh         # Release automation
   docs/                # User-facing documentation (markdown)
   notebooks/           # Jupyter notebooks (examples/exploration)
   .github/workflows/   # CI/CD pipelines

Core Architecture
-----------------

All core functionality is in ``vdsxarray/vds.py``.

1. get_annotated_coordinates(vds)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def get_annotated_coordinates(vds: VDS) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
       """Extract inline/crossline/sample coordinates from VDS axis metadata."""

**Purpose**: Convert VDS axis metadata into xarray coordinate arrays

**Implementation**:

- Uses ``np.linspace(start=axis.coordinate_min, stop=axis.coordinate_max, num=shape[i])``
- Returns ``(inlines, xlines, samples)`` as numpy arrays
- Data types: int16 for inlines/xlines, float32 for samples

**Known Issue**: Docstring says axis 0 = samples, but code does ``inlines = vds.axes[0]``

2. VdsBackendArray(BackendArray)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class VdsBackendArray(BackendArray):
       def __init__(self, vds_reader: VDS, dtype):
           self.vds_reader = vds_reader
           self.shape = vds_reader.shape
           self.dtype = np.dtype("float32")

       def __getitem__(self, key):
           # Implements lazy indexing
           pass

**Purpose**: Wrap VDS reader for xarray's lazy indexing protocol

**Key Method**: ``__getitem__`` via ``explicit_indexing_adapter``

**Raw Indexing**: ``_raw_indexing_method`` translates xarray indices to VDS slices

**Supports**:

- Slice indexing: ``key[i]`` is a ``slice`` object
- Array indexing: ``key[i]`` is an ``np.ndarray``
- Integer indexing: ``key[i]`` is an ``int``

**Returns**: Squeezed data array (removes singleton dimensions)

3. VdsEngine(BackendEntrypoint)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class VdsEngine(BackendEntrypoint):
       def open_dataset(self, filename_or_obj, *, drop_variables=None, ...):
           # Opens VDS, creates dataset
           pass

       def guess_can_open(self, filename_or_obj):
           # Returns True for *.vds files
           pass

**Purpose**: Xarray backend engine (registered as ``engine="vds"``)

**open_dataset Flow**:

1. Open VDS file via ``VDS(path=str(filename_or_obj))``
2. Extract coordinates via ``get_annotated_coordinates(vds)``
3. Set dimension names: ``("inline", "crossline", "sample")``
4. Create ``VdsBackendArray`` wrapper
5. Set VDS channel format to ``Formats.R32``
6. Wrap in ``LazilyIndexedArray``
7. Create ``xr.DataArray`` with coordinates and dimensions
8. Create ``xr.Dataset`` with attributes
9. Chunk to 128×128×128
10. Clean up VDS resources (with silent exception swallowing)
11. Return chunked dataset

**Parameters**:

- ``filename_or_obj``: Path to VDS file
- ``drop_variables``: Not used
- ``volume_format``: Default ``"float32"``
- ``name``: Data variable name, default ``"Amplitude"``
- ``channels``: Not used
- ``LOD``: Level of detail, default 0
- ``calculate_cdp``: Default ``False`` (not implemented)

4. get_cdp_coordinates(vds)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def get_cdp_coordinates(vds: VDS):
       pass

**Status**: Stub function, returns ``None``

**Purpose**: Placeholder for future CDP coordinate calculation

Utilities (vdsxarray/utils.py)
-------------------------------

get_vds_metadata(vds)
~~~~~~~~~~~~~~~~~~~~~

Extracts shape, axis info, data type into a dict.

**Not currently used** in main codebase.

estimate_chunk_size(shape, target_mb=64)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculates roughly-cubic chunk sizes.

**Status**: Imported in ``vds.py`` but **commented out**

**Issue**: Returns dict with keys ``{'sample': ..., 'crossline': ..., 'inline': ...}``
mapping shape indices 0→sample, 1→crossline, 2→inline. But ``VdsEngine`` uses dimension
order ``(inline, crossline, sample)``. Keys won't match if uncommented.

Data Flow Diagram
-----------------

.. code-block:: text

   User Code
      ↓
   xr.open_dataset("file.vds", engine="vds")
      ↓
   Xarray dispatches to VdsEngine.open_dataset()
      ↓
   VDS(path) opens file via ovds_utils
      ↓
   get_annotated_coordinates(vds) extracts coordinates
      ↓
   VdsBackendArray wraps VDS reader
      ↓
   LazilyIndexedArray wraps VdsBackendArray
      ↓
   DataArray created with coords, dims, attrs
      ↓
   Dataset created, chunked to 128³
      ↓
   Dataset returned to user
      ↓
   User performs operations (lazy)
      ↓
   .compute() or .values triggers data loading
      ↓
   VdsBackendArray.__getitem__ called for each chunk
      ↓
   VDS reader fetches data from disk
      ↓
   Data returned to user

Entry Point Registration
-------------------------

In ``pyproject.toml``:

.. code-block:: toml

   [project.entry-points."xarray.backends"]
   vds = "vdsxarray.vds:VdsEngine"

This registers the backend so xarray can discover it.

**Critical**: Do NOT change ``vds`` key or the module path.

Axis Order Mapping
------------------

**VDS file axes** → **xarray dimensions**:

.. list-table::
   :header-rows: 1

   * - VDS Axis
     - xarray Dimension
     - Code Reference
   * - ``vds.axes[0]``
     - ``inline``
     - ``vds.py:39-44``
   * - ``vds.axes[1]``
     - ``crossline``
     - ``vds.py:46-51``
   * - ``vds.axes[2]``
     - ``sample``
     - ``vds.py:53-58``

**Dimension order in Dataset**: ``(inline, crossline, sample)``

**Shape**: ``(n_inlines, n_crosslines, n_samples)``

Memory Management
-----------------

**Lazy Loading**: All data access through ``VdsBackendArray`` → Dask

**Chunking**: Default 128×128×128 = ~8.39 MB per chunk

**Resource Cleanup**:

.. code-block:: python

   # In VdsEngine.open_dataset()
   try:
       vds.accessor.commit()
       vds.accessor.removeReference()
   except Exception:
       pass  # Silent exception swallowing

**Issue**: No logging or warning if cleanup fails.

Type System
-----------

**Coordinate types**:

- ``inline``: ``int16``
- ``crossline``: ``int16``
- ``sample``: ``float32``

**Data type**: ``float32`` (amplitude values)

**Dask chunks**: Stored as tuples in ``DataArray.chunks``

Important Implementation Details
---------------------------------

1. The code calls ``ovds_utils.vds.VDS``, **not** ``openvds`` directly
2. Coordinates are generated via ``np.linspace``, not extracted from file data
3. All data is wrapped in Dask arrays (lazy)
4. Dimension order is hardcoded as ``("inline", "crossline", "sample")``
5. Default chunks are hardcoded as 128 for all dimensions
6. The ``calculate_cdp`` parameter is accepted but not implemented
7. VDS cleanup errors are silently swallowed

Next Steps
----------

- Review :doc:`development` for code style conventions
- Check :doc:`testing` for testing strategies
- Read :doc:`guardrails` for critical constraints
