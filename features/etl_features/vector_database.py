import chromadb
from chromadb.config import Settings
from .generate_embeddings import generate_embeddings, generate_query_embedding, generate_dummy_embedding

# Singleton class VectorDatabase to ensure multiple instantiations do not happen
class VectorDatabase:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance
    
    def _init(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection("judgments")


    def add_document(self, doc_id: str, text: str, metadata: dict):
        chunked_text, embeddings = generate_embeddings(text)
        ids = [f"{doc_id}_{i}" for i in range(len(embeddings))]
        self.collection.add(
            ids=ids,
            documents=chunked_text,
            embeddings=embeddings,
            metadatas = [{**metadata, "id": doc_id}] * len(chunked_text)
        )
        return

    def search(self, query: str, num_results: int = 3, filters: dict = None):
        query_embedding = generate_query_embedding(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=num_results,
            where=filters
        )

        return {
            "matches": [
                {
                    "id": id_,
                    "document": doc,
                    "score": score,
                    "metadata": meta
                }
                for id_, doc, score, meta in zip(
                    results["ids"][0],
                    results["documents"][0],
                    results["distances"][0],
                    results["metadatas"][0]
                )
            ]
        }