import os
import shutil
import zipfile

# Define paths relative to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
EXTRACT_DIR = os.path.join(BASE_DIR, "data", "extracted")


def extract_zip(force_extract=False):
    """
    Extract PDFs from a zip file in the data/raw directory, placing them directly into data/extracted/.

    Args:
        force_extract (bool): If True, force extraction even if the extracted directory already contains files.
                              Defaults to False.

    - Skips extraction if the directory already contains files unless force_extract=True.
    - Removes unnecessary nested directories (__MACOSX, p17192coll1, etc.) after extraction.
    """
    # Check if the extracted directory already has files
    if os.path.exists(EXTRACT_DIR) and os.listdir(EXTRACT_DIR) and not force_extract:
        print(
            f"⚠️ Extraction skipped: {EXTRACT_DIR} already contains files. Use force_extract=True to override."
        )
        return

    # Find a zip file in the raw data directory
    zip_files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith(".zip")]
    if not zip_files:
        print("❌ No zip file found in data/raw.")
        return

    zip_path = os.path.join(RAW_DATA_DIR, zip_files[0])

    # Ensure the extracted directory exists and is clean
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    # Extract files
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for file in zip_ref.namelist():
            if file.lower().endswith(".pdf"):
                zip_ref.extract(file, EXTRACT_DIR)

    print(f"✅ Extracted PDFs to {EXTRACT_DIR}")

    # Cleanup: Move PDFs from nested directories to the root `extracted/`
    for root, _, files in os.walk(EXTRACT_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(EXTRACT_DIR, file)
                if src_path != dest_path:  # Prevent unnecessary moves
                    shutil.move(src_path, dest_path)

    # Remove unnecessary folders (__MACOSX, p17192coll1, etc.)
    for folder in os.listdir(EXTRACT_DIR):
        folder_path = os.path.join(EXTRACT_DIR, folder)
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path, ignore_errors=True)

    print("✅ Cleanup complete: All PDFs moved to the extracted directory.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract PDFs from a zip file in data/raw to data/extracted."
    )
    parser.add_argument(
        "--force-extract",
        action="store_true",
        help="Force extraction even if files exist in the extracted directory",
    )
    args = parser.parse_args()

    extract_zip(force_extract=args.force_extract)