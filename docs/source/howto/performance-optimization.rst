Performance Optimization
=========================

.. _howto-optimize-performance:

How to Optimize Data Access
----------------------------

.. code-block:: python

   # Good: Contiguous selections
   subset = ds.sel(
       inline=slice(1000, 2000),
       crossline=slice(2000, 3000)
   )

   # Avoid: Non-contiguous selections
   # scattered = ds.sel(inline=[1000, 1500, 2000])

How to Monitor Memory Usage
----------------------------

.. code-block:: python

   print(f"Dataset size: {ds.nbytes / 1e9:.1f} GB")
   print(f"Chunk sizes: {ds.Amplitude.chunksizes}")

How to Process Large Datasets
------------------------------

.. code-block:: python

   from dask.diagnostics import ProgressBar

   with ProgressBar():
       result = ds.Amplitude.mean().compute()

For more performance tips, see :doc:`../USER-GUIDE` and :doc:`../explanation/lazy-loading`.
