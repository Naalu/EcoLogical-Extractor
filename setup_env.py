#!/usr/bin/env python3
"""
EcoLogical Extractor Environment Setup
=====================================

This script automates the setup of the development environment for
the EcoLogical Extractor project across different platforms.

It handles:
1. Creating a virtual environment
2. Installing dependencies (core and optional)
3. Setting up pre-commit hooks
4. Creating required data directories
5. Downloading necessary models
6. Verifying installation
"""

import argparse
import platform
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Union

# Import utility functions if available, otherwise define stub functions
try:
    from src.utils.external_deps import check_all_dependencies, get_env_var_instructions

    external_deps_available = True
except ImportError:
    # Stub functions if module not available yet
    def check_all_dependencies() -> dict[str, bool]:  # type: ignore
        return {}  # type: ignore

    def get_env_var_instructions() -> str:
        return ""

    external_deps_available = False


def print_step(message: str) -> None:
    """Print a formatted step message."""
    print(f"\n\033[1;34m==> {message}\033[0m")


def print_success(message: str) -> None:
    """Print a formatted success message."""
    print(f"\033[1;32m✓ {message}\033[0m")


def print_error(message: str) -> None:
    """Print a formatted error message."""
    print(f"\033[1;31m✗ {message}\033[0m")


def print_warning(message: str) -> None:
    """Print a formatted warning message."""
    print(f"\033[1;33m! {message}\033[0m")


def run_command(
    command: Union[List[str], str], shell: bool = False, check: bool = True
) -> Optional[subprocess.CompletedProcess]:
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=check,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {e}")
        print(e.stderr)
        return None


def check_python_version() -> bool:
    """Check if Python version is 3.9 or higher."""
    print_step("Checking Python version")

    major, minor = sys.version_info.major, sys.version_info.minor
    if major < 3 or (major == 3 and minor < 9):
        print_error("Python 3.9 or higher is required")
        print(f"Current version: {major}.{minor}")
        print("Please install a compatible Python version and try again")
        return False

    print_success(f"Python {major}.{minor} detected")
    return True


def setup_virtual_env(env_name: str, conda: bool = False) -> bool:
    """Create and activate a virtual environment."""
    print_step(f"Setting up virtual environment: {env_name}")

    # Check if virtual environment already exists
    env_path = Path(env_name)
    if env_path.exists():
        print_warning(f"Environment directory {env_name} already exists")
        response = input("Do you want to remove it and create a new one? (y/n): ")
        if response.lower() == "y":
            import shutil

            shutil.rmtree(env_path)
        else:
            print("Using existing environment")
            return True

    # Create virtual environment
    if conda:
        # Create conda environment
        result = run_command(
            [
                "conda",
                "create",
                "-y",
                "-n",
                env_name,
                f"python={'.'.join(map(str, sys.version_info[:2]))}",
            ]
        )
    else:
        # Create venv environment
        import venv

        venv.create(env_path, with_pip=True)
        print_success(f"Virtual environment created at {env_path}")

    # Provide activation instructions
    activation_cmd = ""
    if conda:
        activation_cmd = f"conda activate {env_name}"
    else:
        if platform.system() == "Windows":
            activation_cmd = f"{env_name}\\Scripts\\activate"
        else:
            activation_cmd = f"source {env_name}/bin/activate"

    print("\nTo activate the environment, run:")
    print(f"  {activation_cmd}")
    print("\nAfter activation, complete setup with:")
    print("  python setup_env.py --install-deps")

    return True


def install_dependencies(core_only: bool = True, dev: bool = False) -> bool:
    """Install project dependencies."""
    print_step("Installing dependencies")

    # Check if we're in a virtual environment
    if sys.prefix == sys.base_prefix:
        print_error("Not running in a virtual environment")
        print("Please activate your virtual environment and run this script again")
        print(
            "  For venv: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)"
        )
        print("  For conda: conda activate env_name")
        return False

    # Core dependencies are always installed
    print("Installing core dependencies...")
    result = run_command(
        [sys.executable, "-m", "pip", "install", "-r", "requirements-core.txt"]
    )
    if not result or result.returncode != 0:
        print_error("Failed to install core dependencies")
        return False

    # Development dependencies if requested
    if dev:
        print("Installing development dependencies...")
        run_command(
            [sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"]
        )

    # Optional dependencies
    if not core_only:
        # Ask about external dependencies
        if external_deps_available:
            dep_status = check_all_dependencies()
            missing_deps = [k for k, v in dep_status.items() if not v]

            if missing_deps:
                print_warning("Some external dependencies are missing.")
                print("These are required for certain optional features.")
                print("\nSee docs/DEPENDENCIES.md for installation instructions.")
                install_optional = input(
                    "\nDo you want to continue installing optional Python dependencies? (y/n): "
                )
                if install_optional.lower() != "y":
                    return True

        # Install optional components
        print("\nInstalling OCR dependencies...")
        run_command(
            [sys.executable, "-m", "pip", "install", "-r", "requirements-ocr.txt"],
            check=False,
        )

        print("Installing table extraction dependencies...")
        run_command(
            [sys.executable, "-m", "pip", "install", "-r", "requirements-table.txt"],
            check=False,
        )

        print("Installing audio transcription dependencies...")
        run_command(
            [sys.executable, "-m", "pip", "install", "-r", "requirements-audio.txt"],
            check=False,
        )

    # Platform-specific instructions
    system = platform.system()
    if system == "Windows":
        print_warning("For Windows, the fasttext package needs special installation:")
        print(
            "  1. Download the appropriate wheel file from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#fasttext"
        )
        print("  2. Install it with: pip install [downloaded-wheel-file]")

    print_success("Dependencies installed")
    return True


def setup_pre_commit() -> bool:
    """Set up pre-commit hooks."""
    print_step("Setting up pre-commit hooks")

    # Create pre-commit config if it doesn't exist
    pre_commit_file = Path(".pre-commit-config.yaml")
    if not pre_commit_file.exists():
        with open(pre_commit_file, "w") as f:
            f.write("""repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black

-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
        additional_dependencies: [flake8-docstrings]
""")

    # Install pre-commit
    run_command([sys.executable, "-m", "pip", "install", "pre-commit"])

    # Install the git hook scripts
    run_command(["pre-commit", "install"])

    print_success("Pre-commit hooks installed")
    return True


def download_models() -> bool:
    """Download required models for spaCy and other dependencies."""
    print_step("Downloading required models")

    # Download spaCy model
    print("Downloading spaCy English model...")
    run_command([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])

    print_success("Models downloaded")
    return True


def create_data_directories() -> bool:
    """Create necessary data directories if they don't exist."""
    print_step("Creating data directories")

    base_dir = Path(__file__).resolve().parent
    directories = [
        base_dir / "data" / "raw",
        base_dir / "data" / "extracted",
        base_dir / "data" / "text_output",
        base_dir / "data" / "ocr_output",
        base_dir / "data" / "tables" / "csv",
        base_dir / "data" / "tables" / "json",
        base_dir / "data" / "tables" / "logs",
    ]

    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            print_success(f"Created directory: {directory}")
        except Exception as e:
            print_error(f"Failed to create directory {directory}: {e}")
            return False

    return True


def verify_installation() -> bool:
    """Verify that the installation is working correctly."""
    print_step("Verifying installation")

    # Run the setup_test.py script
    result = run_command([sys.executable, "src/setup_test.py"])
    if result and result.returncode == 0:
        print_success("Installation verified successfully!")
        return True
    else:
        print_error("Installation verification failed")
        return False


def main() -> int:
    """Main function to orchestrate the setup process."""
    parser = argparse.ArgumentParser(
        description="Set up EcoLogical Extractor environment"
    )

    # Setup options
    setup_group = parser.add_argument_group("Environment Setup")
    setup_group.add_argument(
        "--venv", action="store_true", help="Create a virtual environment using venv"
    )
    setup_group.add_argument(
        "--conda", action="store_true", help="Create a virtual environment using conda"
    )
    setup_group.add_argument(
        "--env-name", default="venv", help="Name of the virtual environment"
    )

    # Installation options
    install_group = parser.add_argument_group("Installation")
    install_group.add_argument(
        "--install-deps", action="store_true", help="Install dependencies"
    )
    install_group.add_argument(
        "--full",
        action="store_true",
        help="Install all dependencies (core and optional)",
    )
    install_group.add_argument(
        "--dev", action="store_true", help="Install development dependencies"
    )
    install_group.add_argument(
        "--pre-commit", action="store_true", help="Set up pre-commit hooks"
    )
    install_group.add_argument(
        "--download-models", action="store_true", help="Download required models"
    )
    install_group.add_argument(
        "--create-dirs", action="store_true", help="Create required data directories"
    )
    install_group.add_argument(
        "--check-deps", action="store_true", help="Check external dependencies"
    )

    # Verification
    parser.add_argument("--verify", action="store_true", help="Verify installation")

    # Full setup
    parser.add_argument(
        "--all", action="store_true", help="Perform complete setup (all steps)"
    )

    args = parser.parse_args()

    # Check if no arguments were provided
    if len(sys.argv) == 1 or args.all:
        # Ask the user which setup to perform
        print("EcoLogical Extractor Setup\n")

        # Check Python version first
        if not check_python_version():
            return 1

        # Ask about virtual environment
        venv_type = input(
            "\nChoose a virtual environment type:\n1. venv (Python standard)\n2. conda (Anaconda/Miniconda)\nEnter choice (1/2): "
        )
        if venv_type == "2":
            args.conda = True
        else:
            args.venv = True

        # Ask for environment name
        env_name = input(f"\nEnter environment name (default: {args.env_name}): ")
        if env_name:
            args.env_name = env_name

        # Set up virtual environment
        if args.venv or args.conda:
            setup_virtual_env(args.env_name, args.conda)

            print("\nVirtual environment has been created.")
            print(
                "You need to activate it before continuing with dependency installation."
            )
            print("After activating, run this script again with --install-deps flag.")
            return 0

    # Check external dependencies if requested
    if args.check_deps or args.all:
        if external_deps_available:
            print("\nChecking external dependencies:")
            check_all_dependencies()
        else:
            print_warning("External dependency checking not available yet.")
            print("Install core dependencies first, then run with --check-deps again.")

    # Handle individual steps
    if args.install_deps or args.all:
        install_dependencies(not args.full, args.dev)

    if args.pre_commit or args.all:
        setup_pre_commit()

    if args.download_models or args.all:
        download_models()

    if args.create_dirs or args.all:
        create_data_directories()

    if args.verify or args.all:
        verify_installation()

    return 0


if __name__ == "__main__":
    sys.exit(main())
