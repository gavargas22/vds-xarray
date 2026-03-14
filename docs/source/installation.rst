Installation
============

Requirements
------------

VDSXarray requires:

- Python >=3.9, <3.12
- xarray >=2024.7.0
- openvds >=3.4.6
- ovds-utils >=0.3.1
- dask >=2024.8.0

Installing from PyPI
--------------------

The easiest way to install vdsxarray is via pip:

.. code-block:: bash

   pip install vdsxarray

This will install vdsxarray and all required dependencies.

Using uv (Recommended)
----------------------

For faster and more reliable dependency resolution, we recommend using `uv <https://github.com/astral-sh/uv>`_:

.. code-block:: bash

   uv add vdsxarray

Installing from Source
----------------------

For Development
~~~~~~~~~~~~~~~

If you want to contribute to vdsxarray or need the latest development version:

.. code-block:: bash

   git clone https://github.com/gavargas22/vds-xarray-backend.git
   cd vds-xarray-backend
   uv sync --group dev --group test

This will:

1. Clone the repository
2. Install vdsxarray in editable mode
3. Install development dependencies (testing, linting)
4. Install test dependencies

For Users
~~~~~~~~~

To install the latest development version:

.. code-block:: bash

   pip install git+https://github.com/gavargas22/vds-xarray-backend.git

Verification
------------

Verify your installation by running:

.. code-block:: python

   import vdsxarray
   print(vdsxarray.__version__)

You should also be able to use the VDS engine with xarray:

.. code-block:: python

   import xarray as xr

   # The 'vds' engine should be available
   from vdsxarray import VdsEngine
   print("VDS backend installed successfully!")

Troubleshooting
---------------

OpenVDS Installation Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you encounter issues with the ``openvds`` package:

.. code-block:: bash

   # Try installing openvds separately first
   pip install openvds>=3.4.6

Platform-Specific Issues
~~~~~~~~~~~~~~~~~~~~~~~~

**Windows**

On Windows, ensure you have the Microsoft Visual C++ Redistributable installed, as it's required by OpenVDS.

**Linux**

On Linux, you might need additional system libraries:

.. code-block:: bash

   # Ubuntu/Debian
   sudo apt-get install libgomp1

   # RHEL/CentOS
   sudo yum install libgomp

**macOS**

On macOS with Apple Silicon (M1/M2), ensure you're using a compatible Python version:

.. code-block:: bash

   # Check your Python architecture
   python -c "import platform; print(platform.machine())"

Dependency Conflicts
~~~~~~~~~~~~~~~~~~~~

If you encounter dependency conflicts:

.. code-block:: bash

   # Create a fresh virtual environment
   python -m venv vdsxarray-env
   source vdsxarray-env/bin/activate  # On Windows: vdsxarray-env\\Scripts\\activate
   pip install vdsxarray

Optional Dependencies
---------------------

For Enhanced Functionality
~~~~~~~~~~~~~~~~~~~~~~~~~~

Install optional dependencies for additional features:

.. code-block:: bash

   # For visualization
   pip install matplotlib hvplot

   # For Jupyter notebook support
   pip install jupyter ipykernel

   # For advanced data export
   pip install zarr h5netcdf

All Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~

To install all optional dependencies at once:

.. code-block:: bash

   pip install vdsxarray[all]

Next Steps
----------

After installation, proceed to the :doc:`quickstart` guide to learn how to use vdsxarray.
