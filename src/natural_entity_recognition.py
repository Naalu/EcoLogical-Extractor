import os

import en_core_web_lg
from tqdm import tqdm  # Progress bar

# Define paths relative to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "text_output")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "ner_output")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def read_text_file_to_string(file_path):
    """
    Reads the content of a text file into a single string.

    Args:
        file_path (str): The path to the text file.

    Returns:
        str: The content of the file as a single string, or None if an error occurs.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()
            return file_content
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def ner_all_txts(force_extract=False):
    """
    Extract NER output from all TXTs in the text_output folder and save them as text files.

    Args:
        force_extract (bool): If True, reprocess all TXTs even if the text files already exist. Defaults to False.

    - Skips already processed TXTs unless force_extract=True.
    - Provides clear console output on which files are processed vs. skipped.
    """
    if not os.path.exists(DATA_DIR) or not any(
        f.endswith(".txt") for f in os.listdir(DATA_DIR)
    ):
        print("❌ No TXTs found in text_output directory. Run pdf_text_extraction.py and mp3_text_extraction.py first.")
        return

    txt_files = [
        f
        for f in os.listdir(DATA_DIR)
        # Filter out hidden files and non-TXT files
        if f.lower().endswith(".txt") and not f.startswith("._")
    ]
    num_files = len(txt_files)
    skipped = 0

    if num_files == 0:
        print("❌ No valid TXTs found. Hidden files may have been filtered.")
        return

    print(f"📂 Processing {num_files} TXTs...\n")

    nlp = en_core_web_lg.load()

    for filename in tqdm(txt_files, desc="Parsing TXTs", unit="file"):
        txt_path = os.path.join(DATA_DIR, filename)
        output_filename = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        # Skip if text file already exists (unless force_extract is set)
        if os.path.exists(output_path) and not force_extract:
            continue  # Skip without printing, since tqdm provides progress feedback

        text = read_text_file_to_string(txt_path)

        # Skip saving if extraction failed
        if text is None or len(text) > 1000000:
            skipped += 1
            continue

        # Save text to output file
        with open(output_path, "w", encoding="utf-8") as f:
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ in ["GPE", "LOC"]:
                    f.write(f"Text: {ent.text}, Start: {ent.start_char}, End: {ent.end_char}, Label: {ent.label_}\n")

    print("\n✅ Natural Entity Recognition complete! All available TXTs have been processed.")
    print(f"Number of Skipped Files (no text or too long): {skipped}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract NER output from TXTs in the text_output folder and save as text files."
    )
    parser.add_argument(
        "--force-extract",
        action="store_true",
        help="Force extraction even if text files already exist",
    )
    args = parser.parse_args()

    ner_all_txts(force_extract=args.force_extract)