# Contributing to EcoLogical Extractor

Thank you for your interest in contributing to EcoLogical Extractor! This document provides guidelines and best practices for contributing to the project.

## Table of Contents

- [Contributing to EcoLogical Extractor](#contributing-to-ecological-extractor)
  - [Table of Contents](#table-of-contents)
  - [Development Environment](#development-environment)
    - [Virtual Environment Best Practices](#virtual-environment-best-practices)
    - [Required Development Tools](#required-development-tools)
    - [External Dependencies](#external-dependencies)
      - [1. Tesseract OCR (Required for OCR Processing)](#1-tesseract-ocr-required-for-ocr-processing)
      - [2. ffmpeg (Required for Audio Transcription)](#2-ffmpeg-required-for-audio-transcription)
      - [3. Ghostscript (Required for Table Extraction on Windows)](#3-ghostscript-required-for-table-extraction-on-windows)
      - [Verifying External Dependencies](#verifying-external-dependencies)
  - [Development Workflow](#development-workflow)
  - [Code Style Guidelines](#code-style-guidelines)
  - [Testing](#testing)
    - [Test Structure](#test-structure)
    - [Running Tests](#running-tests)
  - [Documentation](#documentation)
    - [Docstring Example](#docstring-example)
  - [Pull Request Process](#pull-request-process)
    - [PR Template](#pr-template)
  - [Dependency Management](#dependency-management)

## Development Environment

### Virtual Environment Best Practices

Always use a virtual environment for development to ensure consistent dependencies and avoid conflicts with other projects.

1. **Create a virtual environment** (if you haven't already):

   ```bash
   # Using UV (recommended)
   uv venv

   # Using venv
   python -m venv .venv
   ```

2. **Activate your virtual environment** before any development work:

   ```bash
   # macOS/Linux
   source .venv/bin/activate

   # Windows
   .venv\Scripts\activate
   ```

3. **Verify activation** by checking your command prompt (should show environment name) or by running:

   ```bash
   python src/setup_test.py
   ```

4. **Deactivate when switching projects**:

   ```bash
   deactivate
   ```

### Required Development Tools

- **Python 3.12+**: Core language requirement
- **Git**: For version control
- **pytest**: For running tests
- **Black**: For code formatting (optional but recommended)
- **Flake8**: For linting (optional but recommended)

### External Dependencies

In addition to Python packages, EcoLogical Extractor requires several external tools for full functionality:

#### 1. Tesseract OCR (Required for OCR Processing)

**Windows**:

- Download from [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
- Add to PATH: `setx PATH "%PATH%;C:\Program Files\Tesseract-OCR"`
- Verify: `tesseract --version`

**macOS**:

- Install: `brew install tesseract`
- Verify: `tesseract --version`

**Linux**:

- Install: `sudo apt-get install tesseract-ocr libtesseract-dev`
- Verify: `tesseract --version`

#### 2. ffmpeg (Required for Audio Transcription)

**Windows**:

- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Extract files and add bin folder to PATH
- Verify: `ffmpeg -version`

**macOS**:

- Install: `brew install ffmpeg`
- Verify: `ffmpeg -version`

**Linux**:

- Install: `sudo apt-get install ffmpeg`
- Verify: `ffmpeg -version`

#### 3. Ghostscript (Required for Table Extraction on Windows)

**Windows**:

- Download from [Ghostscript Downloads](https://ghostscript.com/releases/gsdnld.html)
- Run the installer (it will add to PATH automatically)
- Verify: `gswin64c -version`

**macOS**:

- Install: `brew install ghostscript`
- Verify: `gs --version`

**Linux**:

- Install: `sudo apt-get install ghostscript`
- Verify: `gs --version`

#### Verifying External Dependencies

Run the setup test script to verify all dependencies are correctly installed:

```bash
python src/setup_test.py
```

This will perform basic checks and provide information about any missing dependencies. For detailed debugging information, add the `--debug` flag:

```bash
python src/setup_test.py --debug
```

## Development Workflow

1. **Update your local main branch**:

   ```bash
   git checkout main
   git pull origin main
   ```

2. **Create a feature branch** from `main`:

   ```bash
   git checkout -b feature/<feature-name>
   ```

   Use prefixes to categorize your branches:
   - `feature/` for new features
   - `bugfix/` for bug fixes
   - `docs/` for documentation updates
   - `refactor/` for code refactoring
   - `test/` for adding or updating tests

3. **Make small, focused commits**:
   - Write meaningful commit messages
   - Start commit messages with a short summary line
   - Each commit should address a single concern
   - Example:

     ```
     Add UTM coordinate extraction regex pattern

     - Implement regex for UTM zone identification
     - Add conversion function from UTM to lat/long
     - Add unit tests for various UTM formats
     ```

4. **Run tests** regularly and before submitting a PR:

   ```bash
   pytest
   ```

5. **Keep your branch up to date** with main:

   ```bash
   git checkout main
   git pull origin main
   git checkout feature/<feature-name>
   git rebase main
   ```

## Code Style Guidelines

We follow these coding conventions:

1. **Python Style Guide**:
   - PEP 8 compliant with a line length of 88 characters (Black compatible)
   - Google-style docstrings for all functions and classes
   - Type hints for all function parameters and return values

2. **Naming Conventions**:
   - Snake case for variables and functions (`process_document`)
   - Pascal case for classes (`DocumentProcessor`)
   - Screaming snake case for constants (`MAX_DOCUMENT_SIZE`)
   - Prefixed protected members (`_internal_method`)

3. **Format your code with Black** before committing:

   ```bash
   black src tests
   ```

4. **Check your code with Flake8**:

   ```bash
   flake8 src tests
   ```

## Testing

- Write tests for all new functionality
- Place tests in the `tests/` directory
- Name test files with the prefix `test_`
- Use pytest for running tests

### Test Structure

```python
# Example test file: tests/test_nlp_extraction.py

import pytest
from src.nlp_extraction import extract_coordinates

def test_extract_utm_coordinates():
    """Test extraction of UTM coordinates."""
    sample_text = "The study site is located at 12S 429500E 3897400N in Arizona."
    coordinates = extract_coordinates(sample_text)

    assert len(coordinates) == 1
    assert coordinates[0]["type"] == "utm"
    assert coordinates[0]["utm_zone"] == "12S"
    assert coordinates[0]["coordinates"]["latitude"] == pytest.approx(35.262, abs=0.001)
    assert coordinates[0]["coordinates"]["longitude"] == pytest.approx(-111.742, abs=0.001)
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_nlp_extraction.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src
```

## Documentation

- Update documentation for all code changes
- Use Google-style docstrings for all functions, classes, and modules
- Keep the README.md file up to date
- Add examples for new features

### Docstring Example

```python
def extract_coordinates(text: str) -> List[Dict[str, Any]]:
    """
    Extract UTM and latitude/longitude coordinates from text.

    Args:
        text: The text to analyze for coordinate patterns.

    Returns:
        A list of dictionaries containing the extracted coordinates with the following fields:
        - text: The original extracted text
        - type: The coordinate type ("utm" or "latlong")
        - coordinates: Dictionary with "latitude" and "longitude" fields
        - confidence: Confidence score between 0 and 1
        - context: Surrounding text for verification

    Raises:
        ValueError: If the input text is empty or None.
    """
```

## Pull Request Process

1. **Create a pull request** from your feature branch to `main`
2. **Fill out the PR template** with:
   - Summary of changes
   - Related issue(s)
   - Type of change (bugfix, feature, etc.)
   - How to test the changes
3. **Request review** from at least one team member
4. **Address any feedback** from reviewers
5. **Once approved**, your PR will be merged by a maintainer

### PR Template

```markdown
## Description
[Brief description of changes]

## Related Issue
Fixes #[issue number]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Other (please describe):

## How Has This Been Tested?
[Describe the tests that you ran]

## Checklist:
- [ ] My code follows the style guidelines of this project
- [ ] I have added tests that prove my fix/feature works
- [ ] All new and existing tests pass
- [ ] I have updated the documentation accordingly
- [ ] I have verified all required external dependencies are properly installed
```

## Dependency Management

1. **Adding new dependencies**:
   - Add to `requirements.txt` with specific version (e.g., `package==1.2.3`)
   - Update `pyproject.toml` if it's a direct dependency
   - Document why the dependency is needed in the PR

2. **Updating dependencies**:
   - Test thoroughly before updating versions
   - Update both `requirements.txt` and `pyproject.toml`
   - Document any breaking changes or migration steps

3. **Installing dependencies**:

   ```bash
   # Using UV (recommended)
   uv pip install -r requirements.txt

   # Using pip
   pip install -r requirements.txt
   ```

4. **Adding external dependencies**:
   - Document the dependency in README.md, DEVELOPMENT.md, and CONTRIBUTING.md
   - Add installation verification to setup_test.py
   - Provide clear installation instructions for all supported platforms
   - Consider environment variable configuration for paths

---

Thank you for contributing to EcoLogical Extractor! Your efforts help make ecological research more accessible and discoverable.
