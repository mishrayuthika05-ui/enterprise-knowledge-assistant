from fastapi import APIRouter, UploadFile, File

from app.models.health import HealthResponse
from app.services.file_service import save_file
from app.services.parser_service import extract_text

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="healthy",
        message="Enterprise Knowledge Assistant API is running successfully"
    )


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Save uploaded file
    saved_path = save_file(file)

    # Extract text from saved file
    extracted_text = extract_text(saved_path)

    return {
        "success": True,
        "filename": file.filename,
        "saved_path": saved_path,
        "characters": len(extracted_text),
        "preview": extracted_text[:500]
    }