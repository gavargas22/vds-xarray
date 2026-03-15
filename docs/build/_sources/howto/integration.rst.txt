Integration with Other Tools
=============================

How to Convert to NumPy
------------------------

.. code-block:: python

   numpy_array = ds.Amplitude.sel(inline=slice(1400, 1600)).values

How to Convert to Pandas
-------------------------

.. code-block:: python

   df = ds.Amplitude.sel(sample=slice(0, 500)).to_dataframe()

How to Use with Dask
---------------------

.. code-block:: python

   import dask

   dask.config.set({'array.chunk-size': '128MB'})
   result = ds.Amplitude.mean().compute()

For more integration examples, see :doc:`../USER-GUIDE`.
