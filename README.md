# EcoLogical-Extractor

<img src="docs/images/logo.png" alt="EcoLogical Extractor Logo" width="150" align="right"/>

**EcoLogical Extractor** is a specialized data extraction system that parses, analyzes, and structures geographic and keyword information from ecological research publications. This tool helps researchers discover relevant studies by location and topic, significantly reducing search time and revealing connections across research projects.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Last Commit](https://img.shields.io/github/last-commit/Naalu/EcoLogical-Extractor.svg)](https://github.com/Naalu/EcoLogical-Extractor/commits/main)
[![Issues](https://img.shields.io/github/issues/Naalu/EcoLogical-Extractor.svg)](https://github.com/Naalu/EcoLogical-Extractor/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

***

## 📋 Table of Contents

- [EcoLogical-Extractor](#ecological-extractor)
  - [📋 Table of Contents](#-table-of-contents)
  - [🌟 Overview](#-overview)
  - [🚀 Key Features](#-key-features)
  - [💡 Why EcoLogical Extractor?](#-why-ecological-extractor)
    - [Impact Metric Goals](#impact-metric-goals)
  - [🚀 Quick Start](#-quick-start)
    - [Prerequisites](#prerequisites)
    - [Basic Installation](#basic-installation)
  - [📋 Detailed Setup Guide](#-detailed-setup-guide)
    - [Virtual Environment Setup](#virtual-environment-setup)
    - [Platform-Specific Setup](#platform-specific-setup)
      - [Windows](#windows)
      - [macOS](#macos)
      - [Linux (Ubuntu/Debian)](#linux-ubuntudebian)
    - [Verifying External Dependencies](#verifying-external-dependencies)
  - [📊 Usage Examples](#-usage-examples)
    - [Processing Documents](#processing-documents)
    - [Extracting Geographic Information](#extracting-geographic-information)
    - [Visualization](#visualization)
  - [📁 Project Structure](#-project-structure)
  - [⚠️ Troubleshooting](#️-troubleshooting)
    - [Common Issues](#common-issues)
      - [Tesseract Not Found Error](#tesseract-not-found-error)
      - [SpaCy Model Not Found Error](#spacy-model-not-found-error)
      - [ffmpeg Not Found Error](#ffmpeg-not-found-error)
      - [PDF Processing Errors](#pdf-processing-errors)
      - [Virtual Environment Issues](#virtual-environment-issues)
  - [🤝 Contributing](#-contributing)
  - [📄 License](#-license)
  - [🙏 Acknowledgements](#-acknowledgements)
  - [🆘 Getting Help](#-getting-help)

## 🌟 Overview

Developed for the [Ecological Restoration Institute (ERI)](https://eri.nau.edu/) at Northern Arizona University, EcoLogical Extractor addresses a critical need to make their extensive research library (1,134+ publications) more accessible and searchable within their ContentDM system.

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

### Impact Metric Goals

- **80-90%** reduction in search time for location-based queries
- **85%+** accuracy in geographic entity recognition
- **90%+** extraction success rate across document types
- Integration with **1,134** research publications

## 🚀 Quick Start

### Prerequisites

- Python >3.8 and <3.12
- pip (Python package manager)
- Git
- Tesseract OCR (see platform-specific setup below)
- spaCy and its language models

### Basic Installation

```bash
# Clone the repository
git clone https://github.com/Naalu/EcoLogical-Extractor.git
cd EcoLogical-Extractor

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install spaCy language model
python -m spacy download en_core_web_lg

# Verify installation
python src/setup_test.py
```

## 📋 Detailed Setup Guide

### Virtual Environment Setup

We strongly recommend using a virtual environment for development and deployment.

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

2. **Install ffmpeg** (required for audio transcription):
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Extract files and add the bin folder to your PATH
   - Verify installation: `ffmpeg -version`

3. **Install Ghostscript** (required for table extraction):
   - Download from [Ghostscript Downloads](https://ghostscript.com/releases/gsdnld.html)
   - Run the installer (it will add to PATH automatically)
   - Verify installation: `gswin64c -version`

4. **Install spaCy language model**:

   ```bash
   python -m spacy download en_core_web_lg
   ```

5. **Install requirements**:

   ```bash
   pip install -r requirements.txt
   ```

#### macOS

1. **Install Tesseract OCR**:

   ```bash
   brew install tesseract
   ```

2. **Install ffmpeg** (required for audio transcription):

   ```bash
   brew install ffmpeg
   ```

3. **Install spaCy language model**:

   ```bash
   python -m spacy download en_core_web_lg
   ```

4. **Install requirements**:

   ```bash
   pip install -r requirements.txt
   ```

#### Linux (Ubuntu/Debian)

1. **Install Tesseract OCR and ffmpeg**:

   ```bash
   sudo apt-get update
   sudo apt-get install -y tesseract-ocr libtesseract-dev ffmpeg
   ```

2. **Install spaCy language model**:

   ```bash
   python -m spacy download en_core_web_lg
   ```

3. **Install requirements**:

   ```bash
   pip install -r requirements.txt
   ```

### Verifying External Dependencies

Run the setup test script to get detailed information about your environment:

```bash
python src/setup_test.py
```

This will check for:

- Python package requirements
- Virtual environment activation
- External dependencies (Tesseract OCR, ffmpeg, Ghostscript on Windows)

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
├── src/                # Source code
│   ├── cms_integration.py      # ContentDM integration
│   ├── data_structuring.py     # Data transformation and storage
│   ├── main.py                 # Main entry point
│   ├── mp3_text_extraction.py  # Audio transcription
│   ├── nlp_extraction.py       # NLP analysis
│   ├── ocr_processing.py       # OCR for scanned documents
│   ├── pdf_text_extraction.py  # PDF text extraction
│   ├── setup_test.py           # Environment verification
│   ├── table_extraction.py     # Table extraction
│   └── visualization.py        # Data visualization
├── tests/              # Test suite
├── .gitignore          # Git ignore configuration
├── LICENSE             # MIT License
├── pyproject.toml      # Project configuration
├── README.md           # This file
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

#### SpaCy Model Not Found Error

**Symptoms**: `OSError: [E050] Can't find model 'en_core_web_lg'`

**Solutions**:

1. Install the model manually:

   ```bash
   python -m spacy download en_core_web_lg
   ```

2. Verify installation:

   ```python
   import spacy
   nlp = spacy.load("en_core_web_lg")
   ```

#### ffmpeg Not Found Error

**Symptoms**: `FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'`

**Solutions**:

1. Verify ffmpeg is installed: `ffmpeg -version`
2. Ensure it's in your PATH
3. On Windows, download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
4. On macOS: `brew install ffmpeg`
5. On Linux: `sudo apt-get install ffmpeg`

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
   pip install --force-reinstall -r requirements.txt
   ```

## 🤝 Contributing

We welcome contributions to the EcoLogical Extractor project! Please see CONTRIBUTING.md for detailed guidelines on how to contribute, including:

- Development environment setup
- Coding standards
- Testing requirements
- Pull request process

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Ecological Restoration Institute at Northern Arizona University
- Contributors and maintainers
- Open-source libraries that make this project possible

## 🆘 Getting Help

- **Issues**: Open a [GitHub Issue](https://github.com/Naalu/EcoLogical-Extractor/issues)
- **Discussion**: Join our [GitHub Discussions](https://github.com/Naalu/EcoLogical-Extractor/discussions)
- **Contact**: Reach out to project maintainers at [kcr28@nau.edu](mailto:kcr28@nau.edu)

---

For questions or support, please open an issue on GitHub or contact the project maintainers. Thank you for using EcoLogical Extractor! 🌿
