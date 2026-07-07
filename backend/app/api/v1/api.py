from fastapi import APIRouter, UploadFile, File

from app.models.health import HealthResponse
from app.services.file_service import save_file
from app.services.parser_service import extract_text
from app.services.chunk_service import chunk_text

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="healthy",
        message="Enterprise Knowledge Assistant API is running successfully"
    )


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = save_file(file)

    text = extract_text(file_path)

    chunks = chunk_text(text)

    return {
        "filename": file.filename,
        "characters": len(text),
        "chunks": len(chunks),
        "first_chunk": chunks[0] if chunks else ""
    }