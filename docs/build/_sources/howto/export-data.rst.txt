Exporting Data
==============

.. _howto-export-netcdf:

How to Export to NetCDF
------------------------

.. code-block:: python

   subset = ds.sel(inline=slice(1400, 1600))
   subset.to_netcdf('output.nc')

How to Export to Zarr
----------------------

.. code-block:: python

   subset.to_zarr('output.zarr')

How to Export Traces to CSV
----------------------------

.. code-block:: python

   trace = ds.Amplitude.sel(inline=1500, crossline=2500)
   trace.to_dataframe().to_csv('trace.csv')

For more export options, see :doc:`../USER-GUIDE`.
