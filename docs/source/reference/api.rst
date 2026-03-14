API Reference
=============

This page contains auto-generated API documentation for vdsxarray.

VDS Backend Engine
------------------

.. autoclass:: vdsxarray.VdsEngine
   :members:
   :undoc-members:
   :show-inheritance:

Backend Array
-------------

.. autoclass:: vdsxarray.vds.VdsBackendArray
   :members:
   :undoc-members:
   :show-inheritance:

Coordinate Functions
--------------------

.. autofunction:: vdsxarray.vds.get_annotated_coordinates

.. autofunction:: vdsxarray.vds.get_cdp_coordinates

Utility Functions
-----------------

.. automodule:: vdsxarray.utils
   :members:
   :undoc-members:
   :show-inheritance:

Package Information
-------------------

.. autodata:: vdsxarray.__version__
   :annotation: = version string

Constants
---------

Default chunk size: 128 × 128 × 128

Default data format: float32

Dimension order: (inline, crossline, sample)
