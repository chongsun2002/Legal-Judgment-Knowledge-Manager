import os
from exceptions.storage_exceptions import DuplicateJudgmentException

DATA_ROOT_DIRECTORY = "data"
UPLOADS_FOLDER = "uploads"

def ensure_directories():
    base_data_dir = os.path.join(os.getcwd(), DATA_ROOT_DIRECTORY)
    uploads_dir = os.path.join(base_data_dir, UPLOADS_FOLDER)

    os.makedirs(uploads_dir, exist_ok=True)

def save_pdf(file):
    ensure_directories()
    filename = file.filename
    filepath = os.path.join(DATA_ROOT_DIRECTORY, UPLOADS_FOLDER, filename)

    if os.path.exists(filepath):
        raise DuplicateJudgmentException("The file you tried to upload already exists in the knowledge manager!")
    
    file.save(filepath)
    file.stream.seek(0)
