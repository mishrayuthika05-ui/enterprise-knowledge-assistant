from pathlib import Path
from fastapi import UploadFile, HTTPException
import shutil
import os
import uuid

from app.core.constants import ALLOWED_EXTENSIONS, MAX_FILE_SIZE

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def validate_file(file: UploadFile):
    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Only {', '.join(ALLOWED_EXTENSIONS)} files are allowed."
        )

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 10 MB."
        )


def generate_unique_filename(filename: str) -> str:
    unique_id = uuid.uuid4().hex[:8]
    return f"{unique_id}_{filename}"


def save_file(file: UploadFile) -> str:
    validate_file(file)

    unique_filename = generate_unique_filename(file.filename)
    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(file_path)