#!/usr/bin/env python3
"""
Development environment verification script.

This module checks if the development environment is properly set up,
including virtual environment, required packages, and external dependencies.
"""

import importlib.metadata
import os
import sys
from pathlib import Path

# Try to import external dependency checking
try:
    from src.utils.external_deps import check_all_dependencies

    external_deps_available = True
except ImportError:
    external_deps_available = False


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
            "darwin": "source .venv/bin/activate",  # macOS
            "nt": r".venv\Scripts\activate",  # Windows
            "posix": "source .venv/bin/activate",  # Linux
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
        debug: If True, print debug information.

    Returns:
        bool: True if all required packages are installed, False otherwise.
    """
    # Check for core requirements first
    core_requirements_file = (
        Path(__file__).resolve().parent.parent / "requirements-core.txt"
    )

    if not core_requirements_file.exists():
        print("❌ requirements-core.txt not found")
        print("   Please ensure you're in the correct directory")
        return False

    # Read requirements file
    with open(core_requirements_file) as f:
        requirements = [
            line.strip().split("#")[0].strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
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
        print("   pip install -r requirements-core.txt")
        return False

    print("✅ All core packages are installed")

    # Check optional packages
    optional_files = [
        ("requirements-ocr.txt", "OCR"),
        ("requirements-table.txt", "Table extraction"),
        ("requirements-audio.txt", "Audio transcription"),
    ]

    for req_file, feature_name in optional_files:
        file_path = Path(__file__).resolve().parent.parent / req_file
        if file_path.exists():
            # Check if packages from this file are installed
            with open(file_path) as f:
                opt_requirements = [
                    line.strip().split("#")[0].strip()
                    for line in f
                    if line.strip() and not line.strip().startswith("#")
                ]

            opt_missing = []
            for requirement in opt_requirements:
                package = (
                    requirement.split("==")[0]
                    .split(">=")[0]
                    .split("<=")[0]
                    .split(">")[0]
                    .split("<")[0]
                    .strip()
                )
                normalized_package = package.lower().replace("-", ".").replace("_", ".")
                if normalized_package not in installed_packages:
                    opt_missing.append(package)

            if not opt_missing:
                print(f"✅ Optional {feature_name} packages are installed")
            else:
                print(f"⚠️  Some optional {feature_name} packages are missing:")
                print(f"   To enable {feature_name} features, install:")
                print(f"   pip install -r {req_file}")

    return True


def check_git_repo() -> bool:
    """Check if the current directory is a git repository.

    Returns:
        bool: True if the current directory is a git repository, False otherwise.
    """
    git_dir = Path(__file__).resolve().parent.parent / ".git"
    if not git_dir.is_dir():
        print("❌ Not in a git repository")
        print(
            "   Please ensure you've cloned the project and are in the correct directory"
        )
        return False
    print("✅ Git repository found")
    return True


def main(debug: bool = False) -> int:
    """Main function to check the development environment setup.

    Args:
        debug: If True, print debug information.

    Returns:
        int: 0 if all checks passed, 1 otherwise.
    """
    print("\n🔍 Checking development environment setup...\n")

    checks = [check_git_repo(), check_virtual_env(), check_requirements(debug)]

    # Check external dependencies if available
    if external_deps_available:
        print("\n📦 Checking external dependencies...")
        external_deps = check_all_dependencies(print_instructions=True)
        # Don't fail if external deps are missing - just inform
        if not all(external_deps.values()):
            print("⚠️  Some external dependencies are missing")
            print("   Some features may not work without them")
            print("   See docs/DEPENDENCIES.md for installation instructions")
        else:
            print("✅ All external dependencies are installed")

    print("\n" + "=" * 50)
    if all(checks):
        print("✨ All core checks passed! You're ready to start development!")
        print("   Note: Some optional features may require additional dependencies")
    else:
        print("⚠️  Some checks failed. Please address the issues above.")
    print("=" * 50 + "\n")

    return 0 if all(checks) else 1


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Check development environment setup.")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    sys.exit(main(debug=args.debug))
