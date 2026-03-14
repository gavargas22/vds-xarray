Visualization Recipes
=====================

.. _howto-create-sections:

How to Create Seismic Sections
-------------------------------

.. code-block:: python

   import matplotlib.pyplot as plt

   ds.Amplitude.sel(inline=1500).plot(
       x='crossline',
       y='sample',
       cmap='seismic',
       robust=True
   )
   plt.gca().invert_yaxis()
   plt.show()

How to Create Attribute Maps
-----------------------------

.. code-block:: python

   import numpy as np

   rms_map = np.sqrt((ds.Amplitude ** 2).mean('sample'))
   rms_map.plot(x='crossline', y='inline', cmap='viridis')
   plt.show()

For more visualization recipes, see :doc:`../USER-GUIDE`.
