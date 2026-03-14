Tutorial 1: Your First VDS Dataset
====================================

.. admonition:: What you'll learn
   :class: tip

   In this tutorial, you'll learn how to:

   - Open a VDS seismic file
   - Understand the dataset structure
   - Access coordinates and dimensions
   - Perform basic data selection
   - Save your work

**Estimated time**: 15-20 minutes

**Prerequisites**: vdsxarray installed, Python basics, access to a VDS file

Introduction
------------

In this tutorial, we'll walk through opening your first VDS seismic dataset and
exploring its contents. By the end, you'll understand the fundamental structure
of VDS data in xarray and how to interact with it.

Step 1: Import Required Libraries
----------------------------------

Let's start by importing the libraries we'll need:

.. code-block:: python

   import xarray as xr
   import numpy as np

   # Optional: for better display in Jupyter
   import warnings
   warnings.filterwarnings('ignore')

The main library we need is ``xarray`` (imported as ``xr``). The vdsxarray backend
is automatically registered when installed.

Step 2: Open Your First VDS File
---------------------------------

Opening a VDS file is straightforward:

.. code-block:: python

   # Replace with your actual file path
   file_path = "path/to/your/seismic.vds"

   # Open the VDS file
   ds = xr.open_dataset(file_path, engine="vds")

   print("Dataset opened successfully!")
   print(ds)

The ``engine="vds"`` parameter tells xarray to use the vdsxarray backend.

**Expected output**:

.. code-block:: text

   Dataset opened successfully!
   <xarray.Dataset>
   Dimensions:    (inline: 1401, crossline: 1351, sample: 2741)
   Coordinates:
     * inline     (inline) int16 1300 1301 1302 ... 2698 2699 2700
     * crossline  (crossline) int16 2500 2502 2504 ... 5196 5198 5200
     * sample     (sample) float32 0.0 3.048 6.096 ... 8348.0 8352.0
   Data variables:
       Amplitude  (inline, crossline, sample) float32 dask.array<...>
   Attributes:
       title:         VDS Seismic Data: Amplitude
       source:        path/to/your/seismic.vds
       created_with:  vdsxarray

Step 3: Understanding the Dataset Structure
--------------------------------------------

Let's break down what we see:

Dimensions
~~~~~~~~~~

.. code-block:: python

   print("Dataset dimensions:")
   print(dict(ds.dims))

Output:

.. code-block:: python

   {'inline': 1401, 'crossline': 1351, 'sample': 2741}

The dataset has three dimensions:

- **inline**: Survey lines (typically running N-S), 1401 lines
- **crossline**: Lines perpendicular to inline (typically E-W), 1351 lines
- **sample**: Time or depth samples (vertical axis), 2741 samples

Coordinates
~~~~~~~~~~~

Coordinates map dimension indices to real-world values:

.. code-block:: python

   print("\\nInline coordinates:")
   print(f"  Range: {ds.inline.min().values} to {ds.inline.max().values}")
   print(f"  Type: {ds.inline.dtype}")

   print("\\nCrossline coordinates:")
   print(f"  Range: {ds.crossline.min().values} to {ds.crossline.max().values}")
   print(f"  Type: {ds.crossline.dtype}")

   print("\\nSample coordinates:")
   print(f"  Range: {ds.sample.min().values} to {ds.sample.max().values}")
   print(f"  Type: {ds.sample.dtype}")
   print(f"  Units: milliseconds (ms)")

Data Variables
~~~~~~~~~~~~~~

The main data is stored in the ``Amplitude`` variable:

.. code-block:: python

   print("\\nAmplitude data:")
   print(ds.Amplitude)

Output:

.. code-block:: text

   <xarray.DataArray 'Amplitude' (inline: 1401, crossline: 1351, sample: 2741)>
   dask.array<...>
   Coordinates:
     * inline     (inline) int16 1300 1301 1302 ... 2698 2699 2700
     * crossline  (crossline) int16 2500 2502 2504 ... 5196 5198 5200
     * sample     (sample) float32 0.0 3.048 6.096 ... 8348.0 8352.0

Notice ``dask.array`` - this means the data is **lazily loaded** and not yet in memory!

Step 4: Checking Data Properties
---------------------------------

Let's verify the data is chunked for efficient processing:

.. code-block:: python

   amplitude = ds.Amplitude

   print(f"Is chunked? {amplitude.chunks is not None}")
   print(f"Chunk sizes: {amplitude.chunksizes}")
   print(f"Total size: {amplitude.nbytes / 1e9:.2f} GB")
   print(f"Memory per chunk: {(128**3 * 4) / 1e6:.2f} MB")  # 128^3 float32 values

**Expected output**:

.. code-block:: text

   Is chunked? True
   Chunk sizes: {'inline': (128, 128, ...), 'crossline': (128, 128, ...), 'sample': (128, 128, ...)}
   Total size: 20.85 GB
   Memory per chunk: 8.39 MB

The data is divided into 128×128×128 chunks for efficient processing.

Step 5: Accessing Coordinate Arrays
------------------------------------

Get the actual coordinate values:

.. code-block:: python

   # Get coordinate arrays
   inlines = ds.inline.values
   crosslines = ds.crossline.values
   samples = ds.sample.values

   print(f"First 5 inline values: {inlines[:5]}")
   print(f"First 5 crossline values: {crosslines[:5]}")
   print(f"First 5 sample values: {samples[:5]}")

   print(f"\\nInline spacing: {inlines[1] - inlines[0]}")
   print(f"Crossline spacing: {crosslines[1] - crosslines[0]}")
   print(f"Sample interval: {samples[1] - samples[0]:.3f} ms")

Step 6: Selecting Data
-----------------------

There are two ways to select data: by index or by coordinate value.

By Coordinate Value (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Select a single inline
   inline_1500 = ds.sel(inline=1500)
   print(f"Selected inline 1500: {inline_1500.dims}")

   # Select a range of inlines
   inline_range = ds.sel(inline=slice(1400, 1600))
   print(f"\\nSelected inlines 1400-1600:")
   print(f"  Shape: {inline_range.Amplitude.shape}")

   # Select nearest value (useful for approximate matches)
   time_slice = ds.sel(sample=100, method='nearest')
   print(f"\\nSelected nearest to sample=100:")
   print(f"  Actual sample value: {time_slice.sample.values}")

By Index Position
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Select by integer position
   first_inline = ds.isel(inline=0)
   print(f"First inline (by index): {first_inline.inline.values}")

   middle_inline = ds.isel(inline=len(ds.inline)//2)
   print(f"Middle inline (by index): {middle_inline.inline.values}")

Step 7: Extracting a Single Trace
----------------------------------

Extract a single seismic trace (1D) by specifying inline and crossline:

.. code-block:: python

   # Extract trace at inline=1500, crossline=2500
   trace = ds.Amplitude.sel(inline=1500, crossline=2500)

   print(f"Trace shape: {trace.shape}")
   print(f"Trace dimensions: {trace.dims}")
   print(f"Trace coordinates: {trace.coords}")

   # Get the actual values (this triggers computation!)
   trace_values = trace.values
   print(f"\\nFirst 10 amplitude values: {trace_values[:10]}")

Step 8: Extracting a 2D Section
--------------------------------

Extract 2D seismic sections:

.. code-block:: python

   # Inline section (crossline vs sample)
   inline_section = ds.Amplitude.sel(inline=1500)
   print(f"Inline section shape: {inline_section.shape}")
   print(f"Inline section dims: {inline_section.dims}")

   # Crossline section (inline vs sample)
   crossline_section = ds.Amplitude.sel(crossline=2500)
   print(f"\\nCrossline section shape: {crossline_section.shape}")

   # Time slice (inline vs crossline)
   time_slice = ds.Amplitude.sel(sample=200, method='nearest')
   print(f"\\nTime slice shape: {time_slice.shape}")

Step 9: Extracting a 3D Subset
-------------------------------

Extract a 3D volume subset:

.. code-block:: python

   # Define subset bounds
   subset = ds.sel(
       inline=slice(1400, 1600),      # 200 inlines
       crossline=slice(2400, 2600),   # 200 crosslines
       sample=slice(0, 1000)          # First 1000 ms
   )

   print(f"Subset shape: {subset.Amplitude.shape}")
   print(f"Subset size: {subset.Amplitude.nbytes / 1e6:.2f} MB")

   # The subset is still lazy - no data loaded yet!
   print(f"Is still a dask array? {hasattr(subset.Amplitude.data, 'compute')}")

Step 10: Computing Values
--------------------------

To actually load data into memory, use ``.compute()`` or ``.values``:

.. code-block:: python

   # Get a small subset
   small_subset = ds.sel(
       inline=slice(1500, 1510),
       crossline=slice(2500, 2510),
       sample=slice(0, 100)
   )

   # Option 1: Use .values (loads immediately)
   data_values = small_subset.Amplitude.values
   print(f"Loaded data shape: {data_values.shape}")
   print(f"Data type: {type(data_values)}")

   # Option 2: Use .compute() (returns xarray object)
   computed_data = small_subset.Amplitude.compute()
   print(f"\\nComputed data type: {type(computed_data)}")

Step 11: Basic Statistics
--------------------------

Calculate statistics on the data:

.. code-block:: python

   # Statistics on the entire dataset (computed lazily)
   print("Computing statistics on full dataset...")

   mean_amp = ds.Amplitude.mean().compute()
   min_amp = ds.Amplitude.min().compute()
   max_amp = ds.Amplitude.max().compute()

   print(f"Mean amplitude: {mean_amp.values:.3f}")
   print(f"Min amplitude: {min_amp.values:.3f}")
   print(f"Max amplitude: {max_amp.values:.3f}")

   # RMS amplitude
   rms = np.sqrt((ds.Amplitude ** 2).mean()).compute()
   print(f"RMS amplitude: {rms.values:.3f}")

Step 12: Saving Your Work
--------------------------

Save subsets or processed data:

.. code-block:: python

   # Save a subset to NetCDF
   subset = ds.sel(
       inline=slice(1400, 1600),
       crossline=slice(2400, 2600)
   )

   # This will compute and save the data
   subset.to_netcdf("seismic_subset.nc")
   print("Subset saved to seismic_subset.nc")

   # Save a single trace to CSV
   trace = ds.Amplitude.sel(inline=1500, crossline=2500)
   trace_df = trace.to_dataframe()
   trace_df.to_csv("trace_1500_2500.csv")
   print("Trace saved to CSV")

Complete Example
----------------

Here's the complete workflow:

.. code-block:: python

   import xarray as xr
   import numpy as np

   # 1. Open dataset
   ds = xr.open_dataset("path/to/seismic.vds", engine="vds")

   # 2. Explore structure
   print("Dataset structure:")
   print(ds)

   # 3. Check dimensions and coordinates
   print(f"\\nDimensions: {dict(ds.dims)}")
   print(f"Inline range: {ds.inline.min().values}-{ds.inline.max().values}")
   print(f"Crossline range: {ds.crossline.min().values}-{ds.crossline.max().values}")
   print(f"Sample range: {ds.sample.min().values}-{ds.sample.max().values} ms")

   # 4. Extract data
   inline_section = ds.Amplitude.sel(inline=1500)
   trace = ds.Amplitude.sel(inline=1500, crossline=2500)

   # 5. Calculate statistics
   rms = np.sqrt((ds.Amplitude ** 2).mean()).compute()
   print(f"\\nRMS amplitude: {rms.values:.3f}")

   # 6. Save subset
   subset = ds.sel(inline=slice(1400, 1600))
   subset.to_netcdf("subset.nc")

   print("\\nTutorial complete!")

Summary
-------

In this tutorial, you learned:

✓ How to open VDS files with xarray
✓ Understanding dataset structure (dimensions, coordinates, data variables)
✓ The difference between lazy and computed data
✓ Selecting data by coordinate value vs. index
✓ Extracting 1D traces, 2D sections, and 3D subsets
✓ Computing basic statistics
✓ Saving results to file

Next Steps
----------

- Continue to :doc:`visualization` to learn how to create seismic plots
- Explore :doc:`../howto/selection-slicing` for advanced selection techniques
- Read :doc:`../explanation/lazy-loading` to understand lazy evaluation in depth

Exercises
---------

Try these exercises to reinforce your learning:

1. Open your own VDS file and print its dimensions
2. Extract the middle inline section
3. Calculate the mean amplitude for a subset of the data
4. Extract a single trace and find its maximum value
5. Create a 3D subset covering the center 100×100 inlines/crosslines
