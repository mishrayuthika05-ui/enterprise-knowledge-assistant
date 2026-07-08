import faiss
import numpy as np
import os


class VectorStore:
    def __init__(self):
        self.index = None
        self.chunks = []

        # Load existing index if available
        if os.path.exists("faiss_index.index") and os.path.exists("chunks.npy"):
            self.index = faiss.read_index("faiss_index.index")
            self.chunks = np.load("chunks.npy", allow_pickle=True).tolist()

    def add_embeddings(self, embeddings, chunks):
        embeddings = np.array(embeddings).astype("float32")

        if self.index is None:
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings)
        self.chunks.extend(chunks)

        # Save index and chunks
        faiss.write_index(self.index, "faiss_index.index")
        np.save("chunks.npy", np.array(self.chunks, dtype=object))

    def search(self, query_embedding, k=3):
        if self.index is None:
            return []

        query_embedding = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query_embedding, k)

        results = []

        for idx in indices[0]:
            if 0 <= idx < len(self.chunks):
                results.append(self.chunks[idx])

        return results