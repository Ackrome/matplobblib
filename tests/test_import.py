import pytest

def test_package_import():
    """Tests that the main package can be imported."""
    try:
        import matplobblib
    except ImportError as e:
        pytest.fail(f"Failed to import the main matplobblib package: {e}")

def test_submodule_imports():
    """Tests that all major submodules can be imported."""
    submodules = ['aisd', 'ml', 'nm', 'tvims']
    for module in submodules:
        try:
            # Dynamically import submodule from matplobblib
            __import__(f"matplobblib.{module}")
        except ImportError as e:
            pytest.fail(f"Failed to import submodule matplobblib.{module}: {e}")
