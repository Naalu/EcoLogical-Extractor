import importlib.metadata
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict


def check_virtual_env() -> bool:
    """Check if running in a virtual environment.

    Returns:
        bool: True if a virtual environment is activated, False otherwise.
    """
    if sys.prefix == sys.base_prefix:
        print("❌ Virtual environment is not activated")
        print("   Please activate your virtual environment and try again")
        # Provide a hint on how to activate the virtual environment
        activation_tips = {
            "mac": "source venv/bin/activate",
            "nt": r"venv\Scripts\activate",
            "posix": "source venv/bin/activate",
        }
        tip = activation_tips.get(
            os.name, "Activate your virtual environment using the appropriate command"
        )
        print(f"   Tip: Run '{tip}'")
        return False
    print("✅ Virtual environment is activated")
    return True


def check_requirements(debug: bool = False) -> bool:
    """Check if all required packages are installed.

    Args:
        debug (bool): If True, print debug information.

    Returns:
        bool: True if all required packages are installed, False otherwise.
    """
    requirements_file = Path("requirements.txt")

    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        print("   Please ensure you're in the correct directory")
        return False

    # Read requirements file
    with open(requirements_file) as f:
        requirements = [
            line.strip() for line in f if line.strip() and not line.startswith("#")
        ]

    # Get all installed distributions and their metadata
    installed_packages = {}
    if debug:
        print("\nDebug: Full package list:")
    for dist in importlib.metadata.distributions():
        try:
            name = dist.metadata["Name"]
            version = dist.version
            normalized_name = name.lower().replace("-", ".").replace("_", ".")
            installed_packages[normalized_name] = version
            if debug:
                print(
                    f"  Original name: {name}, Normalized: {normalized_name}, Version: {version}"
                )
        except Exception as e:
            if debug:
                print(f"Warning: Error processing package {dist}: {e}")

    if debug:
        print(f"\nTotal packages found: {len(installed_packages)}")

    missing = []
    for requirement in requirements:
        package = (
            requirement.split("==")[0]
            .split(">=")[0]
            .split("<=")[0]
            .split(">")[0]
            .split("<")[0]
            .strip()
        )
        normalized_package = package.lower().replace("-", ".").replace("_", ".")
        if debug:
            print(f"\nDebug: Checking requirement: {package}")
            print(f"  Normalized name: {normalized_package}")
            print(
                f"  Found in installed packages: {normalized_package in installed_packages}"
            )
        if normalized_package not in installed_packages:
            missing.append(package)

    if missing:
        print("❌ Some required packages are missing:")
        for package in missing:
            print(f"   - {package}")
        print("\nPlease install missing packages using:")
        print("   pip install -r requirements.txt")
        return False

    print("✅ All required packages are installed")
    return True


def check_git_repo() -> bool:
    """Check if the current directory is a git repository.

    Returns:
        bool: True if the current directory is a git repository, False otherwise.
    """
    git_dir = Path(".git")
    if not git_dir.is_dir():
        print("❌ Not in a git repository")
        print(
            "   Please ensure you've cloned the project and are in the correct directory"
        )
        return False
    print("✅ Git repository found")
    return True


def check_external_dependencies() -> Dict[str, bool]:
    """Check if recommended external dependencies are installed.

    These checks are informational and won't cause the setup test to fail,
    but they indicate which tools will be needed for specific features.

    Returns:
        Dict[str, bool]: Dictionary of dependency names and whether they're installed.
    """
    print("\nChecking external dependencies (informational):")

    results = {}

    # Check for Tesseract OCR (needed for OCR processing)
    try:
        result = subprocess.run(
            ["tesseract", "--version"], capture_output=True, text=True, check=False
        )
        if result.returncode == 0:
            print("✅ Tesseract OCR is installed")
            results["tesseract"] = True
        else:
            print("ℹ️ Tesseract OCR not found (needed for OCR processing)")
            _print_install_instructions("tesseract")
            results["tesseract"] = False
    except (FileNotFoundError, subprocess.SubprocessError):
        print("ℹ️ Tesseract OCR not found (needed for OCR processing)")
        _print_install_instructions("tesseract")
        results["tesseract"] = False

    # Check for ffmpeg (needed for audio transcription)
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"], capture_output=True, text=True, check=False
        )
        if result.returncode == 0:
            print("✅ ffmpeg is installed")
            results["ffmpeg"] = True
        else:
            print("ℹ️ ffmpeg not found (needed for audio transcription)")
            _print_install_instructions("ffmpeg")
            results["ffmpeg"] = False
    except (FileNotFoundError, subprocess.SubprocessError):
        print("ℹ️ ffmpeg not found (needed for audio transcription)")
        _print_install_instructions("ffmpeg")
        results["ffmpeg"] = False

    # Check for Ghostscript (needed for table extraction on Windows)
    if os.name == "nt":  # Windows check
        try:
            # Try to find gswin64c.exe or gswin32c.exe in PATH
            gs_path = shutil.which("gswin64c") or shutil.which("gswin32c")
            if gs_path:
                print("✅ Ghostscript is installed")
                results["ghostscript"] = True
            else:
                print(
                    "ℹ️ Ghostscript not found (needed for table extraction on Windows)"
                )
                _print_install_instructions("ghostscript")
                results["ghostscript"] = False
        except Exception:
            print("ℹ️ Ghostscript not found (needed for table extraction on Windows)")
            _print_install_instructions("ghostscript")
            results["ghostscript"] = False

    return results


def _print_install_instructions(dependency: str) -> None:
    """Print installation instructions for a specific dependency.

    Args:
        dependency (str): Name of the dependency to show instructions for.
    """
    if dependency == "tesseract":
        if os.name == "nt":  # Windows
            print("   To install Tesseract OCR on Windows:")
            print("   1. Download from https://github.com/UB-Mannheim/tesseract/wiki")
            print(
                '   2. Add to PATH: setx PATH "%PATH%;C:\\Program Files\\Tesseract-OCR"'
            )
            print("   3. Verify with: tesseract --version")
        elif os.name == "posix":  # Linux/macOS
            if sys.platform == "darwin":  # macOS
                print("   To install Tesseract OCR on macOS:")
                print("   1. Run: brew install tesseract")
                print("   2. Verify with: tesseract --version")
            else:  # Linux
                print("   To install Tesseract OCR on Linux:")
                print(
                    "   1. Run: sudo apt-get update && sudo apt-get install -y tesseract-ocr"
                )
                print("   2. Verify with: tesseract --version")

    elif dependency == "ffmpeg":
        if os.name == "nt":  # Windows
            print("   To install ffmpeg on Windows:")
            print("   1. Download from https://ffmpeg.org/download.html")
            print("   2. Extract files and add bin folder to PATH")
            print("   3. Verify with: ffmpeg -version")
        elif os.name == "posix":  # Linux/macOS
            if sys.platform == "darwin":  # macOS
                print("   To install ffmpeg on macOS:")
                print("   1. Run: brew install ffmpeg")
                print("   2. Verify with: ffmpeg -version")
            else:  # Linux
                print("   To install ffmpeg on Linux:")
                print(
                    "   1. Run: sudo apt-get update && sudo apt-get install -y ffmpeg"
                )
                print("   2. Verify with: ffmpeg -version")

    elif dependency == "ghostscript":
        if os.name == "nt":  # Windows
            print("   To install Ghostscript on Windows:")
            print("   1. Download from https://ghostscript.com/releases/gsdnld.html")
            print("   2. Run the installer (it will add to PATH automatically)")
            print("   3. Verify with: gswin64c -version")


def main(debug: bool = False) -> int:
    """Main function to check the development environment setup.

    Args:
        debug (bool): If True, print debug information.

    Returns:
        int: 0 if all required checks passed, 1 otherwise.
    """
    print("\n🔍 Checking development environment setup...\n")

    # Required checks (these must pass)
    required_checks = [check_git_repo(), check_virtual_env(), check_requirements(debug)]

    # Informational checks (these don't have to pass)
    external_deps = check_external_dependencies()

    print("\n" + "=" * 50)
    if all(required_checks):
        print("✨ All required checks passed! You're ready to start development!")
        if not all(external_deps.values()):
            print("\nℹ️  Note: Some recommended external dependencies are missing.")
            print("   These are not required for all features, but you may need")
            print("   to install them later depending on which parts of the project")
            print("   you're working with.")
    else:
        print("⚠️  Some checks failed. Please address the issues above.")
    print("=" * 50 + "\n")

    return 0 if all(required_checks) else 1


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Check development environment setup.")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    sys.exit(main(debug=args.debug))
