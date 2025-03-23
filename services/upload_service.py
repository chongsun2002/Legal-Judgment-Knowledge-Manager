from features.storage.save_pdf import save_pdf
from features.etl_features.process_pdf import get_pdf_text, extract_metadata, preprocess_text, normalize_filename
from features.etl_features.vector_database import VectorDatabase
from features.storage.document_db import DocumentDatabase
import io
import uuid

def upload_file(file):
    # 1. Save the file into the storage
    save_pdf(file)
    filename = normalize_filename(file.filename)

    # 2. Extract the metadata fields
    pdf_file_as_bytes = file.read()
    pdf_file_as_buffer = io.BytesIO(pdf_file_as_bytes)
    text = get_pdf_text(pdf_file_as_buffer)
    metadata = extract_metadata(text, filename)

    # 3. Preprocess the text
    processed_text = preprocess_text(text, metadata)

    # 4. Generate and upload the embeddings
    # We also generate a UUID for the judgement which will be returned.
    judgment_id = str(uuid.uuid4())
    VectorDatabase().add_document(judgment_id, processed_text, {})
    DocumentDatabase().insert_document(
        judgment_id,
        metadata["case_name"],
        metadata["year"],
        metadata["citation"], 
        metadata["parties"],
        filename)

    return judgment_id

