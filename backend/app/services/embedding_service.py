from sentence_transformers import SentenceTransformer

# Load embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks: list[str]):
    """
    Convert text chunks into vector embeddings.
    """
    embeddings = model.encode(chunks, convert_to_numpy=True)

    return embeddings


def generate_query_embedding(question: str):
    """
    Convert a user question into an embedding.
    """
    embedding = model.encode(question, convert_to_numpy=True)

    return embedding