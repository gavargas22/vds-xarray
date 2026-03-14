Chunking Strategy
=================

Default Chunk Sizes
-------------------

VDSXarray uses default chunk sizes of **128 × 128 × 128** for:

- inline: 128
- crossline: 128
- sample: 128

This results in approximately **8.39 MB per chunk** (128³ × 4 bytes for float32).

Chunk Size Optimization
------------------------

The chunk size is chosen to balance:

1. **Memory efficiency**: Small enough to fit in cache
2. **I/O efficiency**: Large enough to minimize read operations
3. **Parallelization**: Enables effective Dask parallelization

Custom Chunking
---------------

You can rechunk data after loading:

.. code-block:: python

   ds = xr.open_dataset("file.vds", engine="vds")

   # Rechunk for different access patterns
   rechunked = ds.chunk({
       'inline': 256,
       'crossline': 256,
       'sample': 64
   })

Chunking Guidelines
-------------------

**For inline/crossline access**:
   Larger inline/crossline chunks, smaller sample chunks

**For time slice access**:
   Smaller inline/crossline chunks, larger sample chunks

**For full volume processing**:
   Use default balanced chunks
