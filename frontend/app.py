import streamlit as st
import requests

st.set_page_config(
    page_title="LectureSense AI",
    page_icon="📚",
    layout="wide"
)

st.title("📚 LectureSense AI")

st.markdown(
    """
    ### Multimodal Lecture Understanding & Intelligent Study Companion

    Upload lecture slides, PDFs and audio recordings to automatically generate:

    - 📝 Lecture Notes
    - 📄 Summary
    - 🎴 Flashcards
    - ❓ Practice Quiz
    """
)

# -------------------------------
# Backend Health Check
# -------------------------------

try:
    response = requests.get("http://127.0.0.1:8000/health")

    if response.status_code == 200:
        st.success("🟢 Backend Connected")

    else:
        st.error("🔴 Backend Offline")

except:
    st.error("🔴 Cannot connect to backend")


st.divider()

st.subheader("Upload Files")

slides = st.file_uploader(
    "Upload Lecture Slides",
    type=["jpg", "jpeg", "png", "pdf"],
    accept_multiple_files=True
)

pdf = st.file_uploader(
    "Upload Lecture Notes PDF",
    type=["pdf"]
)

audio = st.file_uploader(
    "Upload Lecture Audio",
    type=["mp3", "wav", "m4a"]
)

analyze = st.button("🚀 Analyze Lecture")

if analyze:
    st.info("Analysis pipeline will be implemented in the next milestone.")