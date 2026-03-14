Architecture
============

VDSXarray implements the xarray backend protocol to provide seamless VDS file access.

Component Overview
------------------

The architecture consists of three main components:

1. **VdsEngine** - Backend entry point
2. **VdsBackendArray** - Lazy indexing wrapper
3. **Coordinate extraction** - Metadata to xarray mapping

VdsEngine
---------

Implements ``xarray.backends.BackendEntrypoint``:

- Registered via entry points as ``engine="vds"``
- Opens VDS files and creates xarray datasets
- Manages chunking and lazy loading
- Handles resource cleanup

VdsBackendArray
---------------

Implements ``xarray.backends.BackendArray``:

- Wraps ``ovds_utils.vds.VDS`` reader
- Provides lazy indexing via ``__getitem__``
- Translates xarray index types to VDS slice reads
- Supports vectorized indexing

Coordinate Extraction
---------------------

``get_annotated_coordinates(vds)`` function:

- Extracts inline/crossline/sample coordinate arrays
- Uses ``np.linspace`` with VDS axis metadata
- Maps VDS axes to xarray dimensions
- Returns coordinate arrays for dataset creation

Data Flow
---------

1. User calls ``xr.open_dataset("file.vds", engine="vds")``
2. Xarray dispatches to ``VdsEngine.open_dataset()``
3. VdsEngine opens VDS file via ``ovds_utils``
4. Coordinate arrays extracted from VDS metadata
5. ``VdsBackendArray`` wraps VDS reader
6. Array wrapped in ``LazilyIndexedArray``
7. Dataset created with chunked dask arrays
8. Dataset returned to user

For implementation details, see :doc:`../TECHNICAL-OVERVIEW` and :doc:`../reference/api`.
