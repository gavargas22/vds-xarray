Lazy Loading
============

Lazy loading is a core concept in vdsxarray that enables working with datasets larger than available memory.

What is Lazy Loading?
----------------------

Lazy loading means data is **not** loaded into memory when you open a file. Instead:

1. Metadata is read immediately (dimensions, coordinates, attributes)
2. Data remains on disk
3. Data is loaded only when needed (on ``.compute()`` or ``.values``)

Example
-------

.. code-block:: python

   # Open dataset - NO data loaded yet
   ds = xr.open_dataset("100GB_survey.vds", engine="vds")
   print(f"Dataset size: {ds.nbytes / 1e9:.1f} GB")  # Shows 100 GB

   # Still no data loaded - just metadata operations
   subset = ds.sel(inline=slice(1000, 1200))
   print(f"Subset size: {subset.nbytes / 1e9:.1f} GB")  # Shows 5 GB

   # NOW data is loaded into memory
   result = subset.Amplitude.mean().compute()
   print(f"Result: {result.values}")

How It Works
------------

VDSXarray uses:

1. **Dask arrays**: Lazy array library for parallel computing
2. **VdsBackendArray**: Custom backend that reads VDS on demand
3. **Chunking**: Data divided into manageable pieces

When you call ``.compute()``:

1. Dask determines which chunks are needed
2. ``VdsBackendArray.__getitem__`` is called for each chunk
3. VDS reader fetches data from disk
4. Results are combined and returned

Benefits
--------

**Work with huge datasets**: Process 100GB+ surveys on laptops

**Memory efficiency**: Only load what you need

**Performance**: Parallel chunk loading with Dask

**Interactivity**: Fast exploration without waiting for full load

Best Practices
--------------

1. **Select before computing**: Reduce data size first
2. **Use coordinate selection**: ``.sel()`` is clearer than ``.isel()``
3. **Monitor chunk sizes**: Check ``.chunksizes`` attribute
4. **Compute strategically**: Only compute final results

For more details, see :doc:`../howto/performance-optimization`.
