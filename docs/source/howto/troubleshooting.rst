Troubleshooting
===============

Common Issues and Solutions
----------------------------

File Not Found
~~~~~~~~~~~~~~

.. code-block:: python

   try:
       ds = xr.open_dataset('file.vds', engine='vds')
   except FileNotFoundError:
       print("Check file path and permissions")

Memory Errors
~~~~~~~~~~~~~

.. code-block:: python

   # Solution: Process smaller chunks
   subset = ds.sel(inline=slice(1000, 1200))
   result = subset.Amplitude.mean().compute()

Slow Performance
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Check and optimize chunk sizes
   print(ds.chunks)
   rechunked = ds.chunk({'inline': 128, 'crossline': 128, 'sample': 128})

Coordinate Misalignment
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Use method='nearest' for approximate matching
   value = ds.sel(sample=100.5, method='nearest')

For more help, see :doc:`../USER-GUIDE` or open an issue on GitHub.
