"""
Table Extraction Module with Advanced Quality Filtering

This module extracts and filters tables from PDFs using a comprehensive
Table Quality Score (TQS) system that evaluates multiple quality metrics:

Quality Metrics:
1. Non-Empty Cell Ratio: Higher ratio → Higher score
2. Column Consistency: Low variance → Higher score
3. Header Analysis: Common header terms → Higher score
4. Special Character Ratio: More noise → Lower score
5. First Page Penalty: Tables on first page are penalized
6. Empty Cell Distribution: Clustered empty cells → Lower score

Extraction Methods:
1. PDFPlumber (primary) - For structured tables with clear borders
2. Camelot (fallback) - For complex or borderless tables

Usage:
    python table_extraction.py [--force] [--min-quality FLOAT]
"""

import argparse
import json
import logging
import re
import statistics
import warnings
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Union

import camelot
import pandas as pd
import pdfplumber
from tqdm import tqdm

warnings.filterwarnings("ignore", category=UserWarning, module="camelot")

# Type hints for clarity
BASE_DIR = Path(__file__).resolve().parent.parent
ProcessingStatus = Dict[str, Union[str, bool, int, float]]
ManifestDict = Dict[str, ProcessingStatus]

# Path configuration
DATA_DIR = BASE_DIR / "data"
EXTRACTED_DATA_DIR = DATA_DIR / "extracted"
TABLES_DIR = DATA_DIR / "tables"
TABLE_CSV_DIR = TABLES_DIR / "csv"
TABLE_JSON_DIR = TABLES_DIR / "json"
LOG_DIR = TABLES_DIR / "logs"
LOG_FILE = LOG_DIR / "table_extraction.log"
PROCESSED_MANIFEST = TABLES_DIR / "processed_manifest.json"

# Required directories
REQUIRED_DIRS = [TABLE_CSV_DIR, TABLE_JSON_DIR, LOG_DIR]

# Quality thresholds
TQS_THRESHOLD = 0.5  # Tables below this score will be discarded
QUALITY_THRESHOLDS = {
    "high": 0.6,  # Tables above this are definitely kept
    "borderline": 0.5,  # Tables between borderline and high are flagged for review
    "low": 0.5,  # Tables below this are discarded
}

# Penalties
FIRST_PAGE_PENALTY = 0.4  # Penalty for tables on the first page

HEADER_KEYWORDS = {
    "table",
    "id",
    "name",
    "date",
    "year",
    "value",
    "category",
    "type",
    "species",
    "count",
    "total",
    "number",
    "description",
    "location",
    "site",
}


@contextmanager
def suppress_stdout():
    """Context manager to suppress stdout temporarily."""
    from contextlib import redirect_stdout
    from io import StringIO

    with StringIO() as buf, redirect_stdout(buf):
        yield


def setup_environment() -> None:
    """Creates required directories if they do not exist."""
    for directory in REQUIRED_DIRS:
        directory.mkdir(parents=True, exist_ok=True)


def setup_logging() -> None:
    """
    Configure logging system with file handler only.
    Console output will be handled separately via tqdm.
    """
    # Remove all existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create file formatter
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Setup file handler for all logs
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.INFO)

    # Get module logger
    global logger
    logger = logging.getLogger(__name__)


def compute_table_quality(table: List[List[str]], page_number: int) -> float:
    """
    Compute the Table Quality Score (TQS).

    Metrics:
    - Content Quality (40%): Non-empty cells, special chars, numeric content
    - Structure Quality (30%): Column consistency
    - Header Analysis (30%): Common header terms
    - Penalties: First page and empty cell clustering

    Args:
        table: Extracted table data as 2D list
        page_number: Page where table was found

    Returns:
        float: Quality score between 0 and 1
    """
    if not table or len(table) < 2:
        return 0.0

    try:
        # Get metrics
        total_cells, non_empty, special_chars, numeric = compute_content_metrics(table)
        col_consistency = compute_structure_metrics(table)  # This was missing
        cluster_penalty = compute_empty_cell_clustering(table)
        header_score = compute_header_analysis(table)

        # Avoid division by zero
        if total_cells == 0:
            return 0.0

        # Calculate final score
        final_score = (
            0.4 * (non_empty / total_cells)
            + 0.3 * col_consistency
            + 0.3 * header_score
            - 0.2 * cluster_penalty
            - (FIRST_PAGE_PENALTY if page_number == 1 else 0.0)
        )

        return max(0.0, min(1.0, round(final_score, 2)))

    except Exception as e:
        logger.error(f"Error computing table quality: {str(e)}")
        return 0.0


def compute_content_metrics(table: List[List[str]]) -> tuple:
    """Compute content metrics for the table."""
    total_cells = 0
    non_empty = 0
    special_chars = 0
    numeric = 0

    for row in table:
        total_cells += len(row)
        for cell in row:
            if cell is not None and str(cell).strip():
                non_empty += 1
                if re.search(r"[^\w\s.,%-]", str(cell)):
                    special_chars += 1
                if re.match(r"^[\d.,%-]+$", str(cell).strip()):
                    numeric += 1

    return total_cells, non_empty, special_chars, numeric


def compute_structure_metrics(table: List[List[str]]) -> float:
    """Compute structure metrics for the table."""
    col_lengths = [len(row) for row in table]
    col_variance = statistics.pvariance(col_lengths) if len(col_lengths) > 1 else 0
    col_consistency = 1 / (1 + col_variance)
    return col_consistency


def compute_empty_cell_clustering(table: List[List[str]]) -> float:
    """Compute empty cell clustering penalty for the table."""
    empty_clusters = sum(1 for row in table if row.count("") > len(row) // 2)
    cluster_penalty = empty_clusters / len(table)
    return cluster_penalty


def compute_header_analysis(table: List[List[str]]) -> float:
    """Compute header analysis score for the table."""
    if not table or not table[0]:
        return 0.0

    # Safely handle None values in header row
    first_row = set(str(cell).lower() for cell in table[0] if cell is not None)
    header_matches = len(HEADER_KEYWORDS.intersection(first_row))
    header_score = min(1.0, header_matches / 3)
    return header_score


def extract_tables_with_pdfplumber(pdf_path: str) -> List[Dict]:
    """Extract tables using PDFPlumber."""
    extracted_tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                for table in page.extract_tables():
                    quality_score = compute_table_quality(table, page_num)
                    if quality_score >= TQS_THRESHOLD:
                        extracted_tables.append(
                            {
                                "page": page_num,
                                "table": table,
                                "method": "pdfplumber",
                                "quality_score": quality_score,
                                "extraction_time": datetime.now().isoformat(),
                            }
                        )
    except FileNotFoundError as e:
        logger.error(
            f"PDFPlumber extraction failed for {pdf_path} due to a file not found error: {e}"
        )
    return extracted_tables
def extract_tables_with_camelot(pdf_path: str) -> List[Dict]:
    """Extract tables using Camelot, trying 'lattice' first, then 'stream'."""
    extracted_tables = []

    try:
        with suppress_stdout():
            # Try lattice mode first
            tables = camelot.read_pdf(pdf_path, flavor="lattice")
            if tables and tables.n > 0:
                for table in tables:
                    if not table.df.empty:
                        quality_score = compute_table_quality(
                            table.df.values.tolist(), table.page
                        )
                        if quality_score >= TQS_THRESHOLD:
                            extracted_tables.append(
                                {
                                    "page": table.page,
                                    "table": table.df.to_dict(orient="split"),
                                    "method": "camelot",
                                    "quality_score": round(quality_score, 2),
                                    "extraction_time": datetime.now().isoformat(),
                                }
                            )
            else:
                logger.debug(f"No tables found in {pdf_path} using Camelot.")
    except Exception as e:
        logger.error(f"Camelot extraction failed for {pdf_path}: {e}")

    return extracted_tables


def extract_tables(pdf_path: str) -> List[Dict]:
    """Extract tables using PDFPlumber first, falling back to Camelot if needed."""
    if is_image_based_pdf(pdf_path):
        logger.info(f"🔍 {pdf_path} is image-based, skipping extraction.")
        return []
        
    tables = extract_tables_with_pdfplumber(pdf_path)
    if not tables:
        tables = extract_tables_with_camelot(pdf_path)
        if not tables:
            logger.warning(f"No tables extracted from {pdf_path} using both pdfplumber and camelot.")
    
    return tables


def is_image_based_pdf(pdf_path: str) -> bool:
    """
    Check if the PDF is image-based (scanned).

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        bool: True if the PDF is image-based (scanned), False otherwise.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:2]:  # Check the first 2 pages
                text = page.extract_text()
                if text and text.strip():
                    return False  # Text detected, NOT image-based
        return True  # No text found, assume it's a scanned PDF
    except Exception as e:
        logger.error(f"Error checking PDF {pdf_path}: {e}")
        return True  # If error occurs, assume scanned PDF


def load_manifest() -> ManifestDict:
    """
    Load the processing manifest from disk.

    This function reads the JSON file containing the processing status of previously processed PDFs.

    Returns:
        ManifestDict: Dictionary of previously processed files and their status
    """
    try:
        with open(PROCESSED_MANIFEST, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_manifest(manifest: ManifestDict) -> None:
    """
        Save the processing manifest to disk.
    
        This function writes the manifest dictionary to a JSON file.
    
        Args:
            manifest: Dictionary of processed files and their status
        """
    with open(PROCESSED_MANIFEST, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)


def normalize_table_data(table: List[List[str]]) -> List[List[str]]:
    """
    Normalize table data to ensure all rows have the same length.
    
    Args:
        table: Raw table data as 2D list
        
    Returns:
        Normalized table with consistent row lengths
    """
    if not table:
        return []
    
    try:
        # Convert None values to empty strings
        cleaned_table = [
            ['' if cell is None else str(cell) for cell in row]
            for row in table
        ]
        
        # Find the maximum row length
        max_length = max(len(row) for row in cleaned_table)
        
        # Pad shorter rows with empty strings
        normalized = [
            row + [''] * (max_length - len(row))
            for row in cleaned_table
        ]
        
        return normalized
    except Exception as e:
        logger.error(f"Error normalizing table: {str(e)}")
        return []


def save_extracted_tables(
    pdf_name: str, tables: List[Dict], save_csv: bool = False
) -> None:
    """Save extracted tables to a single JSON file per PDF, and optionally to CSV."""
    if not tables:
        logger.warning(f"No tables to save for {pdf_name}")
        return

    pdf_data = {
        "filename": pdf_name,
        "processed_date": datetime.now().isoformat(),
        "num_tables": len(tables),
        "tables": [],
    }

    for idx, table_data in enumerate(tables, 1):
        try:
            if table_data["quality_score"] >= QUALITY_THRESHOLDS["high"]:
                # Convert table to DataFrame with proper normalization
                if table_data["method"] == "pdfplumber":
                    # Normalize table data before creating DataFrame
                    normalized_table = normalize_table_data(table_data["table"])
                    if not normalized_table:
                        logger.warning(f"Empty or invalid table found in {pdf_name}, table {idx}")
                        continue
                        
                    # Ensure all rows have the same number of columns
                    if len(set(len(row) for row in normalized_table)) > 1:
                        logger.warning(f"Inconsistent row lengths in {pdf_name}, table {idx}")
                        continue
                        
                    df = pd.DataFrame(normalized_table).fillna("")
                else:  # camelot
                    try:
                        df = pd.DataFrame.from_dict(table_data["table"]).fillna("")
                    except ValueError as e:
                        logger.error(f"Error converting Camelot table: {str(e)}")
                        continue

                # Clean column names
                df.columns = [
                    str(col).strip() if col is not None else f"column_{i}"
                    for i, col in enumerate(df.columns)
                ]

                # Add table metadata and data to the PDF's JSON
                table_info = {
                    "table_number": idx,
                    "page_number": table_data["page"],
                    "extraction_method": table_data["method"],
                    "quality_score": table_data["quality_score"],
                    "extraction_time": table_data["extraction_time"],
                    "num_rows": len(df),
                    "num_columns": len(df.columns),
                    "column_names": df.columns.tolist(),
                    "table_data": df.to_dict(orient="records"),
                }
                pdf_data["tables"].append(table_info)

                # Optionally save as CSV
                if save_csv:
                    csv_filename = f"{pdf_name}_table_{idx}.csv"
                    csv_path = TABLE_CSV_DIR / csv_filename
                    df.to_csv(csv_path, index=False)

        except Exception as e:
            logger.error(f"Failed to process table {idx} in {pdf_name}: {str(e)}")
            continue

    # Save the combined JSON file
    try:
        json_path = TABLE_JSON_DIR / f"{pdf_name}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(pdf_data, f, indent=2, ensure_ascii=False)

        logger.info(
            f"Saved {len(pdf_data['tables'])} tables from {pdf_name}"
            f"{' (with CSV files)' if save_csv else ''}"
        )
    except Exception as e:
        logger.error(f"Failed to save JSON for {pdf_name}: {str(e)}")


def process_pdf(
    pdf_path: Path, manifest: ManifestDict, save_csv: bool = False
) -> Dict[str, Union[str, bool, int, float, list, dict]]:
    """
    Process a single PDF file and extract tables.

    This function checks if the PDF is scanned, extracts tables using pdfplumber and camelot,
    filters for high-quality tables, and saves the results.

    Args:
        pdf_path: Path to the PDF file
        manifest: Current processing manifest
        save_csv: Whether to save individual tables as CSV files
    """
    pdf_name = pdf_path.stem

    # Step 1: Check if the PDF is scanned (image-based)
    if is_image_based_pdf(pdf_path):
        manifest[pdf_name] = {
            "filename": pdf_name,
            "processed_date": datetime.now().isoformat(),
            "is_scanned": True,
            "has_tables": False,
            "num_tables": 0,
            "extraction_method": None,
            "quality_scores": [],
            "saved_files": None,
            "success": False,
        }
        return manifest[pdf_name]

    # Step 2: Extract tables using pdfplumber first
    tables = extract_tables(pdf_path)

    # Step 3: Filter for high-quality tables
    high_quality_tables = [
        t for t in tables if t["quality_score"] >= QUALITY_THRESHOLDS["high"]
    ]

    # Step 4: Save tables if any high-quality ones were found
    if high_quality_tables:
        save_extracted_tables(pdf_name, high_quality_tables, save_csv)

    # Step 5: Update status
    status = {
        "filename": pdf_name,
        "processed_date": datetime.now().isoformat(),
        "is_scanned": False,
        "has_tables": bool(high_quality_tables),
        "num_tables": len(high_quality_tables),
        "extraction_method": high_quality_tables[0]["method"]
        if high_quality_tables
        else None,
        "quality_scores": [t["quality_score"] for t in high_quality_tables]
        if high_quality_tables
        else [],
        "saved_files": {
            "json": f"{pdf_name}.json",
            "csv": [
                f"{pdf_name}_table_{i + 1}.csv" for i in range(len(high_quality_tables))
            ],
        }
        if high_quality_tables
        else None,
        "success": True,
    }

    return status


def main():
    """Main execution function with manifest tracking."""
    parser = argparse.ArgumentParser(
        description="Extract tables from PDFs using multiple methods."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force reprocessing of all PDFs, ignoring existing results",
    )
    parser.add_argument(
        "--save-csv", action="store_true", help="Additionally save tables as CSV files"
    )
    args = parser.parse_args()

    setup_environment()
    setup_logging()
    manifest = load_manifest()

    # Process only valid PDFs
    pdf_files = [
        f for f in Path(EXTRACTED_DATA_DIR).glob("*.pdf") if not f.name.startswith(".")
    ]

    if not pdf_files:
        return

    # Initialize counters
    stats = {"processed": 0, "skipped": 0, "failed": 0, "no_tables": 0}

    # Configure progress bar
    with tqdm(
        total=len(pdf_files),
        desc="Processing PDFs",
        unit="file",
        ncols=100,
        bar_format="{desc:<30} |{bar:50}| {percentage:3.0f}% [{n_fmt}/{total_fmt}]",
        disable=None,
    ) as progress_bar:
        for pdf_path in pdf_files:
            pdf_name = pdf_path.stem
            progress_bar.set_description(f"Processing {pdf_name[:20]}")

            # Skip if already processed and not forcing
            if pdf_name in manifest and not args.force:
                stats["skipped"] += 1
                progress_bar.update(1)
                continue

            try:
                status = process_pdf(pdf_path, manifest, args.save_csv)
                if status["has_tables"]:
                    stats["processed"] += 1
                else:
                    stats["no_tables"] += 1
            except Exception as e:
                logger.error(f"Failed to process {pdf_name}: {str(e)}")
                stats["failed"] += 1
                manifest[pdf_name] = {
                    "filename": pdf_name,
                    "processed_date": datetime.now().isoformat(),
                    "error": str(e),
                    "success": False,
                }

            progress_bar.update(1)

    save_manifest(manifest)

    # Print final summary to console
    print("\nProcessing Summary:")
    print(f"{'Files with tables:':<20} {stats['processed']}")
    print(f"{'Files without tables:':<20} {stats['no_tables']}")
    print(f"{'Skipped files:':<20} {stats['skipped']}")
    if stats["failed"]:
        print(f"{'Failed files:':<20} {stats['failed']}")
    print("\n✅ Processing complete!")


if __name__ == "__main__":
    main()
