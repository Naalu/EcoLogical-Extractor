# tests/test_setup.py

import subprocess
from unittest import mock

from src.setup_test import (
    check_external_dependencies,
    check_git_repo,
    check_virtual_env,
)


def test_check_virtual_env():
    # Test when not in virtual environment
    with mock.patch("sys.prefix", "prefix"):
        with mock.patch("sys.base_prefix", "prefix"):
            assert not check_virtual_env()

    # Test when in virtual environment
    with mock.patch("sys.prefix", "prefix"):
        with mock.patch("sys.base_prefix", "different_prefix"):
            assert check_virtual_env()


def test_check_git_repo():
    # Test when .git directory exists
    with mock.patch("pathlib.Path.is_dir", return_value=True):
        assert check_git_repo()

    # Test when .git directory doesn't exist
    with mock.patch("pathlib.Path.is_dir", return_value=False):
        assert not check_git_repo()


def test_check_external_dependencies():
    # Mock shutil.which to return a path for all commands
    with mock.patch("shutil.which", return_value="/usr/bin/tesseract"):
        assert check_external_dependencies()

    # Mock shutil.which to return None for all commands but make subprocess work
    with mock.patch("shutil.which", return_value=None):
        with mock.patch("subprocess.run"):
            assert check_external_dependencies()

    # Mock both methods failing
    with mock.patch("shutil.which", return_value=None):
        with mock.patch("subprocess.run", side_effect=subprocess.SubprocessError):
            assert not check_external_dependencies()
