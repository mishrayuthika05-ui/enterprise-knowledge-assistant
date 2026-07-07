from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Enterprise Knowledge Assistant API is Running 🚀"
    }


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "message": "Server is running successfully"
    }