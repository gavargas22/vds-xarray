# User Guide: Working with VDS Files in Xarray

## Getting Started

### Installation and Setup

```bash
# Install the VDS Xarray Backend
pip install vdsxarray

# For development or latest features
git clone https://github.com/gavargas22/vds-xarray-backend.git
cd vds-xarray-backend
pip install -e .
```

### Your First VDS Dataset

```python
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# Open a VDS file - it's that simple!
ds = xr.open_dataset('path/to/your/seismic.vds', engine='vds')

# Explore your dataset
print(ds)
```

**What you'll see:**
```
<xarray.Dataset>
Dimensions:    (inline: 1401, crossline: 1351, sample: 2741)
Coordinates:
  * inline     (inline) int16 1300 1301 1302 ... 2698 2699 2700
  * crossline  (crossline) int16 2500 2502 2504 ... 5196 5198 5200
  * sample     (sample) float32 0.0 3.048 6.096 ... 8.348e+03 8.352e+03
Data variables:
    Amplitude  (inline, crossline, sample) float32 dask.array<...>
Attributes:
    title:         VDS Seismic Data: Amplitude
    source:        /path/to/original/file.vds
    created_with:  vdsxarray
```

## Basic Operations

### Accessing Data

```python
# Get the main seismic data
amplitude = ds.Amplitude

# Check if data is chunked (it should be!)
print(f"Chunked: {amplitude.chunks is not None}")
print(f"Chunk sizes: {amplitude.chunksizes}")

# Get coordinate information
print(f"Inline range: {ds.inline.min().values} to {ds.inline.max().values}")
print(f"Crossline range: {ds.crossline.min().values} to {ds.crossline.max().values}")
print(f"Sample range: {ds.sample.min().values} to {ds.sample.max().values} ms")
```

### Selecting Data

```python
# Select by coordinate values (not array indices!)
inline_slice = ds.sel(inline=1500)  # Single inline
crossline_slice = ds.sel(crossline=2500)  # Single crossline
time_slice = ds.sel(sample=100, method='nearest')  # Nearest to 100ms

# Select ranges
volume_subset = ds.sel(
    inline=slice(1400, 1600),
    crossline=slice(2400, 2600),
    sample=slice(0, 1000)  # First 1000ms
)

# Select by integer position (if needed)
first_inline = ds.isel(inline=0)
last_sample = ds.isel(sample=-1)
```

## Visualization

### Quick Plotting

```python
# Plot a single inline (seismic section)
ds.Amplitude.sel(inline=1500).plot(
    x='crossline', 
    y='sample',
    cmap='seismic',
    robust=True  # Better color scaling
)
plt.gca().invert_yaxis()  # Time increases downward
plt.title('Inline 1500')
plt.ylabel('Time (ms)')
plt.show()

# Plot a time slice (horizon view)
ds.Amplitude.sel(sample=200, method='nearest').plot(
    x='crossline',
    y='inline', 
    cmap='seismic',
    robust=True
)
plt.title('Time Slice at ~200ms')
plt.show()

# Plot a crossline section
ds.Amplitude.sel(crossline=2500).plot(
    x='inline',
    y='sample',
    cmap='seismic',
    robust=True
)
plt.gca().invert_yaxis()
plt.title('Crossline 2500')
plt.ylabel('Time (ms)')
plt.show()
```

### Advanced Visualization

```python
import matplotlib.pyplot as plt

# Create a multi-panel figure
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Inline section
ds.Amplitude.sel(inline=1500).plot(
    ax=axes[0,0], 
    x='crossline', 
    y='sample',
    cmap='seismic', 
    add_colorbar=False
)
axes[0,0].invert_yaxis()
axes[0,0].set_title('Inline 1500')

# Crossline section  
ds.Amplitude.sel(crossline=2500).plot(
    ax=axes[0,1],
    x='inline',
    y='sample', 
    cmap='seismic',
    add_colorbar=False
)
axes[0,1].invert_yaxis()
axes[0,1].set_title('Crossline 2500')

# Time slice
ds.Amplitude.sel(sample=200, method='nearest').plot(
    ax=axes[1,0],
    x='crossline',
    y='inline',
    cmap='seismic',
    add_colorbar=False
)
axes[1,0].set_title('Time Slice ~200ms')

# RMS amplitude
rms = np.sqrt((ds.Amplitude ** 2).mean('sample'))
rms.plot(
    ax=axes[1,1],
    x='crossline', 
    y='inline',
    cmap='viridis'
)
axes[1,1].set_title('RMS Amplitude')

plt.tight_layout()
plt.show()
```

## Data Analysis

### Statistical Analysis

```python
# Basic statistics
print("Dataset Statistics:")
print(f"Mean amplitude: {ds.Amplitude.mean().values:.3f}")
print(f"RMS amplitude: {np.sqrt((ds.Amplitude ** 2).mean()).values:.3f}")
print(f"Min amplitude: {ds.Amplitude.min().values:.3f}")
print(f"Max amplitude: {ds.Amplitude.max().values:.3f}")

# Statistics along specific dimensions
inline_rms = np.sqrt((ds.Amplitude ** 2).mean(['crossline', 'sample']))
crossline_rms = np.sqrt((ds.Amplitude ** 2).mean(['inline', 'sample']))
time_rms = np.sqrt((ds.Amplitude ** 2).mean(['inline', 'crossline']))

# Plot RMS vs coordinates
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

inline_rms.plot(ax=axes[0])
axes[0].set_title('RMS vs Inline')

crossline_rms.plot(ax=axes[1]) 
axes[1].set_title('RMS vs Crossline')

time_rms.plot(ax=axes[2])
axes[2].set_title('RMS vs Time')
axes[2].set_xlabel('Time (ms)')

plt.tight_layout()
plt.show()
```

### Spectral Analysis

```python
from scipy import signal

# Extract a trace for analysis
trace = ds.Amplitude.sel(inline=1500, crossline=2500).values

# Calculate power spectral density
sample_rate = 1000.0 / (ds.sample[1] - ds.sample[0]).values  # Hz
frequencies, psd = signal.welch(trace, sample_rate, nperseg=256)

# Plot spectrum
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
plt.plot(ds.sample, trace)
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude')
plt.title('Seismic Trace')

plt.subplot(1, 2, 2)
plt.semilogy(frequencies, psd)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectral Density')
plt.title('Frequency Spectrum')
plt.grid(True)

plt.tight_layout()
plt.show()
```

## Working with Large Datasets

### Memory-Efficient Operations

```python
# Load dataset (lazy loading - no data in memory yet)
ds = xr.open_dataset('huge_survey.vds', engine='vds')
print(f"Dataset size: {ds.nbytes / 1e9:.1f} GB")

# Select subset without loading full dataset
subset = ds.sel(
    inline=slice(1000, 1200),
    crossline=slice(2000, 2200)
)
print(f"Subset size: {subset.nbytes / 1e6:.1f} MB")

# Perform computation on subset
result = subset.Amplitude.mean().compute()
print(f"Mean amplitude in subset: {result.values:.3f}")
```

### Chunked Processing

```python
import dask

# Configure dask for your system
dask.config.set({
    'array.chunk-size': '128MB',
    'array.slicing.split_large_chunks': True
})

# Process in chunks automatically
def apply_agc(data, window_samples=100):
    """Apply Automatic Gain Control"""
    # This will process in chunks automatically
    rolling_rms = data.rolling(sample=window_samples, center=True).std()
    agc_data = data / (rolling_rms + 1e-6)  # Avoid division by zero
    return agc_data

# Apply AGC to entire dataset (processes in chunks)
agc_amplitude = apply_agc(ds.Amplitude)

# Compute result for a subset
agc_subset = agc_amplitude.sel(inline=slice(1400, 1600))
agc_result = agc_subset.compute()
```

### Progress Monitoring

```python
from dask.diagnostics import ProgressBar

# Monitor progress of computations
with ProgressBar():
    # Compute RMS for entire dataset
    rms_map = np.sqrt((ds.Amplitude ** 2).mean('sample')).compute()
    
    # Save result
    rms_map.to_netcdf('rms_amplitude_map.nc')
```

## Data Export and Conversion

### Export to Different Formats

```python
# Export subset to NetCDF
subset = ds.sel(inline=slice(1400, 1600), crossline=slice(2400, 2600))
subset.to_netcdf('seismic_subset.nc')

# Export to Zarr (for cloud storage)
subset.to_zarr('seismic_subset.zarr')

# Export to CSV (for small datasets)
trace = ds.Amplitude.sel(inline=1500, crossline=2500)
trace_df = trace.to_dataframe()
trace_df.to_csv('trace_1500_2500.csv')
```

### Integration with Other Tools

```python
# Convert to numpy for custom processing
subset_array = subset.Amplitude.values

# Convert to pandas DataFrame
df = ds.Amplitude.sel(sample=slice(0, 500)).to_dataframe()

# Save processed data back as xarray
processed_amplitude = apply_custom_processing(ds.Amplitude)
processed_ds = ds.copy()
processed_ds['Amplitude'] = processed_amplitude
processed_ds.to_netcdf('processed_seismic.nc')
```

## Advanced Workflows

### Time-Lapse Analysis

```python
# Load multiple surveys
surveys = []
years = [2018, 2020, 2022]

for year in years:
    ds = xr.open_dataset(f'survey_{year}.vds', engine='vds')
    ds = ds.expand_dims('time')
    ds = ds.assign_coords(time=[year])
    surveys.append(ds)

# Combine into 4D dataset
time_lapse = xr.concat(surveys, dim='time')

# Calculate differences
baseline = time_lapse.sel(time=2018)
monitor_2020 = time_lapse.sel(time=2020)
monitor_2022 = time_lapse.sel(time=2022)

diff_2020 = monitor_2020 - baseline
diff_2022 = monitor_2022 - baseline

# Visualize changes
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

diff_2020.Amplitude.sel(sample=200, method='nearest').plot(
    ax=axes[0], x='crossline', y='inline', cmap='RdBu_r'
)
axes[0].set_title('Amplitude Change 2018-2020')

diff_2022.Amplitude.sel(sample=200, method='nearest').plot(
    ax=axes[1], x='crossline', y='inline', cmap='RdBu_r'
)
axes[1].set_title('Amplitude Change 2018-2022')

plt.tight_layout()
plt.show()
```

### Attribute Analysis

```python
# Calculate seismic attributes
def calculate_attributes(amplitude_data):
    """Calculate common seismic attributes"""
    
    # Instantaneous amplitude (envelope)
    analytic_signal = signal.hilbert(amplitude_data, axis=-1)
    inst_amplitude = np.abs(analytic_signal)
    
    # Instantaneous phase
    inst_phase = np.angle(analytic_signal)
    
    # Instantaneous frequency
    inst_freq = np.diff(np.unwrap(inst_phase, axis=-1), axis=-1)
    
    return inst_amplitude, inst_phase, inst_freq

# Apply to a subset
subset = ds.sel(inline=slice(1400, 1600), crossline=slice(2400, 2600))
amplitude_array = subset.Amplitude.values

inst_amp, inst_phase, inst_freq = calculate_attributes(amplitude_array)

# Create new dataset with attributes
attrs_ds = subset.copy()
attrs_ds['InstantaneousAmplitude'] = (['inline', 'crossline', 'sample'], inst_amp)
attrs_ds['InstantaneousPhase'] = (['inline', 'crossline', 'sample'], inst_phase)

# Visualize attributes
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Original amplitude
subset.Amplitude.sel(inline=1500).plot(
    ax=axes[0,0], x='crossline', y='sample', cmap='seismic'
)
axes[0,0].invert_yaxis()
axes[0,0].set_title('Original Amplitude')

# Instantaneous amplitude
attrs_ds.InstantaneousAmplitude.sel(inline=1500).plot(
    ax=axes[0,1], x='crossline', y='sample', cmap='viridis'
)
axes[0,1].invert_yaxis()
axes[0,1].set_title('Instantaneous Amplitude')

# Instantaneous phase
attrs_ds.InstantaneousPhase.sel(inline=1500).plot(
    ax=axes[1,0], x='crossline', y='sample', cmap='hsv'
)
axes[1,0].invert_yaxis()
axes[1,0].set_title('Instantaneous Phase')

# Time slice of instantaneous amplitude
attrs_ds.InstantaneousAmplitude.sel(sample=200, method='nearest').plot(
    ax=axes[1,1], x='crossline', y='inline', cmap='viridis'
)
axes[1,1].set_title('Inst. Amplitude at ~200ms')

plt.tight_layout()
plt.show()
```

## Performance Tips

### Optimizing Data Access

```python
# Good: Select contiguous regions
good_subset = ds.sel(
    inline=slice(1000, 2000),      # Contiguous range
    crossline=slice(2000, 3000),   # Contiguous range
    sample=slice(0, 1000)          # Contiguous range
)

# Avoid: Non-contiguous selections (slower)
# scattered_inlines = ds.sel(inline=[1000, 1500, 2000])  # Non-contiguous

# Good: Coordinate-based selection
time_slice = ds.sel(sample=100, method='nearest')

# Less efficient: Index-based selection
# time_slice = ds.isel(sample=50)  # Need to know the index
```

### Memory Management

```python
# Monitor memory usage
import psutil

def print_memory_usage():
    memory = psutil.virtual_memory()
    print(f"Memory usage: {memory.percent}% ({memory.used / 1e9:.1f} GB / {memory.total / 1e9:.1f} GB)")

print_memory_usage()

# Process data in smaller chunks if memory is limited
chunk_size = 200  # Process 200 inlines at a time

results = []
for start_inline in range(ds.sizes['inline'])[::chunk_size]:
    end_inline = min(start_inline + chunk_size, ds.sizes['inline'])
    
    chunk = ds.isel(inline=slice(start_inline, end_inline))
    result = process_chunk(chunk)  # Your processing function
    results.append(result)
    
    print_memory_usage()

# Combine results
final_result = xr.concat(results, dim='inline')
```

## Troubleshooting

### Common Issues and Solutions

```python
# Issue: "File not found" error
try:
    ds = xr.open_dataset('seismic.vds', engine='vds')
except FileNotFoundError:
    print("Check file path and permissions")

# Issue: Memory errors with large datasets
try:
    result = ds.Amplitude.mean().compute()
except MemoryError:
    # Solution: Process in smaller chunks
    result = ds.Amplitude.chunk({'inline': 100}).mean().compute()

# Issue: Slow performance
# Solution: Check chunk sizes
print(f"Current chunks: {ds.chunks}")
# Rechunk if necessary
rechunked = ds.chunk({'inline': 128, 'crossline': 128, 'sample': 128})

# Issue: Coordinate misalignment
# Solution: Use .sel() with method='nearest' for approximate matching
value = ds.sel(sample=100.5, method='nearest')  # Finds closest sample
```

This user guide provides practical examples for working with VDS files in the xarray ecosystem, from basic operations to advanced seismic analysis workflows.
