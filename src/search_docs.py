import os

def search_text_documents(folder_path, search_term):
    """
    Searches for a term in all text files within a folder and prints matches.
    :param folder_path: Path to the folder containing text files.
    :param search_term: Term to search for.
    """
    if not os.path.exists(folder_path):
        print("Folder not found!")
        return
    
    search_term = search_term.lower()
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # Only process .txt files
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                text = ""
                for line in enumerate(file, start=1):
                    text += line
                if search_term in text:
                        print(f"Match found in {filename}")

if __name__ == "__main__":
    folder = input("Enter folder path: ")
    term = input("Enter search term: ")
    search_text_documents(folder, term)
