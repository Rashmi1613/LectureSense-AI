from fastapi import APIRouter, HTTPException
import fitz  # PyMuPDF
import tempfile
import os

from database import get_files,get_ocr_results, save_ocr_result
from services.ocr_service import extract_text_from_image

router = APIRouter(
    prefix="/analyze",
    tags=["Analyze"]
)


@router.post("/{lecture_id}")
def analyze_lecture(lecture_id: int):
    cached_results = get_ocr_results(lecture_id)

    if cached_results:

      return {
           "lecture_id": lecture_id,
            "ocr_results": cached_results,
            "cached": True
        } 

    files = get_files(lecture_id)

    if not files:
        raise HTTPException(
            status_code=404,
            detail="Lecture not found."
        )
        

    extracted_text = []

    for file in files:

        file_type = file["file_type"]

        file_path = file["file_path"]

        # -----------------------------------
        # Slides
        # -----------------------------------

        if file_type == "SLIDE":

            text = extract_text_from_image(file_path)# calling the function from ocr_service.py to extract text from image....business logic is in analyze.py and ocr_service.py is just a service to extract text from image
            #saving into database
            save_ocr_result(
                lecture_id,
                file["file_id"],
                 text
             )

            extracted_text.append({
                "source": file["file_name"],
                "text": text
            })

        # -----------------------------------
        # PDF
        # -----------------------------------

        elif file_type == "PDF":

            pdf = fitz.open(file_path)

            for page_number in range(len(pdf)):

                page = pdf.load_page(page_number)

                pix = page.get_pixmap(dpi=300)

                with tempfile.NamedTemporaryFile(
                    suffix=".png",
                    delete=False
                ) as temp:

                    temp_path = temp.name

                pix.save(temp_path)

                text = extract_text_from_image(temp_path)

                extracted_text.append({
                    "source": f"{file['file_name']} - Page {page_number+1}",
                    "text": text
                })

                os.remove(temp_path)

            pdf.close()

    return {
        "lecture_id": lecture_id,
        "ocr_results": extracted_text
    }