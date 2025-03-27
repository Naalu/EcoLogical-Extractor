#!/bin/bash
# Quick setup script for EcoLogical Extractor

# Create and activate virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install core dependencies
echo "Installing core dependencies..."
pip install -r requirements-core.txt

# Create data directories
echo "Creating data directories..."
python setup_env.py --create-dirs

# Check for external dependencies
echo "Checking external dependencies..."
python -m src.utils.external_deps

echo "Setup complete! Run 'python src/setup_test.py' to verify your installation."