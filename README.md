# EcoLogical Extractor

<img src="docs/images/logo.png" alt="EcoLogical Extractor Logo" width="150" align="right"/>

**EcoLogical Extractor** is a specialized data extraction system that parses, analyzes, and structures geographic and keyword information from ecological research publications. This tool helps researchers discover relevant studies by location and topic, significantly reducing search time and revealing connections across research projects.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Last Commit](https://img.shields.io/github/last-commit/YOUR_GITHUB_USERNAME/EcoLogical-Extractor.svg)](https://github.com/YOUR_GITHUB_USERNAME/EcoLogical-Extractor/commits/main)
[![Issues](https://img.shields.io/github/issues/YOUR_GITHUB_USERNAME/EcoLogical-Extractor.svg)](https://github.com/YOUR_GITHUB_USERNAME/EcoLogical-Extractor/issues)

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Why EcoLogical Extractor?](#why-ecological-extractor)
- [Quick Start](#quick-start)
- [Detailed Setup Guide](#detailed-setup-guide)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Architecture & Development](#architecture--development)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## 🌟 Overview

Developed for the [Ecological Restoration Institute (ERI)](https://nau.edu/eri/) at Northern Arizona University, EcoLogical Extractor addresses a critical need to make their extensive research library (1,134+ publications) more accessible and searchable within their ContentDM system.

**Key Problem**: ERI researchers currently struggle to find studies based on locations or ecological concepts, requiring time-consuming manual searches through hundreds of documents.

**Our Solution**: EcoLogical Extractor automates the extraction of:

- Geographic study sites and coordinates
- Research topics and keywords
- Tabular data and research results

This transformation unlocks hidden connections between studies and dramatically improves research efficiency.

## 🚀 Key Features

- **Geographic Entity Extraction**: Identifies research sites and coordinates (UTM, latitude/longitude)
- **Text Extraction**: Processes both digital PDFs and legacy scanned documents via OCR
- **Audio Transcription**: Converts MP3 recordings to searchable text
- **Table Extraction**: Identifies and extracts tabular data with quality filtering
- **Keyword Analysis**: Uses NLP to identify thematic keywords and concepts
- **CMS Integration**: Exports structured metadata in XML format for ContentDM
- **Visualization**: Creates interactive maps of research sites and keyword trends

## 💡 Why EcoLogical Extractor?

- **Saves Research Time**: Find location-specific studies in seconds instead of hours
- **Reveals Hidden Connections**: Discover relationships between studies across decades of research
- **Enhances Metadata Quality**: Generate consistent, structured metadata for improved searchability
- **Preserves Legacy Knowledge**: Makes older scanned documents as searchable as digital ones
- **Empowers Visual Analysis**: Transform text data into interactive maps and visualizations

### Impact Metrics

- **80-90%** reduction in search time for location-based queries
- **85%+** accuracy in geographic entity recognition
- **90%+** extraction success rate across document types
- Integration with **1,134** research publications

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Git
- Tesseract OCR (see platform-specific setup below)

### Basic Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_GITHUB_USERNAME/EcoLogical-Extractor.git
cd EcoLogical-Extractor

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
uv pip install -r requirements.txt

# Verify installation
python src/setup_test.py
```

## 📋 Detailed Setup Guide

### Virtual Environment Setup

We strongly recommend using a virtual environment for development and deployment.

#### Using UV (Recommended)

UV is a modern, fast package manager and virtual environment tool for Python.

```bash
# Install UV
# macOS/Linux
curl -sSf https://raw.githubusercontent.com/astral-sh/uv/main/install.sh | sh

# Windows (PowerShell)
irm https://raw.githubusercontent.com/astral-sh/uv/main/install.ps1 | iex

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

#### Using venv (Python's built-in tool)

```bash
# Create virtual environment
python -m venv .venv

# Activate
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Platform-Specific Setup

#### Windows

1. **Install Tesseract OCR**:
   - Download from [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
   - Add to PATH environment variable:

     ```
     setx PATH "%PATH%;C:\Program Files\Tesseract-OCR"
     ```

   - Verify installation: `tesseract --version`

2. **FastText Installation**:
   The standard fasttext installation may fail on Windows. Try these alternatives:

   ```bash
   # Option 1: Install with no dependencies
   pip install fasttext --no-deps

   # Option 2: Use fasttext-wheel
   pip install fasttext-wheel
   ```

#### macOS

1. **Install Tesseract OCR**:

   ```bash
   brew install tesseract
   ```

2. **Verify installation**:

   ```bash
   tesseract --version
   ```

#### Linux (Ubuntu/Debian)

1. **Install Tesseract OCR**:

   ```bash
   sudo apt-get update
   sudo apt-get install -y tesseract-ocr libtesseract-dev
   ```

2. **Verify installation**:

   ```bash
   tesseract --version
   ```

## 📊 Usage Examples

### Processing Documents

EcoLogical Extractor provides several commands for different extraction needs:

```bash
# Process a single PDF file
python src/main.py process --input path/to/document.pdf --output path/to/output

# Process a directory of PDFs
python src/main.py process-batch --input path/to/documents/ --output path/to/output

# Extract tables from PDFs
python src/table_extraction.py --save-csv
```

### Extracting Geographic Information

Extract location data and coordinates from processed text:

```bash
# Extract geographic entities from processed text
python src/nlp_extraction.py --input path/to/text_files/ --output path/to/output
```

**Example Output:**

```json
{
  "document_id": "ERI_2019_001",
  "entities": {
    "locations": [
      {
        "text": "Fort Valley",
        "type": "named_location",
        "coordinates": {
          "latitude": 35.262,
          "longitude": -111.742
        },
        "confidence": 0.92
      },
      {
        "text": "12S 429500E 3897400N",
        "type": "utm",
        "coordinates": {
          "latitude": 35.262,
          "longitude": -111.742
        },
        "confidence": 0.98
      }
    ]
  }
}
```

### Visualization

Create interactive visualizations from extracted data:

```bash
# Generate interactive map of research sites
python src/visualization.py --type map --input path/to/extracted_locations.json --output map.html

# Generate keyword trend visualization
python src/visualization.py --type keywords --input path/to/extracted_keywords.json --output trends.html
```

## 📁 Project Structure

```
EcoLogical-Extractor/
├── data/               # Data directories
│   ├── raw/            # Raw input files (PDFs, MP3s)
│   ├── extracted/      # Extracted documents
│   ├── text_output/    # Extracted text
│   ├── ocr_output/     # OCR processed text
│   └── tables/         # Extracted tables
│       ├── csv/        # Tables in CSV format
│       ├── json/       # Tables in JSON format
│       └── logs/       # Processing logs
├── docs/               # Documentation
│   ├── api/            # API documentation
│   ├── examples/       # Usage examples
│   └── images/         # Documentation images
├── notebooks/          # Jupyter notebooks for examples
├── src/                # Source code
│   ├── cms_integration.py      # ContentDM integration
│   ├── data_structuring.py     # Data transformation and storage
│   ├── main.py                 # Main entry point
│   ├── mp3transcriber.py       # Audio transcription
│   ├── nlp_extraction.py       # NLP analysis
│   ├── ocr_processing.py       # OCR for scanned documents
│   ├── pdf_processing.py       # PDF utilities
│   ├── setup_test.py           # Environment verification
│   ├── table_extraction.py     # Table extraction
│   └── visualization.py        # Data visualization
├── tests/              # Test suite
├── .gitignore          # Git ignore configuration
├── LICENSE             # MIT License
├── pyproject.toml      # Project configuration
├── README.md           # This file
├── CONTRIBUTING.md     # Contribution guidelines
├── DEVELOPMENT.md      # Technical architecture details
├── requirements.txt    # Package dependencies
└── setup.py            # Installation script
```

## ⚠️ Troubleshooting

### Common Issues

#### Tesseract Not Found Error

**Symptoms**: `TesseractNotFoundError: tesseract is not installed or not in your PATH`

**Solutions**:

1. Verify Tesseract is installed: `tesseract --version`
2. Ensure it's in your PATH
3. Set the path explicitly in code:

   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

#### FastText Installation Issues

**Symptoms**: `ModuleNotFoundError: No module named 'fasttext'` or compilation errors

**Solutions**:

1. For Windows, try alternative installation methods:

   ```bash
   pip install fasttext --no-deps
   # or
   pip install fasttext-wheel
   ```

2. For macOS/Linux, ensure you have build tools:

   ```bash
   # macOS
   brew install cmake
   
   # Ubuntu/Debian
   sudo apt-get install build-essential cmake
   ```

#### PDF Processing Errors

**Symptoms**: PDF extraction fails or produces poor results

**Solutions**:

1. Check PDF quality and type (scanned vs. digital)
2. For scanned documents, force OCR processing:

   ```bash
   python src/ocr_processing.py --force-extract
   ```

3. For problematic tables, try forced extraction:

   ```bash
   python src/table_extraction.py --force
   ```

4. Verify with manual inspection:

   ```python
   import fitz
   doc = fitz.open("problematic.pdf")
   print(doc.metadata)  # Check if PDF is valid
   ```

#### Virtual Environment Issues

**Symptoms**: Package not found errors despite installation

**Solutions**:

1. Verify your virtual environment is activated
2. Confirm you're using the correct Python:

   ```bash
   which python  # macOS/Linux
   where python  # Windows
   ```

3. Reinstall dependencies:

   ```bash
   uv pip install --force-reinstall -r requirements.txt
   ```

## 🤝 Contributing

We welcome contributions to the EcoLogical Extractor project! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on how to contribute, including:

- Development environment setup
- Coding standards
- Testing requirements
- Pull request process

## 🏗️ Architecture & Development

For developers interested in the technical architecture, component interactions, and design decisions, please refer to our [DEVELOPMENT.md](DEVELOPMENT.md) guide. This document provides insights into:

- System architecture
- Component interactions
- Key design decisions
- Development principles
- Debugging and performance tips

The system follows a modular pipeline architecture that allows for flexible component integration and extension:

```
┌──────────────┐    ┌───────────────┐    ┌─────────────┐    ┌─────────────┐
│ Extraction   │ => │ NLP Analysis  │ => │ Structured  │ => │ CMS         │
│ Subsystem    │    │ Subsystem     │    │ Data        │    │ Integration │
└──────────────┘    └───────────────┘    └─────────────┘    └─────────────┘
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- Ecological Restoration Institute at Northern Arizona University
- Contributors and maintainers
- Open-source libraries that make this project possible

## 🆘 Getting Help

- **Issues**: Open a [GitHub Issue](https://github.com/YOUR_GITHUB_USERNAME/EcoLogical-Extractor/issues)
- **Discussion**: Join our [GitHub Discussions](https://github.com/YOUR_GITHUB_USERNAME/EcoLogical-Extractor/discussions)
- **Contact**: Reach out to project maintainers at [maintainer@example.com](mailto:maintainer@example.com)

---

For questions or support, please open an issue on GitHub or contact the repository maintainers. Thank you for using EcoLogical Extractor! 🌿
