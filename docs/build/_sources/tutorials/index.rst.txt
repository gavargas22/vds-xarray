Tutorials
=========

.. admonition:: Learning-Oriented
   :class: note

   Tutorials are **learning-oriented** lessons that take you through a series of steps
   to complete a meaningful project. They are designed for newcomers to vdsxarray.

   **Goal**: Build confidence and familiarity through hands-on practice.

Welcome to the vdsxarray tutorials! These step-by-step guides will help you learn how to work with VDS seismic data using xarray.

Who These Tutorials Are For
----------------------------

These tutorials are designed for:

- Geophysicists and seismic data analysts new to Python
- Python developers new to seismic data processing
- Data scientists exploring geophysical applications
- Anyone wanting to learn vdsxarray from scratch

What You'll Learn
-----------------

Through these tutorials, you'll learn to:

1. Open and explore VDS seismic datasets
2. Visualize seismic sections and attributes
3. Perform common seismic data analysis tasks
4. Handle large datasets efficiently
5. Export and share your results

Prerequisites
-------------

Before starting, you should have:

- Basic Python knowledge (variables, functions, loops)
- Familiarity with Jupyter notebooks (recommended)
- vdsxarray installed (see :doc:`../installation`)
- Access to VDS seismic data files

Tutorial Path
-------------

Follow these tutorials in order for the best learning experience:

.. toctree::
   :maxdepth: 1

   first-dataset
   visualization
   data-analysis
   large-datasets

Tutorial Overview
-----------------

1. Your First VDS Dataset
~~~~~~~~~~~~~~~~~~~~~~~~~~

:doc:`first-dataset`

Learn the fundamentals by opening your first VDS file, exploring its structure,
and understanding coordinates and dimensions.

**Time**: 15-20 minutes

**You'll learn**:

- How to open VDS files
- Dataset structure and components
- Accessing data and coordinates
- Basic data selection

2. Visualizing Seismic Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:doc:`visualization`

Create professional seismic visualizations including inline/crossline sections,
time slices, and attribute maps.

**Time**: 30-40 minutes

**You'll learn**:

- Plotting seismic sections
- Creating time slices
- Multi-panel visualizations
- Customizing colormaps and labels

3. Seismic Data Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~

:doc:`data-analysis`

Perform common seismic analysis tasks including statistical analysis,
attribute calculation, and spectral analysis.

**Time**: 45-60 minutes

**You'll learn**:

- Statistical analysis
- RMS amplitude calculation
- Frequency spectrum analysis
- Seismic attribute computation

4. Working with Large Datasets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:doc:`large-datasets`

Master techniques for efficiently processing large seismic volumes that don't
fit in memory.

**Time**: 30-45 minutes

**You'll learn**:

- Lazy loading strategies
- Chunked processing with Dask
- Memory management
- Progress monitoring

Next Steps
----------

After completing the tutorials:

- Explore :doc:`../howto/index` for solutions to specific problems
- Check :doc:`../reference/index` for detailed API documentation
- Read :doc:`../explanation/index` to understand design decisions

Getting Help
------------

If you get stuck:

1. Review the :doc:`../quickstart` guide
2. Check the :doc:`../howto/troubleshooting` section
3. Open an issue on `GitHub <https://github.com/gavargas22/vds-xarray-backend/issues>`_
