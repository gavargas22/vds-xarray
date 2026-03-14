VDS Format
==========

Volume Data Store (VDS) is a cloud-optimized format for storing 3D seismic survey data.

Format Overview
---------------

VDS was developed by Bluware/OSDU for efficient storage and access of seismic volumes.

Key characteristics:

- **3D volume structure**: inline, crossline, sample dimensions
- **Chunked storage**: Optimized for efficient access patterns
- **Compression**: Built-in compression for reduced storage
- **Metadata**: Rich header information
- **Cloud-optimized**: Designed for modern cloud workflows

Dimension Structure
-------------------

.. list-table::
   :header-rows: 1

   * - Dimension
     - Axis Index
     - Description
     - Data Type
   * - inline
     - 0
     - Survey line direction
     - int16
   * - crossline
     - 1
     - Perpendicular to inline
     - int16
   * - sample
     - 2
     - Time or depth (vertical)
     - float32

Volume data itself is float32 amplitude values.

Dependencies
------------

VDSXarray uses:

- **openvds** (>=3.4.6): Bluware's C++ SDK with Python bindings
- **ovds-utils** (>=0.3.1): Python convenience wrapper around openvds

The code uses ``ovds-utils.vds.VDS`` class exclusively and does not call ``openvds`` directly.

For more details, see :doc:`../TECHNICAL-OVERVIEW`.
