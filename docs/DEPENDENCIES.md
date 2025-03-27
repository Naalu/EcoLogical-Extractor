# External Dependencies Guide

EcoLogical Extractor relies on several external tools for full functionality. This guide explains how to install and configure these dependencies on different platforms.

## Overview

The project has these external dependencies:

1. **Tesseract OCR** - Required for processing scanned documents
2. **FFmpeg** - Required for audio transcription
3. **LLVM** - Required for Numba (used by Whisper for audio transcription)
4. **Ghostscript** - Required for table extraction with Camelot

## Checking Dependencies

To check which dependencies are installed on your system:

```bash
python -m src.utils.external_deps
```

## Installation Instructions

### Tesseract OCR

Tesseract is an OCR engine needed for extracting text from scanned documents.

#### macOS

```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr
```

#### Windows

1. Download the installer from the [UB-Mannheim repository](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer and follow the prompts
3. Add the installation directory to your PATH environment variable

### FFmpeg

FFmpeg is required for audio processing and transcription.

#### macOS

```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y ffmpeg
```

#### Windows

1. Download the build from [FFmpeg's official site](https://ffmpeg.org/download.html)
2. Extract the archive to a directory (e.g., `C:\ffmpeg`)
3. Add the `bin` folder to your PATH environment variable

### LLVM

LLVM is required for Numba, which Whisper uses for audio transcription.

#### macOS

```bash
brew install llvm
```

After installation, set these environment variables:

```bash
export PATH="/opt/homebrew/opt/llvm/bin:$PATH"
export LLVM_CONFIG="/opt/homebrew/opt/llvm/bin/llvm-config"
export LDFLAGS="-L/opt/homebrew/opt/llvm/lib"
export CPPFLAGS="-I/opt/homebrew/opt/llvm/include"
```

For permanent setup, add these to your `~/.zshrc` or `~/.bash_profile`.

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y llvm
```

#### Windows

1. Download the installer from [LLVM releases](https://github.com/llvm/llvm-project/releases)
2. Run the installer and follow the prompts
3. Add the installation directory to your PATH environment variable

### Ghostscript

Ghostscript is required for table extraction with Camelot.

#### macOS

```bash
brew install ghostscript
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y ghostscript
```

#### Windows

1. Download the installer from [Ghostscript's official site](https://www.ghostscript.com/download.html)
2. Run the installer and follow the prompts
3. Add the installation directory to your PATH environment variable

## Troubleshooting

### LLVM Issues

If you encounter errors with `llvmlite` or `numba` installation:

1. Make sure LLVM is installed correctly
2. Check that the environment variables are set properly
3. Try installing pre-built wheels:

   ```bash
   pip install --only-binary=numba,llvmlite numba llvmlite
   ```

### Tesseract Not Found

If you see `TesseractNotFoundError`:

1. Verify Tesseract is installed: `tesseract --version`
2. Make sure it's in your PATH
3. You can explicitly set the Tesseract path in your code:

   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows example
   ```

### FFmpeg Issues

If you encounter errors with FFmpeg:

1. Verify FFmpeg is installed: `ffmpeg -version`
2. Make sure it's in your PATH
3. For Windows, ensure you've added the bin directory to your PATH

## Alternative Approach for Difficult Installations

If you're having trouble installing external dependencies, you can focus on using the core functionality first:

1. Install only the core dependencies: `pip install -r requirements-core.txt`
2. Avoid using features that require external tools until you need them
3. Gradually add optional components as your needs evolve

This modular approach allows you to start using the basic features of EcoLogical Extractor without requiring all external dependencies to be set up immediately.
