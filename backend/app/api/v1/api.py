from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "message": "Enterprise Knowledge Assistant API is running successfully"
    }