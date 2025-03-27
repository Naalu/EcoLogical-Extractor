# tests/test_setup_env.py

import subprocess
from unittest import mock

from setup_env import check_python_version, create_data_directories, run_command


def test_create_data_directories():
    # Mock mkdir to avoid actually creating directories
    with mock.patch("pathlib.Path.mkdir") as mock_mkdir:
        assert create_data_directories()
        # Verify mkdir was called with expected arguments
        assert mock_mkdir.call_count > 0
        assert all(call.kwargs.get("parents") for call in mock_mkdir.call_args_list)
        assert all(call.kwargs.get("exist_ok") for call in mock_mkdir.call_args_list)


def test_check_python_version():
    # Test with Python 3.12
    with mock.patch("sys.version_info", (3, 12)):
        assert check_python_version()

    # Test with Python 3.8 (should fail)
    with mock.patch("sys.version_info", (3, 8)):
        assert not check_python_version()


def test_run_command():
    # Test successful command
    with mock.patch("subprocess.run") as mock_run:
        mock_run.return_value = mock.Mock(returncode=0)
        result = run_command(["echo", "test"])
        assert result is not None

    # Test failed command
    with mock.patch(
        "subprocess.run", side_effect=subprocess.CalledProcessError(1, "cmd")
    ) as mock_run:
        result = run_command(["invalid", "command"])
        assert result is None
