"""Tests for the dependency management module."""

from unittest.mock import MagicMock, patch

import pytest

from src.utils.dependencies import DependencyManager


@pytest.fixture
def mock_which():
    """Fixture to mock shutil.which."""
    with patch("shutil.which") as mock:
        yield mock


@pytest.fixture
def mock_subprocess():
    """Fixture to mock subprocess.run."""
    with patch("subprocess.run") as mock:
        # Set up the mock to return a successful response
        process_mock = MagicMock()
        process_mock.returncode = 0
        process_mock.stdout = "Mock version 1.0"
        mock.return_value = process_mock
        yield mock


def test_check_tesseract_not_found(mock_which):
    """Test checking for Tesseract when it's not found."""
    mock_which.return_value = None

    # Mock importlib.util.find_spec to return non-None for pytesseract
    with patch("importlib.util.find_spec", return_value=True):
        result = DependencyManager.check_tesseract()

    assert result["available"] is False
    assert result["path"] is None
    assert result["version"] is None


def test_check_tesseract_found(mock_which, mock_subprocess):
    """Test checking for Tesseract when it's found."""
    mock_which.return_value = "/usr/bin/tesseract"

    # Mock importlib.util.find_spec to return non-None for pytesseract
    with patch("importlib.util.find_spec", return_value=True):
        result = DependencyManager.check_tesseract()

    assert result["available"] is True
    assert result["path"] == "/usr/bin/tesseract"
    assert result["version"] == "Mock version 1.0"


def test_check_ffmpeg(mock_which, mock_subprocess):
    """Test checking for ffmpeg."""
    mock_which.return_value = "/usr/bin/ffmpeg"

    result = DependencyManager.check_ffmpeg()

    assert result["available"] is True
    assert result["path"] == "/usr/bin/ffmpeg"
    assert result["version"] == "Mock version 1.0"


def test_check_ghostscript(mock_which, mock_subprocess):
    """Test checking for Ghostscript."""
    mock_which.return_value = "/usr/bin/gs"

    result = DependencyManager.check_ghostscript()

    assert result["available"] is True
    assert result["path"] == "/usr/bin/gs"
    assert result["version"] == "Mock version 1.0"
