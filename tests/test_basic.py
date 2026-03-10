"""
Basic tests for vdsxarray package.
"""

import vdsxarray


def test_version():
    """Test that version is defined."""
    assert hasattr(vdsxarray, '__version__')
    assert isinstance(vdsxarray.__version__, str)


def test_engine_import():
    """Test that VdsEngine can be imported."""
    from vdsxarray import VdsEngine
    assert VdsEngine is not None


def test_engine_attributes():
    """Test that VdsEngine has required attributes."""
    from vdsxarray import VdsEngine
    
    # Check if it has the required methods for an xarray backend
    assert hasattr(VdsEngine, 'open_dataset')
    assert callable(VdsEngine.open_dataset)


def test_package_structure():
    """Test basic package structure."""
    import vdsxarray
    
    # Check __all__ is defined
    assert hasattr(vdsxarray, '__all__')
    assert 'VdsEngine' in vdsxarray.__all__
