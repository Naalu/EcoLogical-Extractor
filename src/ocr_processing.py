import os

import cv2
import fitz  # PyMuPDF
import numpy as np
import pytesseract
from tqdm import tqdm  # Progress bar

# Define paths relative to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "extracted")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "ocr_output")
LOG_FILE = os.path.join(BASE_DIR, "ocr_errors.log")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def log_error(message):
    """
    Logs errors to a file for later review.

    Args:
        message (str): The error message to log.
    """
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(message + "\n")


def preprocess_image_for_ocr(image):
    """
    Applies preprocessing to improve OCR accuracy.

    Args:
        image (numpy.ndarray): The input image.

    Returns:
        numpy.ndarray: The preprocessed image.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)  # Reduce noise
    threshold = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[
        1
    ]  # Thresholding
    return threshold


def extract_text_from_scanned_pdf(pdf_path):
    """
    Extracts text from scanned PDFs using Tesseract OCR.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF, or None if no text is detected.
    """
    try:
        doc = fitz.open(pdf_path)
        extracted_text = ""

        for i, page in enumerate(doc):
            pix = page.get_pixmap()
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                pix.h, pix.w, -1
            )  # Convert to NumPy array

            # Preprocess image
            processed_img = preprocess_image_for_ocr(img)

            # OCR processing
            text = pytesseract.image_to_string(processed_img)
            extracted_text += f"\nPage {i + 1}:\n{text}\n"

        return (
            extracted_text.strip() if extracted_text.strip() else None
        )  # Return None if no text extracted

    except Exception as e:
        log_error(f"❌ Failed to process {pdf_path}: {str(e)}")
        return None


def process_scanned_pdfs(force_extract=False):
    """
    Processes all scanned PDFs in the extracted folder using OCR.

    Args:
        force_extract (bool): If True, reprocess all PDFs even if the text files already exist. Defaults to False.

    - Skips already processed PDFs unless force_extract=True.
    - Provides clear console output on which files are processed vs. skipped.
    """
    if not os.path.exists(DATA_DIR) or not any(
        f.endswith(".pdf") for f in os.listdir(DATA_DIR)
    ):
        print("❌ No PDFs found in extracted directory. Run extract_data.py first.")
        return

    pdf_files = [
        f
        for f in os.listdir(DATA_DIR)
        if f.lower().endswith(".pdf") and not f.startswith("._")
    ]

    if not pdf_files:
        print("❌ No valid PDFs found. Hidden files may have been filtered.")
        return

    print(f"📂 Processing {len(pdf_files)} PDFs with OCR...")

    # Create progress bar
    pbar = tqdm(pdf_files, desc="OCR Processing", unit="file")
    skipped_files = []
    failed_files = []

    for filename in pbar:
        # Update progress bar description with current file
        pbar.set_description(f"Processing {filename}")

        pdf_path = os.path.join(DATA_DIR, filename)
        output_filename = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        # Skip if text file already exists (unless force_extract is set)
        if os.path.exists(output_path) and not force_extract:
            skipped_files.append(filename)
            continue

        text = extract_text_from_scanned_pdf(pdf_path)

        # Track failed OCR attempts
        if text is None:
            failed_files.append(filename)
            continue

        # Save OCR text to output file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

    # Print summary after completion
    print("\n✅ OCR Processing complete!")
    if skipped_files:
        print(f"⏭️  Skipped {len(skipped_files)} already processed files")
    if failed_files:
        print(f"❌ Failed to process {len(failed_files)} files")
        for file in failed_files:
            log_error(f"OCR failed for: {file}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Process scanned PDFs using OCR and save the extracted text."
    )
    parser.add_argument(
        "--force-extract",
        action="store_true",
        help="Force extraction even if text files already exist",
    )
    args = parser.parse_args()

    process_scanned_pdfs(force_extract=args.force_extract)
