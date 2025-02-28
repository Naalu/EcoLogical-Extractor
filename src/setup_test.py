import importlib.metadata
import os
import sys
from pathlib import Path


def check_virtual_env():
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


def check_requirements(debug=False):
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


def check_git_repo():
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


def main(debug=False):
    """Main function to check the development environment setup.

    Args:
        debug (bool): If True, print debug information.
    """
    print("\n🔍 Checking development environment setup...\n")

    checks = [check_git_repo(), check_virtual_env(), check_requirements(debug)]

    print("\n" + "=" * 50)
    if all(checks):
        print("✨ All checks passed! You're ready to start development!")
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
