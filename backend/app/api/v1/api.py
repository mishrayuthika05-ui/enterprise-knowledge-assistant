from fastapi import APIRouter, UploadFile, File

from app.models.health import HealthResponse
from app.services.file_service import save_file
from app.services.parser_service import extract_text
from app.services.chunk_service import chunk_text
from app.services.embedding_service import generate_embeddings
from app.services.vector_store import VectorStore

router = APIRouter()

# FAISS Vector Store (in-memory)
vector_store = VectorStore()


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

    # Store embeddings in FAISS
    vector_store.add_embeddings(embeddings, chunks)

    return {
        "filename": file.filename,
        "characters": len(text),
        "chunks": len(chunks),
        "status": "Document indexed successfully"
    }