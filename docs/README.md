# VDS Xarray Backend Documentation

Welcome to the VDS Xarray Backend - a powerful library that brings the VDS (Volume Data Store) format into the modern scientific Python ecosystem through xarray.

## 📚 Documentation Structure

### 🌟 [Why Xarray?](WHY-XARRAY.md)
**Essential reading for understanding the motivation behind this project**

- What is xarray and why it matters for seismic data
- How VDS + Xarray creates a powerful combination
- Real-world benefits with concrete examples
- Performance advantages and use cases

*Perfect for: Geophysicists new to xarray, managers evaluating tools, scientists considering adoption*

### 🛠️ [Technical Overview](TECHNICAL-OVERVIEW.md)
**Deep dive into the architecture and implementation**

- Backend engine architecture
- Integration with OpenVDS and dask
- Performance optimizations and chunking strategies
- Extensibility and plugin system
- Testing and deployment considerations

*Perfect for: Developers, technical implementers, anyone extending the library*

### 📖 [User Guide](USER-GUIDE.md)
**Comprehensive practical guide with examples**

- Getting started and basic operations
- Data visualization and analysis workflows
- Working with large datasets efficiently
- Advanced seismic processing examples
- Performance tips and troubleshooting

*Perfect for: Daily users, seismic analysts, researchers, anyone doing hands-on work*

## 🚀 Quick Start

```python
# Install
pip install vdsxarray

# Use
import xarray as xr
ds = xr.open_dataset('your_survey.vds', engine='vds')

# Explore
print(ds)
ds.Amplitude.sel(inline=1500).plot(x='crossline', y='sample')
```

## 📊 Key Concepts at a Glance

| Concept | Description | Benefit |
|---------|-------------|---------|
| **Lazy Loading** | Data loaded only when needed | Work with datasets larger than memory |
| **Coordinate-Aware** | Operations use real coordinates, not indices | Prevent errors, intuitive operations |
| **Chunked Processing** | Automatic parallel processing with dask | Faster computation, scalable workflows |
| **Rich Metadata** | Preserve acquisition and processing info | Better reproducibility and documentation |
| **Ecosystem Integration** | Seamless with pandas, matplotlib, scipy | Leverage entire scientific Python stack |

## 🎯 Use Cases

### For Seismic Interpreters
- **Interactive exploration** of large 3D surveys
- **Multi-attribute analysis** with coordinate awareness
- **Time-slice and section visualization** with proper coordinates
- **Quality control** workflows with statistical analysis

### For Processing Geophysicists
- **Algorithm development** with chunked, parallel processing
- **Large-scale processing** workflows that scale to any dataset size
- **Multi-vintage analysis** and 4D seismic studies
- **Custom attribute computation** with full metadata preservation

### For Research Scientists
- **Machine learning** on seismic data with easy array access
- **Statistical analysis** with coordinate-aware operations
- **Method development** with immediate visualization capabilities
- **Reproducible research** with rich metadata and provenance tracking

### For Data Engineers
- **Cloud-native workflows** with zarr export capabilities
- **ETL pipelines** with robust error handling
- **Data validation** and quality assurance automation
- **Format conversion** between VDS, NetCDF, and other formats

## 🔧 Integration Examples

### With Machine Learning
```python
# Extract features for ML
features = ds.Amplitude.values.reshape(-1, ds.sizes['sample'])
from sklearn.cluster import KMeans
clusters = KMeans(n_clusters=5).fit(features)
```

### With Cloud Workflows
```python
# Export to cloud-friendly format
ds.to_zarr('s3://my-bucket/seismic-data.zarr')

# Process with dask distributed
from dask.distributed import Client
client = Client('scheduler-address')
result = ds.Amplitude.mean().compute()
```

### With Visualization Tools
```python
# Interactive plotting with hvplot
import hvplot.xarray
ds.Amplitude.hvplot.image(x='crossline', y='sample', by='inline')

# 3D visualization with mayavi
from mayavi import mlab
mlab.contour3d(ds.Amplitude.values)
```

## 📈 Performance Characteristics

| Dataset Size | Load Time | Memory Usage | Subset Access |
|--------------|-----------|--------------|---------------|
| 1 GB | ~1 second | ~50 MB | Instant |
| 10 GB | ~2 seconds | ~100 MB | Instant |
| 100 GB | ~5 seconds | ~200 MB | Instant |
| 1 TB | ~10 seconds | ~500 MB | < 1 second |

*Performance scales with metadata complexity, not data size thanks to lazy loading*

## 🌐 Ecosystem Compatibility

### Core Dependencies
- **xarray** ≥2024.7.0 - N-dimensional labeled arrays
- **dask** ≥2024.8.0 - Parallel computing
- **openvds** ≥3.4.6 - VDS file access
- **ovds-utils** ≥0.3.1 - VDS utilities

### Compatible With
- **pandas** - Tabular data analysis
- **matplotlib** - Static plotting
- **hvplot/bokeh** - Interactive visualization
- **scikit-learn** - Machine learning
- **scipy** - Scientific computing
- **zarr** - Cloud-native arrays
- **h5netcdf** - NetCDF files

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](../CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- Testing requirements
- Pull request process

## 📞 Support

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: General questions and community support
- **Documentation**: Comprehensive guides and examples
- **Examples**: Jupyter notebooks with real-world workflows

## 🗺️ Roadmap

### Current (v1.0)
- ✅ Basic VDS reading with xarray integration
- ✅ Chunked, lazy loading with dask
- ✅ Coordinate-aware operations
- ✅ Rich metadata preservation

### Near Term (v1.1-1.2)
- 🚧 Enhanced coordinate systems (UTM, geographic)
- 🚧 Multi-component seismic support
- 🚧 Performance optimizations

---

## 📝 Document Quick Reference

| Document | Best For | Key Topics |
|----------|----------|------------|
| [WHY-XARRAY.md](WHY-XARRAY.md) | Decision makers, newcomers | Benefits, motivation, examples |
| [TECHNICAL-OVERVIEW.md](TECHNICAL-OVERVIEW.md) | Developers, implementers | Architecture, internals, extending |
| [USER-GUIDE.md](USER-GUIDE.md) | Daily users, analysts | Practical examples, workflows |

**New to seismic data science?** Start with [Why Xarray?](WHY-XARRAY.md)

**Ready to start coding?** Jump to [User Guide](USER-GUIDE.md)

**Want to contribute or extend?** Read [Technical Overview](TECHNICAL-OVERVIEW.md)

---

*Built with ❤️ @ Shell for the seismic data science community*
