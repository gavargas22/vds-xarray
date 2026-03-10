"""
Utility functions for VDS xarray backend.
"""

import numpy as np
from ovds_utils.vds import VDS


def get_vds_metadata(vds: VDS) -> dict:
    """Extract metadata from VDS object."""
    metadata = {
        'shape': vds.shape,
        'axes_info': [],
        'data_type': str(vds.format) if hasattr(vds, 'format') else 'unknown'
    }
    
    for i, axis in enumerate(vds.axes):
        axis_info = {
            'axis': i,
            'coordinate_min': axis.coordinate_min,
            'coordinate_max': axis.coordinate_max,
            'size': vds.shape[i]
        }
        metadata['axes_info'].append(axis_info)
    
    return metadata


def estimate_chunk_size(shape: tuple, target_mb: int = 64) -> dict:
    """
    Estimate optimal chunk sizes for dask arrays.
    
    Parameters
    ----------
    shape : tuple
        Shape of the array
    target_mb : int
        Target chunk size in megabytes
        
    Returns
    -------
    dict
        Dictionary with chunk sizes for each dimension
    """
    # Assume float32 (4 bytes per element)
    bytes_per_element = 4
    target_bytes = target_mb * 1024 * 1024
    total_elements = np.prod(shape)
    
    if total_elements * bytes_per_element <= target_bytes:
        # Data is small enough to load entirely
        return {
            'sample': shape[0],
            'crossline': shape[1], 
            'inline': shape[2]
        }
    
    # Calculate chunk sizes to approximate target
    chunk_elements = target_bytes // bytes_per_element
    
    # Try to make roughly cubic chunks
    chunk_size = int(chunk_elements ** (1/3))
    
    return {
        'sample': min(chunk_size, shape[0]),
        'crossline': min(chunk_size, shape[1]),
        'inline': min(chunk_size, shape[2])
    }