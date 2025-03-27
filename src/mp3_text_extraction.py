import os

import whisper
from tqdm import tqdm  # Progress bar

# Define paths relative to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "extracted")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "text_output")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_text_from_mp3(mp3_path, model):
    """
    Extract text from a given MP3 file using Whisper model.

    Args:
        mp3_path (str): The path to the MP3 file.
        model (whisper_obj): The model used to transcribe the MP3 file.

    Returns:
        str: The extracted text from the MP3, or None if an error occurs.
    """
    try:
        result = model.transcribe(mp3_path)
        return result["text"]
    except Exception as e:
        print(f"❌ Skipping {os.path.basename(mp3_path)} (error: {str(e)})")
        return None
    
def process_all_mp3s(force_extract=False):
    """
    Extract text from all MP3s in the extracted folder and save them as text files.

    Args:
        force_extract (bool): If True, reprocess all MP3s even if the text files already exist. Defaults to False.

    - Skips already processed MP3s unless force_extract=True.
    - Provides clear console output on which files are processed vs. skipped.
    """
    if not os.path.exists(DATA_DIR) or not any(
        f.endswith(".mp3") for f in os.listdir(DATA_DIR)
    ):
        print("❌ No MP3s found in extracted directory. Run extract_data.py first.")
        return

    mp3_files = [
        f
        for f in os.listdir(DATA_DIR)
        # Filter out hidden files and non-PDF files
        if f.lower().endswith(".mp3") and not f.startswith("._")
    ]
    num_files = len(mp3_files)

    if num_files == 0:
        print("❌ No valid MP3s found. Hidden files may have been filtered.")
        return

    print(f"📂 Processing {num_files} MP3s...\n")

    # Load Whisper model
    model = whisper.load_model("turbo")

    for filename in tqdm(mp3_files, desc="Extracting MP3s", unit="file"):
        mp3_path = os.path.join(DATA_DIR, filename)
        output_filename = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        # Skip if text file already exists (unless force_extract is set)
        if os.path.exists(output_path) and not force_extract:
            continue  # Skip without printing, since tqdm provides progress feedback

        text = extract_text_from_mp3(mp3_path, model)

        # Skip saving if extraction failed
        if text is None:
            continue

        # Save text to output file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

    print("\n✅ Extraction complete! All available MP3s have been processed.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract text from MP3s in the extracted folder and save as text files."
    )
    parser.add_argument(
        "--force-extract",
        action="store_true",
        help="Force extraction even if text files already exist",
    )
    args = parser.parse_args()

    process_all_mp3s(force_extract=args.force_extract)