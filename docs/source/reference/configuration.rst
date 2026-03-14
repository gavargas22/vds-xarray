Configuration
=============

``open_dataset`` Parameters
----------------------------

.. code-block:: python

   xr.open_dataset(
       filename_or_obj,
       engine="vds",
       drop_variables=None,
       volume_format="float32",
       name="Amplitude",
       channels=None,
       LOD=0,
       calculate_cdp=False
   )

Parameters
~~~~~~~~~~

**filename_or_obj** : str or Path
   Path to the VDS file

**drop_variables** : list, optional
   Variables to drop (not used for VDS)

**volume_format** : str, default "float32"
   Data format to use

**name** : str, default "Amplitude"
   Name for the data variable

**channels** : list, optional
   Specific channels to read

**LOD** : int, default 0
   Level of detail

**calculate_cdp** : bool, default False
   Whether to calculate CDP coordinates (not yet implemented)

Environment Variables
---------------------

None currently supported.

Dask Configuration
------------------

Configure Dask behavior:

.. code-block:: python

   import dask

   dask.config.set({
       'array.chunk-size': '128MB',
       'array.slicing.split_large_chunks': True
   })
