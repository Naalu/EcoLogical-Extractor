@echo off
REM Quick setup script for EcoLogical Extractor on Windows

echo Creating virtual environment...
python -m venv .venv
call .venv\Scripts\activate

echo Installing core dependencies...
pip install -r requirements-core.txt

echo Creating data directories...
python setup_env.py --create-dirs

echo Checking external dependencies...
python -m src.utils.external_deps

echo Setup complete! Run 'python src/setup_test.py' to verify your installation.