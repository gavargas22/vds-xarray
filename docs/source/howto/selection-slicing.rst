Data Selection and Slicing
==========================

.. _howto-select-region:

How to Select a Region of Interest
-----------------------------------

.. code-block:: python

   ds = xr.open_dataset("file.vds", engine="vds")

   # Select by coordinate ranges
   roi = ds.sel(
       inline=slice(1400, 1600),
       crossline=slice(2400, 2600),
       sample=slice(0, 1000)
   )

.. _howto-extract-traces:

How to Extract Seismic Traces
------------------------------

.. code-block:: python

   # Single trace
   trace = ds.Amplitude.sel(inline=1500, crossline=2500)

   # Multiple traces along an inline
   traces = ds.Amplitude.sel(inline=1500)

For more selection techniques, see :doc:`../USER-GUIDE`.
