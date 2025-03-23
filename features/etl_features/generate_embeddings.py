from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
embedding_model_vector_dimension = 384

def _chunk_text(text, max_words=200) -> list[str]:
    words = text.split()
    return [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

def generate_embeddings(text):
    chunked_text = _chunk_text(text)
    embeddings = embedding_model.encode(chunked_text).tolist()
    return chunked_text, embeddings

def generate_query_embedding(query: str) -> list[float]:
    return embedding_model.encode([query])[0].tolist()

def generate_dummy_embedding():
    return [[0.0] * 384]