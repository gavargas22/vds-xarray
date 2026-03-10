# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-08-13

### Added
- Initial release of vdsxarray
- VDS backend for xarray with lazy loading support
- Automatic coordinate extraction (inline, crossline, sample)
- Optimized chunking for efficient processing
- Dask array integration for large seismic datasets
- Proper metadata extraction from VDS files

### Features
- Read VDS files using `xr.open_dataset("file.vds", engine="vds")`
- Lazy loading with dask arrays
- Automatic coordinate system detection
- Memory-efficient chunking strategy
- Integration with xarray ecosystem

### Dependencies
- xarray >=2024.7.0
- openvds >=3.4.6
- ovds-utils >=0.3.1
- dask >=2024.8.0
- Python >=3.9, <3.12
