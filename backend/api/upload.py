from fastapi import APIRouter, UploadFile, File, Form
from pathlib import Path
import shutil
from typing import List, Optional

from database import create_lecture, add_file

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
async def upload_lecture(
    lecture_name: str = Form(...),
    slides: Optional[List[UploadFile]] = File(None),
    pdf: Optional[UploadFile] = File(None),
    audio: Optional[UploadFile] = File(None),
):
    if not slides and pdf is None and audio is None:
        return {
            "message": "Please upload at least one file."
        }

    lecture_id = create_lecture(lecture_name)

    slides_dir = Path("uploads/slides")
    pdfs_dir = Path("uploads/pdfs")
    audio_dir = Path("uploads/audio")

    slides_dir.mkdir(parents=True, exist_ok=True)
    pdfs_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # Save Slides (if provided)
    # -----------------------------
    if slides:
        for slide in slides:
            destination = slides_dir / slide.filename
            with destination.open("wb") as buffer:
                shutil.copyfileobj(slide.file, buffer)

            add_file(
                lecture_id=lecture_id,
                file_type="SLIDE",
                file_name=slide.filename,
                file_path=str(destination)
            )

    # -----------------------------
    # Save PDF (if provided)
    # -----------------------------
    if pdf:
        pdf_destination = pdfs_dir / pdf.filename
        with pdf_destination.open("wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)

        add_file(
            lecture_id=lecture_id,
            file_type="PDF",
            file_name=pdf.filename,
            file_path=str(pdf_destination)
        )

    # -----------------------------
    # Save Audio (if provided)
    # -----------------------------
    if audio:
        audio_destination = audio_dir / audio.filename
        with audio_destination.open("wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        add_file(
            lecture_id=lecture_id,
            file_type="AUDIO",
            file_name=audio.filename,
            file_path=str(audio_destination)
        )

    return {
        "message": "Lecture uploaded successfully",
        "lecture_id": lecture_id
    }