import os
import io
import zipfile
from features.etl_features.vector_database import VectorDatabase
from features.storage.document_db import DocumentDatabase
from exceptions.storage_exceptions import NoMatchingJudgmentException

UPLOAD_FOLDER = "./data/uploads"

def get_judgments_search(text: str, num_results: int = 3, filters: dict = None) -> io.BytesIO:
    """
    Performs semantic search and returns a zip file of matched judgments.
    """
    vector_db = VectorDatabase()
    result = vector_db.search(query=text, num_results=num_results, filters=filters)

    print(result)

    if not result["matches"]:
        raise NoMatchingJudgmentException()

    # Get filenames from metadata
    ids = list({
        match["metadata"].get("id") for match in result["matches"]
        if match["metadata"].get("id")
    })

    if not ids:
        raise NoMatchingJudgmentException()
    
    filenames = DocumentDatabase().get_filenames_by_ids(ids)

    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename in filenames:
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.exists(file_path):
                zf.write(file_path, arcname=filename)

    memory_file.seek(0)
    return memory_file