# VDS Xarray Backend

[![PyPI version](https://badge.fury.io/py/vdsxarray.svg)](https://badge.fury.io/py/vdsxarray)
[![Python versions](https://img.shields.io/pypi/pyversions/vdsxarray.svg)](https://pypi.org/project/vdsxarray/)
[![License](https://img.shields.io/github/license/gavargas22/vds-xarray-backend.svg)](https://github.com/gavargas22/vds-xarray-backend/blob/main/LICENSE)

An xarray backend for reading VDS (Volume Data Store) files, commonly used in seismic data processing and geophysical applications.

## Installation

Install from PyPI:
```bash
pip install vdsxarray
```

Using uv:
```bash
uv add vdsxarray
```

For development:
```bash
git clone https://github.com/gavargas22/vds-xarray-backend.git
cd vds-xarray-backend
uv sync --group dev --group test
```

## Usage

```python
import xarray as xr

# Open a VDS file
ds = xr.open_dataset("path/to/your/file.vds", engine="vds")

# The dataset will contain seismic data with proper coordinates
print(ds)

# Access the amplitude data
amplitude = ds.Amplitude

# Data is lazily loaded and can be used with dask
print(amplitude.dims)  # ('sample', 'crossline', 'inline')
print(amplitude.coords)  # Shows coordinate ranges
```

## Features

- **Lazy loading**: Data is loaded on-demand using dask arrays
- **Proper coordinates**: Automatically extracts inline, crossline, and sample coordinates
- **Chunking**: Optimized chunk sizes for efficient processing
- **Metadata**: Includes coordinate ranges and source file information

## 📚 Documentation

For comprehensive documentation, examples, and technical details, see our [documentation directory](docs/):

- **[Why Xarray?](docs/WHY-XARRAY.md)** - Understanding the benefits and motivation
- **[User Guide](docs/USER-GUIDE.md)** - Practical examples and workflows  
- **[Technical Overview](docs/TECHNICAL-OVERVIEW.md)** - Architecture and implementation details

## Quick Example

```python
import xarray as xr
import matplotlib.pyplot as plt

# Open VDS file
ds = xr.open_dataset("survey.vds", engine="vds")

# Explore the dataset
print(f"Survey dimensions: {dict(ds.dims)}")
print(f"Coordinate ranges:")
print(f"  Inline: {ds.inline.min().values} - {ds.inline.max().values}")
print(f"  Crossline: {ds.crossline.min().values} - {ds.crossline.max().values}")
print(f"  Sample: {ds.sample.min().values} - {ds.sample.max().values} ms")

# Visualize seismic section
ds.Amplitude.sel(inline=1500).plot(
    x='crossline', y='sample', 
    cmap='seismic', robust=True
)
plt.gca().invert_yaxis()  # Time increases downward
plt.title('Seismic Section - Inline 1500')
plt.show()

# Calculate and plot RMS amplitude map
rms_amp = (ds.Amplitude ** 2).mean('sample') ** 0.5
rms_amp.plot(x='crossline', y='inline', cmap='viridis')
plt.title('RMS Amplitude Map')
plt.show()
```

## Requirements

- Python >=3.9, <3.12
- xarray >=2024.7.0
- openvds >=3.4.6
- ovds-utils >=0.3.1
- dask >=2024.8.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Workflow

1. **Setup development environment:**
   ```bash
   git clone https://github.com/gavargas22/vds-xarray-backend.git
   cd vds-xarray-backend
   uv sync --group dev --group test
   ```

2. **Run tests:**
   ```bash
   uv run pytest
   ```

3. **Run linting:**
   ```bash
   uv run ruff check .
   uv run black --check .
   uv run isort --check-only .
   ```

### Releasing

This project uses automated releases via GitHub Actions:

**Automated Release (Recommended):**
1. Use the release helper script:
   ```bash
   ./scripts/release.sh
   ```
   This will update versions, run tests, and create a tag to trigger the release.

**Manual Release:**
1. Update version in `pyproject.toml` and `vdsxarray/__init__.py`
2. Create and push a tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. GitHub Actions will automatically:
   - Build the package
   - Create a GitHub release with wheel files
   - Publish to PyPI (for stable releases)

**Manual Release Workflow:**
You can also use the GitHub Actions manual release workflow to create releases with custom options.

**This line will be removed, it is only for testing PRs**

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on top of the excellent [xarray](https://xarray.pydata.org/) library
- Uses [OpenVDS](https://osdu.pages.opengroup.org/platform/domain-data-mgmt-services/seismic/open-vds/) for VDS file access
- Powered by [dask](https://dask.org/) for lazy loading and parallel computing
