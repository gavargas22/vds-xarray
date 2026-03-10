import numpy as np
import xarray as xr
from ovds_utils.vds import VDS, Formats
from xarray.backends import BackendArray, BackendEntrypoint
from xarray.core import indexing


def get_annotated_coordinates(vds: VDS):
    """
    Extract coordinate arrays from a VDS object.

    This function generates coordinate arrays for inline, crossline, and sample
    dimensions based on the VDS axes properties and shape information.

    Parameters
    ----------
    vds : VDS
        A VDS object containing axes information with coordinate_min, coordinate_max
        properties and shape information for each dimension.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray]
        A tuple containing three numpy arrays:
        - samples : np.ndarray of float32
            Sample coordinates array (axis 0 - usually time/depth)
        - xlines : np.ndarray of int16
            Crossline coordinates array (axis 1)
        - ilines : np.ndarray of int16
            Inline coordinates array (axis 2)

    Notes
    -----
    The function assumes a 3D seismic volume with:
    - Sample coordinates correspond to vds.axes[0] (time/depth)
    - Crossline coordinates correspond to vds.axes[1]
    - Inline coordinates correspond to vds.axes[2]
    """
    inlines = np.linspace(
        start=vds.axes[0].coordinate_min,
        stop=vds.axes[0].coordinate_max,
        num=vds.shape[0],
        dtype=np.int16,
    )

    xlines = np.linspace(
        start=vds.axes[1].coordinate_min,
        stop=vds.axes[1].coordinate_max,
        num=vds.shape[1],
        dtype=np.int16,
    )

    samples = np.linspace(
        start=vds.axes[2].coordinate_min,
        stop=vds.axes[2].coordinate_max,
        num=vds.shape[2],
        dtype=np.float32,
    )

    return inlines, xlines, samples


def get_cdp_coordinates(vds: VDS):
    pass


class VdsBackendArray(BackendArray):
    def __init__(
        self,
        vds_reader: VDS,
        dtype,
    ):
        self.vds_reader = vds_reader
        self.shape = vds_reader.shape
        self.dtype = np.dtype("float32")

    def __getitem__(
        self,
        key: indexing.ExplicitIndexer,
    ) -> np.typing.ArrayLike:
        return indexing.explicit_indexing_adapter(
            key,
            self.shape,
            indexing.IndexingSupport.VECTORIZED,
            self._raw_indexing_method,
        )

    def _raw_indexing_method(self, key: tuple) -> np.typing.ArrayLike:
        def get_min_max(idx, dim_size):
            if isinstance(idx, slice):
                min_idx = 0 if idx.start is None else idx.start
                max_idx = dim_size if idx.stop is None else idx.stop
            elif isinstance(idx, np.ndarray) and idx.ndim == 1:
                min_idx = idx[0]
                max_idx = idx[-1] + 1
            else:
                min_idx = idx
                max_idx = idx + 1
            return np.amin(min_idx), np.amax(max_idx)

        min_ilines, max_ilines = get_min_max(key[0], self.vds_reader.shape[0])
        min_xlines, max_xlines = get_min_max(key[1], self.vds_reader.shape[1])
        min_samples, max_samples = get_min_max(key[2], self.vds_reader.shape[2])

        data = self.vds_reader[
            min_ilines:max_ilines,
            min_xlines:max_xlines,
            min_samples:max_samples,
        ]

        # Check if any of the data has any dimension of size 1 and remove it to make a 2d array
        data = data.squeeze()
        return data


class VdsEngine(BackendEntrypoint):
    def open_dataset(
        self,
        filename_or_obj,
        *,
        drop_variables=None,
        volume_format: str = "float32",
        name: str = "Amplitude",
        channels=None,
        LOD=0,
        calculate_cdp: bool = False,
    ):
        """
        Open a VDS dataset as an xarray Dataset.

        Parameters
        ----------
        filename_or_obj : str or Path
            Path to the VDS file
        drop_variables : list, optional
            Variables to drop (not used for VDS)
        volume_format : str, default "float32"
            Data format to use
        name : str, default "Amplitude"
            Name for the data variable
        channels : list, optional
            Specific channels to read
        LOD : int, default 0
            Level of detail
        calculate_cdp : bool, default False
            Whether to calculate CDP coordinates

        Returns
        -------
        xarray.Dataset
            Dataset containing the VDS data
        """

        # Open up the VDS volume
        try:
            vds = VDS(path=str(filename_or_obj))
        except Exception as e:
            raise ValueError(f"Failed to open VDS file {filename_or_obj}: {e}")

        # Get annotated coordinate axis
        coords = get_annotated_coordinates(vds=vds)
        dims = ("inline", "crossline", "sample")

        # Using ovds-utils open up the VDS file
        backend_array = VdsBackendArray(vds_reader=vds, dtype=Formats.R32)
        # Set the format
        vds.channel(0).format = Formats.R32

        data = indexing.LazilyIndexedArray(backend_array)

        # Create attributes
        attrs = {
            "source_file": str(filename_or_obj),
            "shape": vds.shape,
            "coordinate_ranges": {
                "inline": [int(coords[0].min()), int(coords[0].max())],
                "crossline": [int(coords[1].min()), int(coords[1].max())],
                "sample": [int(coords[2].min()), int(coords[2].max())],
            },
        }

        seismic_data = xr.DataArray(
            data=data, coords=coords, dims=dims, name=name, attrs=attrs
        )

        # Set an encoding with reasonable chunk sizes
        # from .utils import estimate_chunk_size
        # chunk_sizes = estimate_chunk_size(vds.shape)

        # encoding = {
        #     "preferred_chunks": chunk_sizes
        # }
        # seismic_data.encoding = encoding

        ds = xr.Dataset({f"{seismic_data.name}": seismic_data})
        ds.attrs = {
            "title": f"VDS Seismic Data: {name}",
            "source": str(filename_or_obj),
            "created_with": "vdsxarray",
        }

        # Clean up VDS resources
        try:
            vds.accessor.commit()
            vds.accessor.removeReference()
        except Exception:
            pass  # Some VDS versions may not have these methods
        chunked_ds = ds.chunk({"inline": 128, "crossline": 128, "sample": 128})
        return chunked_ds

    def guess_can_open(self, filename_or_obj):
        """
        Determine if this backend can open the given file or object.

        This method checks whether the VDS backend can handle the provided
        filename or file object by examining the file extension.

        Parameters
        ----------
        filename_or_obj : str or file-like object
            The filename (as a string) or file-like object to check.

        Returns
        -------
        bool
            True if the file appears to be openable by this VDS backend
            (specifically if it's a string ending with '.vds'), False otherwise.

        Notes
        -----
        This is a heuristic check based on file extension only and does not
        verify the actual file format or contents.
        """
        # Implement logic to guess if the file can be opened by this engine
        if isinstance(filename_or_obj, str) and filename_or_obj.endswith(".vds"):
            return True
        return False
