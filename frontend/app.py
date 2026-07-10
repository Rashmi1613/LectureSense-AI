import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="LectureSense AI",
    page_icon="📚",
    layout="wide"
)

# ---------------------------------------------------
# Initialize Session State
# ---------------------------------------------------

if "lecture_id" not in st.session_state:
    st.session_state["lecture_id"] = None

# ---------------------------------------------------
# Title
# ---------------------------------------------------

st.title("📚 LectureSense AI")

st.markdown("""
### Multimodal Lecture Understanding & Intelligent Study Companion

Upload any combination of:

- 📊 Lecture Slides
- 📄 Lecture PDF
- 🎤 Lecture Audio

Generate:

- 📝 Notes
- 📚 Summary
- 🎴 Flashcards
- ❓ Quiz
""")

# ---------------------------------------------------
# Backend Health Check
# ---------------------------------------------------

try:

    response = requests.get(f"{BACKEND_URL}/health")

    if response.status_code == 200:
        st.success("🟢 Backend Connected")

    else:
        st.error("🔴 Backend Offline")

except Exception:

    st.error("🔴 Cannot connect to backend")

st.divider()

# ---------------------------------------------------
# Upload Section
# ---------------------------------------------------

st.header("📤 Upload Lecture")

lecture_name = st.text_input(
    "Lecture Name"
)

slides = st.file_uploader(
    "Upload Lecture Slides",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

pdf = st.file_uploader(
    "Upload Lecture PDF",
    type=["pdf"]
)

audio = st.file_uploader(
    "Upload Lecture Audio",
    type=["mp3", "wav", "m4a"]
)

# ---------------------------------------------------
# Upload Button
# ---------------------------------------------------

if st.button("🚀 Process Lecture"):

    if lecture_name.strip() == "":
        st.warning("Please enter a lecture name.")
        st.stop()

    if not slides and pdf is None and audio is None:
        st.warning("Please upload at least one lecture resource.")
        st.stop()

    files = []

    # -------------------------
    # Slides
    # -------------------------

    if slides:

        for slide in slides:

            files.append(
                (
                    "slides",
                    (
                        slide.name,
                        slide,
                        slide.type
                    )
                )
            )

    # -------------------------
    # PDF
    # -------------------------

    if pdf:

        files.append(
            (
                "pdf",
                (
                    pdf.name,
                    pdf,
                    pdf.type
                )
            )
        )

    # -------------------------
    # Audio
    # -------------------------

    if audio:

        files.append(
            (
                "audio",
                (
                    audio.name,
                    audio,
                    audio.type
                )
            )
        )

    data = {
        "lecture_name": lecture_name
    }

    with st.spinner("Uploading lecture..."):

        response = requests.post(
            f"{BACKEND_URL}/upload",
            data=data,
            files=files
        )

    if response.status_code == 200:

        result = response.json()

        st.success("✅ Lecture Uploaded Successfully!")

        st.session_state["lecture_id"] = result["lecture_id"]

        st.success(
            f"Lecture ID: {result['lecture_id']}"
        )

    else:

        st.error("Upload Failed")

        st.code(response.text)

# ---------------------------------------------------
# Analyze Section
# ---------------------------------------------------

st.divider()

st.header("🔍 Analyze Lecture")

if st.session_state["lecture_id"] is None:

    st.info("Upload a lecture first.")

else:

    st.success(
        f"Current Lecture ID : {st.session_state['lecture_id']}"
    )

    if st.button("Analyze Lecture"):

        with st.spinner("Running OCR..."):

            response = requests.post(
                f"{BACKEND_URL}/analyze/{st.session_state['lecture_id']}"
            )

        if response.status_code == 200:

            result = response.json()

            st.success("OCR Completed Successfully!")

            st.divider()

            st.header("📄 Extracted Text")

            for item in result["ocr_results"]:

                st.subheader(item["source"])

                st.text_area(
                    label="",
                    value=item["text"],
                    height=250
                )

        else:

            st.error("Analysis Failed")

            st.code(response.text)