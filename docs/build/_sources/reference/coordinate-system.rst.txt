Coordinate System
=================

VDS Coordinate Mapping
-----------------------

VDS files use a 3D coordinate system that maps to xarray dimensions:

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - Dimension
     - VDS Axis
     - Data Type
     - Description
   * - inline
     - Axis 0
     - int16
     - Survey line direction (typically N-S)
   * - crossline
     - Axis 1
     - int16
     - Perpendicular to inline (typically E-W)
   * - sample
     - Axis 2
     - float32
     - Time or depth (vertical axis)

Coordinate Generation
---------------------

Coordinates are generated using:

.. code-block:: python

   np.linspace(
       start=axis.coordinate_min,
       stop=axis.coordinate_max,
       num=shape[axis_index],
       dtype=dtype
   )

Coordinate Ranges
-----------------

Coordinate ranges are extracted from VDS axis metadata and stored in dataset attributes:

.. code-block:: python

   ds.attrs['coordinate_ranges'] = {
       'inline': [min_inline, max_inline],
       'crossline': [min_crossline, max_crossline],
       'sample': [min_sample, max_sample]
   }
