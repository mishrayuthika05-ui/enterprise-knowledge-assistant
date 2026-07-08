from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from app.models.health import HealthResponse
from app.services.file_service import save_file
from app.services.parser_service import extract_text
from app.services.chunk_service import chunk_text
from app.services.embedding_service import (
    generate_embeddings,
    generate_query_embedding,
)
from app.services.vector_store import VectorStore

router = APIRouter()

# FAISS Vector Store
vector_store = VectorStore()


class QuestionRequest(BaseModel):
    question: str


@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="healthy",
        message="Enterprise Knowledge Assistant API is running successfully"
    )


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Save uploaded file
    file_path = save_file(file)

    # Extract text
    text = extract_text(file_path)

    # Split into chunks
    chunks = chunk_text(text)

    # Generate embeddings
    embeddings = generate_embeddings(chunks)

    # Store in FAISS
    vector_store.add_embeddings(embeddings, chunks)

    return {
        "filename": file.filename,
        "characters": len(text),
        "chunks": len(chunks),
        "status": "Document indexed successfully"
    }


@router.post("/ask")
def ask_question(request: QuestionRequest):
    query_embedding = generate_query_embedding(request.question)

    results = vector_store.search(query_embedding, k=3)

    return {
        "question": request.question,
        "results": results
    }