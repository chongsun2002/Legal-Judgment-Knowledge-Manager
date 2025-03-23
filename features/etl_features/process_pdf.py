import fitz
import re
import os
from werkzeug.datastructures import FileStorage

# Removes all newlines from text and replaces them with whitespace.
# If there are more than 1 whitespace, converts it to 1 whitespace instead
def _normalize_whitespaces(text: str) -> str:
    return ' '.join(text.split())

def normalize_filename(filename: str) -> str:
    base = os.path.basename(filename)  # remove path
    if not base.lower().endswith('.pdf'):
        base += ".pdf"
    return base

# Gets all the text in the pdf as a single string
def get_pdf_text(file) -> str:
    doc = fitz.open(stream=file, filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    return text

def extract_metadata(text: str, filename: str) -> dict:
    metadata = {
        "file_name": filename
    }
    
    text = _normalize_whitespaces(text)

    # Case name
    case_match = re.search(r'([A-Z][\w\s,.\'()&\-]+?)\s+v(?:s)?\.?\s+([A-Z][\w\s,.\'()&\-]+)', text)
    metadata["case_name"] = case_match.group().strip() if case_match else None

    # Citation
    citation_match = re.search(r'\[\d{4}\]\s+[A-Z]{2,6}\s+\d+', text)
    metadata["citation"] = citation_match.group().strip() if citation_match else None

    # Year
    year_match = re.search(r'\[(\d{4})\]', metadata.get("citation", ""))
    metadata["year"] = int(year_match.group(1)) if year_match else None

    # Parties
    if metadata.get("case_name"):
        parties = metadata["case_name"].split(" v ")
        parties_as_string = [p.strip().lower() for p in parties]
        metadata["parties"] = " | ".join(parties_as_string)

    return metadata

def _remove_metadata_from_text(text: str, metadata: dict) -> str:
    clean_text = text

    if metadata.get("case_name"):
        pattern = re.escape(metadata["case_name"])
        clean_text = re.sub(pattern, '', clean_text, flags=re.IGNORECASE)

    if metadata.get("citation"):
        pattern = re.escape(metadata["citation"])
        clean_text = re.sub(pattern, '', clean_text, flags=re.IGNORECASE)

    if metadata.get("year"):
        pattern = r'\b{}\b'.format(metadata["year"])
        clean_text = re.sub(pattern, '', clean_text)

    return clean_text

def _remove_index_markers(text: str) -> str:
    index_marker_patterns = r'\(\s*([a-zA-Z]|[ivxIVX]+)\s*\)'
    return re.sub(index_marker_patterns, '', text)

def preprocess_text(text: str, metadata: dict) -> str:
    text = _normalize_whitespaces(text)
    text = _remove_metadata_from_text(text, metadata)
    text = _remove_index_markers(text)
    return text
