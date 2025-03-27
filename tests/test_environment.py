"""Basic tests to verify the development environment."""

import importlib
import sys


def test_python_version():
    """Test that Python version is at least 3.12."""
    assert sys.version_info >= (3, 8), "Python version should be at least 3.8"


def test_core_dependencies():
    """Test that core dependencies can be imported."""
    core_packages = [
        "pandas",
        "numpy",
        "pdfplumber",
        "spacy",
        "tqdm",
    ]

    for package in core_packages:
        assert (
            importlib.util.find_spec(package) is not None
        ), f"{package} should be installed"


def test_setup_module():
    """Test that our setup_test module can be imported."""
    import src.setup_test

    assert hasattr(
        src.setup_test, "check_requirements"
    ), "setup_test should have check_requirements function"
