Backend Protocol
================

VDSXarray implements the xarray backend protocol as defined in the xarray documentation.

BackendEntrypoint
-----------------

The ``VdsEngine`` class inherits from ``xarray.backends.BackendEntrypoint``:

.. code-block:: python

   class VdsEngine(BackendEntrypoint):
       def open_dataset(self, filename_or_obj, **kwargs):
           # Implementation
           pass

       def guess_can_open(self, filename_or_obj):
           # Implementation
           pass

Registration
------------

The backend is registered via entry points in ``pyproject.toml``:

.. code-block:: toml

   [project.entry-points."xarray.backends"]
   vds = "vdsxarray.vds:VdsEngine"

This allows users to use ``engine="vds"`` when opening datasets.

BackendArray
------------

The ``VdsBackendArray`` class implements lazy indexing:

.. code-block:: python

   class VdsBackendArray(BackendArray):
       def __getitem__(self, key):
           # Lazy indexing implementation
           pass

Indexing Support
----------------

The backend supports:

- Slice indexing: ``ds.sel(inline=slice(1000, 2000))``
- Integer indexing: ``ds.sel(inline=1500)``
- Nearest neighbor: ``ds.sel(sample=100, method='nearest')``
- Vectorized indexing: ``ds.sel(inline=[1000, 1500, 2000])``
