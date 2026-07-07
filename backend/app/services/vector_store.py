import faiss
import numpy as np


class VectorStore:
    def __init__(self):
        self.index = None
        self.chunks = []

    def add_embeddings(self, embeddings, chunks):
        embeddings = np.array(embeddings).astype("float32")

        if self.index is None:
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings)
        self.chunks.extend(chunks)

    def search(self, query_embedding, k=3):
        query_embedding = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query_embedding, k)

        results = []

        for idx in indices[0]:
            if idx < len(self.chunks):
                results.append(self.chunks[idx])

        return results