from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil
from typing import List

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

# -----------------------------
# Upload Lecture Slides
# -----------------------------
@router.post("/slides")
async def upload_slides(
    files: List[UploadFile] = File(...)
):
    upload_dir = Path("uploads/slides")
    upload_dir.mkdir(parents=True, exist_ok=True)

    uploaded_files = []

    for file in files:
        destination = upload_dir / file.filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_files.append(file.filename)

    return {
        "message": "Slides uploaded successfully",
        "files": uploaded_files
    }


# -----------------------------
# Upload PDF
# -----------------------------
@router.post("/pdf")
async def upload_pdf(
    file: UploadFile = File(...)
):
    upload_dir = Path("uploads/pdfs")
    upload_dir.mkdir(parents=True, exist_ok=True)

    destination = upload_dir / file.filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "PDF uploaded successfully",
        "file": file.filename
    }


# -----------------------------
# Upload Audio
# -----------------------------
@router.post("/audio")
async def upload_audio(
    file: UploadFile = File(...)
):
    upload_dir = Path("uploads/audio")
    upload_dir.mkdir(parents=True, exist_ok=True)

    destination = upload_dir / file.filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Audio uploaded successfully",
        "file": file.filename
    }