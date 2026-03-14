Design Decisions
================

Key design decisions and their rationale.

Default Chunk Size: 128³
-------------------------

**Decision**: Use 128×128×128 chunks by default

**Rationale**:

- Balanced for memory efficiency (~8.4 MB per chunk)
- Large enough for efficient I/O
- Small enough to fit in CPU cache
- Enables good parallelization with Dask

Dimension Order: (inline, crossline, sample)
---------------------------------------------

**Decision**: Use (inline, crossline, sample) dimension order

**Rationale**:

- Matches seismic industry conventions
- Inline sections are common visualization
- Sample (time/depth) as innermost dimension
- Consistent with most seismic software

Using ovds-utils Over Direct openvds
-------------------------------------

**Decision**: Use ``ovds-utils.vds.VDS`` instead of calling ``openvds`` directly

**Rationale**:

- Simpler Python interface
- Less boilerplate code
- Maintained wrapper with conveniences
- Easier testing and mocking

Lazy Loading by Default
------------------------

**Decision**: All data is lazy-loaded via Dask

**Rationale**:

- Enables working with datasets larger than memory
- Users explicitly control when computation happens
- Consistent with xarray ecosystem conventions
- Better performance for subset operations

No Eager Metadata Loading
--------------------------

**Decision**: Extract only essential metadata on open

**Rationale**:

- Fast dataset opening
- Minimal memory footprint
- Metadata extracted on-demand
- User can access additional metadata if needed

For architectural details, see :doc:`architecture`.
