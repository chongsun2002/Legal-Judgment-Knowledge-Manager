import os
from exceptions.storage_exceptions import DuplicateJudgmentException

UPLOAD_FOLDER = "data/uploads"


def save_pdf(file):
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(filepath):
        raise DuplicateJudgmentException("The file you tried to upload already exists in the knowledge manager!")
    
    file.save(filepath)
    file.stream.seek(0)
