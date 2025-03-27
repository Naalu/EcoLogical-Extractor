"""
Utility module for gracefully handling external dependencies.
"""

import importlib.util
import logging
import os
import shutil
import subprocess
from typing import List, Optional, TypedDict


# Define TypedDict classes for more precise return type information
class DependencyInfo(TypedDict):
    available: bool
    path: Optional[str]
    version: Optional[str]


logger: logging.Logger = logging.getLogger(__name__)


class DependencyManager:
    """
    Manages external dependencies and provides fallbacks when they're not available.
    """

    @staticmethod
    def check_tesseract() -> DependencyInfo:
        """
        Check if Tesseract OCR is installed and available.

        Returns:
            Dict containing:
                - available (bool): Whether Tesseract is available
                - path (str): Path to Tesseract executable if found
                - version (str): Version string if available
        """
        result: DependencyInfo = {"available": False, "path": None, "version": None}

        # First check if pytesseract is installed
        if importlib.util.find_spec("pytesseract") is None:
            logger.warning("pytesseract package not installed")
            return result

        # Check for tesseract in PATH
        tesseract_path: Optional[str] = shutil.which("tesseract")

        # On Windows, also check common installation directories
        if not tesseract_path and os.name == "nt":
            common_paths: List[str] = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            ]
            for path in common_paths:
                if os.path.exists(path):
                    tesseract_path = path
                    break

        if tesseract_path:
            result["available"] = True
            result["path"] = tesseract_path

            # Get version
            try:
                version_output = subprocess.run(
                    [tesseract_path, "--version"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if version_output.returncode == 0:
                    # Extract version from output
                    version_line = version_output.stdout.split("\n")[0]
                    result["version"] = version_line.strip()
            except Exception as e:
                logger.error(f"Failed to get Tesseract version: {e}")

        return result

    @staticmethod
    def check_ffmpeg() -> DependencyInfo:
        """
        Check if ffmpeg is installed and available.

        Returns:
            Dict containing:
                - available (bool): Whether ffmpeg is available
                - path (str): Path to ffmpeg executable if found
                - version (str): Version string if available
        """
        result: DependencyInfo = {"available": False, "path": None, "version": None}

        # Check for ffmpeg in PATH
        ffmpeg_path: Optional[str] = shutil.which("ffmpeg")

        if ffmpeg_path:
            result["available"] = True
            result["path"] = ffmpeg_path

            # Get version
            try:
                version_output = subprocess.run(
                    [ffmpeg_path, "-version"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if version_output.returncode == 0:
                    # Extract version from output
                    version_line = version_output.stdout.split("\n")[0]
                    result["version"] = version_line.strip()
            except Exception as e:
                logger.error(f"Failed to get ffmpeg version: {e}")

        return result

    @staticmethod
    def check_ghostscript() -> DependencyInfo:
        """
        Check if Ghostscript is installed and available.

        Returns:
            Dict containing:
                - available (bool): Whether Ghostscript is available
                - path (str): Path to Ghostscript executable if found
                - version (str): Version string if available
        """
        result: DependencyInfo = {"available": False, "path": None, "version": None}

        # Check for different executables based on platform
        if os.name == "nt":  # Windows
            gs_execs = ["gswin64c", "gswin32c"]
        else:  # Unix-like
            gs_execs = ["gs"]

        for exec_name in gs_execs:
            gs_path: Optional[str] = shutil.which(exec_name)
            if gs_path:
                result["available"] = True
                result["path"] = gs_path

                # Get version
                try:
                    version_output = subprocess.run(
                        [gs_path, "--version"],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    if version_output.returncode == 0:
                        result["version"] = version_output.stdout.strip()
                except Exception as e:
                    logger.error(f"Failed to get Ghostscript version: {e}")

                # We found a valid executable, so break
                break

        return result

    @staticmethod
    def configure_pytesseract() -> None:
        """Configure pytesseract with the correct path if available."""
        tesseract_info = DependencyManager.check_tesseract()
        if tesseract_info["available"] and tesseract_info["path"]:
            try:
                import pytesseract  # type: ignore

                pytesseract.pytesseract.tesseract_cmd = tesseract_info["path"]
                logger.info(
                    f"Configured pytesseract with Tesseract path: {tesseract_info['path']}"
                )
            except ImportError:
                logger.warning("pytesseract package not available")


# Initialize logging for this module
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
