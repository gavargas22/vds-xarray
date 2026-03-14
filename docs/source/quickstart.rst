Quick Start Guide
=================

This guide will help you get started with vdsxarray in just a few minutes.

Opening Your First VDS File
----------------------------

The simplest way to open a VDS file is using xarray's ``open_dataset`` function:

.. code-block:: python

   import xarray as xr

   # Open a VDS file
   ds = xr.open_dataset("path/to/your/file.vds", engine="vds")

   # Display the dataset structure
   print(ds)

Output:

.. code-block:: text

   <xarray.Dataset>
   Dimensions:    (inline: 1401, crossline: 1351, sample: 2741)
   Coordinates:
     * inline     (inline) int16 1300 1301 1302 ... 2698 2699 2700
     * crossline  (crossline) int16 2500 2502 2504 ... 5196 5198 5200
     * sample     (sample) float32 0.0 3.048 6.096 ... 8.348e+03 8.352e+03
   Data variables:
       Amplitude  (inline, crossline, sample) float32 dask.array<...>
   Attributes:
       title:         VDS Seismic Data: Amplitude
       source:        /path/to/file.vds
       created_with:  vdsxarray

Understanding the Dataset Structure
------------------------------------

A VDS dataset contains:

**Dimensions**
   - ``inline``: Survey line direction (typically N-S)
   - ``crossline``: Perpendicular to inline (typically E-W)
   - ``sample``: Time or depth (vertical axis)

**Coordinates**
   Coordinate arrays that map dimension indices to real-world values

**Data Variables**
   - ``Amplitude``: The seismic amplitude data (main variable)

**Attributes**
   Metadata about the dataset

Accessing Seismic Data
-----------------------

Access the amplitude data:

.. code-block:: python

   # Get the amplitude data array
   amplitude = ds.Amplitude

   # Check if it's chunked (for lazy loading)
   print(f"Chunked: {amplitude.chunks is not None}")
   print(f"Chunk sizes: {amplitude.chunksizes}")

   # Get coordinate information
   print(f"Inline range: {ds.inline.min().values} to {ds.inline.max().values}")
   print(f"Crossline range: {ds.crossline.min().values} to {ds.crossline.max().values}")
   print(f"Sample range: {ds.sample.min().values} to {ds.sample.max().values} ms")

Selecting Data
--------------

Select data using coordinate values:

.. code-block:: python

   # Select a single inline
   inline_slice = ds.sel(inline=1500)

   # Select a range
   subset = ds.sel(
       inline=slice(1400, 1600),
       crossline=slice(2400, 2600),
       sample=slice(0, 1000)
   )

   # Select nearest value
   time_slice = ds.sel(sample=100, method='nearest')

Basic Visualization
-------------------

Create a simple seismic section plot:

.. code-block:: python

   import matplotlib.pyplot as plt

   # Plot an inline section
   ds.Amplitude.sel(inline=1500).plot(
       x='crossline',
       y='sample',
       cmap='seismic',
       robust=True
   )
   plt.gca().invert_yaxis()  # Time increases downward
   plt.title('Seismic Section - Inline 1500')
   plt.ylabel('Time (ms)')
   plt.show()

Simple Data Analysis
--------------------

Calculate basic statistics:

.. code-block:: python

   import numpy as np

   # Calculate RMS amplitude
   rms = np.sqrt((ds.Amplitude ** 2).mean())
   print(f"RMS amplitude: {rms.values:.3f}")

   # Create RMS amplitude map
   rms_map = np.sqrt((ds.Amplitude ** 2).mean('sample'))
   rms_map.plot(x='crossline', y='inline', cmap='viridis')
   plt.title('RMS Amplitude Map')
   plt.show()

Working with Large Datasets
----------------------------

VDSXarray uses lazy loading, so large datasets won't overwhelm memory:

.. code-block:: python

   # Open large dataset (no data loaded yet)
   ds = xr.open_dataset("huge_survey.vds", engine="vds")
   print(f"Dataset size: {ds.nbytes / 1e9:.1f} GB")

   # Select subset (still lazy)
   subset = ds.sel(
       inline=slice(1000, 1200),
       crossline=slice(2000, 2200)
   )

   # Compute only when needed
   result = subset.Amplitude.mean().compute()
   print(f"Mean amplitude: {result.values:.3f}")

Complete Example
----------------

Here's a complete workflow from loading to visualization:

.. code-block:: python

   import xarray as xr
   import numpy as np
   import matplotlib.pyplot as plt

   # 1. Open VDS file
   ds = xr.open_dataset("survey.vds", engine="vds")

   # 2. Explore dataset
   print(f"Survey dimensions: {dict(ds.dims)}")

   # 3. Select region of interest
   roi = ds.sel(
       inline=slice(1400, 1600),
       crossline=slice(2400, 2600)
   )

   # 4. Calculate RMS amplitude
   rms = np.sqrt((roi.Amplitude ** 2).mean('sample'))

   # 5. Create visualization
   fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

   # Seismic section
   roi.Amplitude.sel(inline=1500).plot(
       ax=ax1,
       x='crossline',
       y='sample',
       cmap='seismic',
       robust=True
   )
   ax1.invert_yaxis()
   ax1.set_title('Seismic Section - Inline 1500')
   ax1.set_ylabel('Time (ms)')

   # RMS amplitude map
   rms.plot(
       ax=ax2,
       x='crossline',
       y='inline',
       cmap='viridis'
   )
   ax2.set_title('RMS Amplitude Map')

   plt.tight_layout()
   plt.show()

   # 6. Export subset
   roi.to_netcdf('region_of_interest.nc')
   print("Subset exported successfully!")

Next Steps
----------

Now that you're familiar with the basics, explore:

- **Tutorials**: :doc:`tutorials/index` - Detailed learning-oriented guides
- **How-To Guides**: :doc:`howto/index` - Solutions to specific tasks
- **API Reference**: :doc:`reference/api` - Detailed API documentation
- **Examples**: Check the ``notebooks/`` directory for Jupyter notebook examples

Common Patterns
---------------

**Pattern 1: Quick Inspection**

.. code-block:: python

   ds = xr.open_dataset("file.vds", engine="vds")
   print(ds)
   ds.Amplitude.sel(inline=ds.inline[len(ds.inline)//2]).plot()

**Pattern 2: Extract and Process**

.. code-block:: python

   subset = ds.sel(inline=slice(1000, 2000))
   processed = subset.Amplitude.rolling(sample=5).mean()
   result = processed.compute()

**Pattern 3: Export for Other Tools**

.. code-block:: python

   # Export to NetCDF
   subset.to_netcdf('output.nc')

   # Export to Zarr (cloud-friendly)
   subset.to_zarr('output.zarr')

   # Export trace to CSV
   trace = ds.Amplitude.sel(inline=1500, crossline=2500)
   trace.to_dataframe().to_csv('trace.csv')

Tips for Success
----------------

1. **Always use lazy loading** - Don't call ``.compute()`` until necessary
2. **Select before computing** - Reduce data size before calculations
3. **Use coordinate-based selection** - ``.sel()`` is more intuitive than ``.isel()``
4. **Check chunk sizes** - Default chunks (128×128×128) work well for most cases
5. **Monitor memory** - Use ``.nbytes`` to check data sizes before computing

Getting Help
------------

If you encounter issues:

1. Check the :doc:`howto/troubleshooting` guide
2. Review the :doc:`reference/api` documentation
3. Search or open an issue on `GitHub <https://github.com/gavargas22/vds-xarray-backend/issues>`_
4. Read the :doc:`explanation/index` section for deeper understanding
