VDSXarray Documentation
========================

.. image:: https://badge.fury.io/py/vdsxarray.svg
   :target: https://badge.fury.io/py/vdsxarray
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/vdsxarray.svg
   :target: https://pypi.org/project/vdsxarray/
   :alt: Python versions

.. image:: https://img.shields.io/github/license/gavargas22/vds-xarray-backend.svg
   :target: https://github.com/gavargas22/vds-xarray-backend/blob/main/LICENSE
   :alt: License

An xarray backend for reading VDS (Volume Data Store) files, commonly used in seismic data processing and geophysical applications.

**VDSXarray** enables seamless integration of VDS seismic data into the Python scientific computing ecosystem through the xarray interface, providing lazy loading, chunked processing with Dask, and intuitive coordinate-based indexing.

Quick Start
-----------

.. code-block:: python

   import xarray as xr

   # Open a VDS file
   ds = xr.open_dataset("path/to/your/file.vds", engine="vds")

   # Access seismic amplitude data
   amplitude = ds.Amplitude

   # Visualize a seismic section
   ds.Amplitude.sel(inline=1500).plot(x='crossline', y='sample', cmap='seismic')


.. grid:: 2
   :gutter: 3

   .. grid-item-card:: 📚 Tutorials
      :link: tutorials/index
      :link-type: doc

      Learning-oriented lessons that take you through a series of steps to complete a project.
      Start here if you're new to vdsxarray!

   .. grid-item-card:: 📖 How-To Guides
      :link: howto/index
      :link-type: doc

      Step-by-step guides to solve specific problems and accomplish specific tasks.
      Practical recipes for common workflows.

   .. grid-item-card:: 📋 Reference
      :link: reference/index
      :link-type: doc

      Technical reference material including API documentation, configuration options,
      and detailed specifications.

   .. grid-item-card:: 💡 Explanation
      :link: explanation/index
      :link-type: doc

      Discussion and clarification of key topics. Understand the "why" behind
      design decisions and architecture.

   .. grid-item-card:: 🤖 AI Agents
      :link: ai-agents/index
      :link-type: doc

      Comprehensive guide for AI coding agents working on this repository.
      Architecture, conventions, and guardrails.

   .. grid-item-card:: 🚀 Getting Started
      :link: installation
      :link-type: doc

      Installation instructions and first steps to get up and running
      with vdsxarray.


Documentation Structure (Diátaxis Framework)
---------------------------------------------

This documentation follows the `Diátaxis framework <https://diataxis.fr/>`_, organizing content into four distinct categories:

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Category
     - Purpose
     - When to Use
   * - **Tutorials**
     - Learning by doing
     - When you want to learn the basics through hands-on lessons
   * - **How-To Guides**
     - Problem-oriented solutions
     - When you have a specific task to accomplish
   * - **Reference**
     - Information-oriented descriptions
     - When you need to look up technical details
   * - **Explanation**
     - Understanding-oriented discussions
     - When you want to understand concepts and design decisions


.. toctree::
   :maxdepth: 2
   :caption: Getting Started
   :hidden:

   installation
   quickstart


.. toctree::
   :maxdepth: 2
   :caption: Tutorials (Learning-Oriented)
   :hidden:

   tutorials/index
   tutorials/first-dataset
   tutorials/visualization
   tutorials/data-analysis
   tutorials/large-datasets


.. toctree::
   :maxdepth: 2
   :caption: How-To Guides (Problem-Oriented)
   :hidden:

   howto/index
   howto/selection-slicing
   howto/visualization-recipes
   howto/export-data
   howto/performance-optimization
   howto/integration
   howto/troubleshooting


.. toctree::
   :maxdepth: 2
   :caption: Reference (Information-Oriented)
   :hidden:

   reference/index
   reference/api
   reference/coordinate-system
   reference/chunking
   reference/backend-protocol
   reference/configuration


.. toctree::
   :maxdepth: 2
   :caption: Explanation (Understanding-Oriented)
   :hidden:

   explanation/index
   explanation/why-xarray
   explanation/vds-format
   explanation/architecture
   explanation/lazy-loading
   explanation/design-decisions


.. toctree::
   :maxdepth: 2
   :caption: For AI Agents
   :hidden:

   ai-agents/index
   ai-agents/architecture
   ai-agents/development
   ai-agents/testing
   ai-agents/guardrails


.. toctree::
   :maxdepth: 2
   :caption: Development
   :hidden:

   contributing
   changelog
   license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
