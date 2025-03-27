"""Utility script for checking external dependencies."""

import logging
import platform
import shutil
import subprocess
from typing import Dict

logger = logging.getLogger(__name__)


# Platform detection
def get_platform() -> str:
    """Determine the current platform."""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    return system


# External dependency definitions
EXTERNAL_DEPENDENCIES = {
    "tesseract": {
        "name": "Tesseract OCR",
        "check_cmd": "tesseract --version",
        "executable": "tesseract",
        "required_for": "OCR processing",
        "install_instructions": {
            "macos": "brew install tesseract",
            "linux": "sudo apt-get install -y tesseract-ocr",
            "windows": "Download from https://github.com/UB-Mannheim/tesseract/wiki",
        },
        "env_vars": {},
        "packages": ["pytesseract", "opencv-python"],
    },
    "ffmpeg": {
        "name": "FFmpeg",
        "check_cmd": "ffmpeg -version",
        "executable": "ffmpeg",
        "required_for": "Audio transcription",
        "install_instructions": {
            "macos": "brew install ffmpeg",
            "linux": "sudo apt-get install -y ffmpeg",
            "windows": "Download from https://ffmpeg.org/download.html",
        },
        "env_vars": {},
        "packages": ["openai-whisper"],
    },
    "gs": {
        "name": "Ghostscript",
        "check_cmd": "gs --version",
        "executable": "gs",
        "required_for": "PDF table extraction",
        "install_instructions": {
            "macos": "brew install ghostscript",
            "linux": "sudo apt-get install -y ghostscript",
            "windows": "Download from https://www.ghostscript.com/download.html",
        },
        "env_vars": {},
        "packages": ["camelot-py"],
    },
    "llvm-config": {
        "name": "LLVM",
        "check_cmd": "llvm-config --version",
        "executable": "llvm-config",
        "required_for": "Audio transcription (Numba dependency)",
        "install_instructions": {
            "macos": (
                "brew install llvm\n"
                'export PATH="/opt/homebrew/opt/llvm/bin:$PATH"\n'
                'export LLVM_CONFIG="/opt/homebrew/opt/llvm/bin/llvm-config"\n'
                'export LDFLAGS="-L/opt/homebrew/opt/llvm/lib"\n'
                'export CPPFLAGS="-I/opt/homebrew/opt/llvm/include"'
            ),
            "linux": "sudo apt-get install -y llvm",
            "windows": "Download from https://github.com/llvm/llvm-project/releases",
        },
        "env_vars": {
            "macos": {
                "PATH": "/opt/homebrew/opt/llvm/bin:$PATH",
                "LLVM_CONFIG": "/opt/homebrew/opt/llvm/bin/llvm-config",
                "LDFLAGS": "-L/opt/homebrew/opt/llvm/lib",
                "CPPFLAGS": "-I/opt/homebrew/opt/llvm/include",
            }
        },
        "packages": ["openai-whisper"],
    },
}


def check_dependency(dependency_key: str, print_instructions: bool = True) -> bool:
    """
    Check if an external dependency is installed.

    Args:
        dependency_key: Key of the dependency to check
        print_instructions: Whether to print installation instructions

    Returns:
        bool: True if the dependency is installed, False otherwise
    """
    if dependency_key not in EXTERNAL_DEPENDENCIES:
        logger.error(f"Unknown dependency: {dependency_key}")
        return False

    dep_info = EXTERNAL_DEPENDENCIES[dependency_key]

    # Check if executable exists in PATH
    if shutil.which(str(dep_info["executable"])):
        return True

    # Try running the check command
    try:
        subprocess.run(
            str(dep_info["check_cmd"]).split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return True

    except (subprocess.SubprocessError, FileNotFoundError):
        if print_instructions:
            platform_name = get_platform()
            platform_instructions = dep_info["install_instructions"]
            if isinstance(platform_instructions, dict):
                instructions = platform_instructions.get(
                    platform_name,
                    platform_instructions.get(
                        "linux", "Installation instructions not available"
                    ),
                )
            else:
                instructions = platform_instructions

            print(
                f"\n{dep_info['name']} is required for {dep_info['required_for']} but not found."
            )
            print(f"To install on {platform_name.capitalize()}:")
            print(f"  {instructions}")

            # Print environment variables if needed
            env_vars = dep_info.get("env_vars", {})
            env_vars = (
                env_vars.get(platform_name, {}) if isinstance(env_vars, dict) else {}
            )
            if env_vars:
                print("\nAfter installation, set these environment variables:")
                for var, value in env_vars.items():
                    print(f'  export {var}="{value}"')

        return False


def check_all_dependencies(print_instructions: bool = True) -> Dict[str, bool]:
    """
    Check all external dependencies.

    Args:
        print_instructions: Whether to print installation instructions

    Returns:
        Dict mapping dependency keys to their status (True if installed)
    """
    results = {}
    for dep_key in EXTERNAL_DEPENDENCIES:
        results[dep_key] = check_dependency(dep_key, print_instructions)
    return results


def get_env_var_instructions() -> str:
    """Get environment variable setup instructions for the current platform."""
    platform_name = get_platform()
    instructions = []

    for dep_key, dep_info in EXTERNAL_DEPENDENCIES.items():
        env_vars = dep_info.get("env_vars", {})
        if isinstance(env_vars, dict):
            platform_vars = env_vars.get(platform_name, {})
            if platform_vars:
                for var, value in platform_vars.items():
                    instructions.append(f'export {var}="{value}"')

    return "\n".join(instructions)


if __name__ == "__main__":
    """Run dependency checks when script is executed directly."""
    logging.basicConfig(level=logging.INFO)
    results = check_all_dependencies()

    # Print summary
    installed = [k for k, v in results.items() if v]
    missing = [k for k, v in results.items() if not v]

    print(f"\nInstalled dependencies: {len(installed)}/{len(results)}")
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print("\nSee docs/DEPENDENCIES.md for detailed installation instructions.")
    else:
        print("All external dependencies are installed!")
