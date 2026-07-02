from fastapi import FastAPI

app = FastAPI(
    title="LectureSense AI",
    description="Multimodal Lecture Understanding and Intelligent Study Companion",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "LectureSense AI Backend Running 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }