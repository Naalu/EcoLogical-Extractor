# EcoLogical-Extractor

EcoLogical Extractor scrapes, parses, and extracts geographic and thematic data from ecological research PDFs. Leveraging OCR and NLP, it roots insights in environmental studies, streamlining restoration research and helping users branch out hidden data clues.

***

## Collaborators Instructions

### Setup Instructions

#### 1. Clone the repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/EcoLogical-Extractor.git
cd EcoLogical-Extractor
```

#### 2. Create and Activate a Virtual Environment

```bash
uv venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

#### 3. Install Dependencies

```bash
uv pip install -r requirements.txt
```

#### 4. Verify Installation

Run the following script:

```bash
python src/setup_test.py
```

Expected output:

```bash
🔍 Checking development environment setup...

✅ Git repository found
✅ Virtual environment is activated
✅ All required packages are installed

==================================================
✨ All checks passed! You're ready to start development!
==================================================
```
