from paddleocr import PaddleOCR

# --------------------------------------------------------
# Initialize OCR Model (Loads only once)
# --------------------------------------------------------

ocr = PaddleOCR(
    lang="en",
    enable_mkldnn=False
)


# --------------------------------------------------------
# Extract Text From Image
# --------------------------------------------------------

def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image using PaddleOCR.

    Parameters
    ----------
    image_path : str
        Path to the input image.

    Returns
    -------
    str
        Extracted text.
    """

    try:

        results = ocr.predict(image_path)

        extracted_text = []

        for page in results:

            if "rec_texts" in page:

                extracted_text.extend(page["rec_texts"])

        return "\n".join(extracted_text)

    except Exception as e:

        print(f"OCR Error: {e}")

        return ""