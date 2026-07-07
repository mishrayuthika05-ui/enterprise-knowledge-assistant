from fastapi import APIRouter
from app.models.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="healthy",
        message="Enterprise Knowledge Assistant API is running successfully"
    )