import os
import io
import zipfile
from features.storage.document_db import DocumentDatabase
from exceptions.storage_exceptions import JudgmentNotFoundException, NoMatchingJudgmentException

UPLOAD_FOLDER = "./data/uploads"

def get_judgments():
    memory_file = io.BytesIO()

    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                zf.write(file_path, arcname=filename)

    memory_file.seek(0)
    return memory_file

def get_judgments_id(id: str) -> str:
    documents = DocumentDatabase().search_by_fields({"id": id})
    if len(documents) == 0:
        raise JudgmentNotFoundException()
    
    filename = documents[0]["filename"]

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        raise JudgmentNotFoundException()

    return file_path

def get_judgments_metadata(metadata: dict):
    documents = DocumentDatabase().search_by_fields(metadata)
    if len(documents) == 0:
        raise NoMatchingJudgmentException()

    filenames = [doc["filename"] for doc in documents]

    memory_file = io.BytesIO()

    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename in filenames:
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.exists(file_path):
                zf.write(file_path, arcname=filename)

    memory_file.seek(0)
    return memory_file