import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="LectureSense AI",
    page_icon="📚",
    layout="wide"
)

st.title("📚 LectureSense AI")

st.write(
    "Generate lecture notes, summaries, flashcards and quizzes from slides, PDFs and audio."
)

# ------------------------------------
# Backend Health Check
# ------------------------------------

try:
    response = requests.get(f"{BACKEND_URL}/health")

    if response.status_code == 200:
        st.success("🟢 Backend Connected")
    else:
        st.error("Backend Offline")

except:
    st.error("Cannot connect to backend")

st.divider()

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

if st.button("🚀 Analyze Lecture"):

    # ---------------------------
    # Upload Slides
    # ---------------------------

    if slides:

        files = [
            (
                "files",
                (
                    slide.name,
                    slide,
                    slide.type
                )
            )
            for slide in slides
        ]

        response = requests.post(
            f"{BACKEND_URL}/upload/slides",
            files=files
        )

        if response.status_code == 200:
            st.success("Slides Uploaded Successfully")

    # ---------------------------
    # Upload PDF
    # ---------------------------

    if pdf:

        response = requests.post(
            f"{BACKEND_URL}/upload/pdf",
            files={
                "file": (
                    pdf.name,
                    pdf,
                    pdf.type
                )
            }
        )

        if response.status_code == 200:
            st.success("PDF Uploaded Successfully")

    # ---------------------------
    # Upload Audio
    # ---------------------------

    if audio:

        response = requests.post(
            f"{BACKEND_URL}/upload/audio",
            files={
                "file": (
                    audio.name,
                    audio,
                    audio.type
                )
            }
        )

        if response.status_code == 200:
            st.success("Audio Uploaded Successfully")