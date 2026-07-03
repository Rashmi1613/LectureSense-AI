from fastapi import FastAPI
from api.upload import router as upload_router

app = FastAPI(
    title="LectureSense AI",
    description="Multimodal Lecture Understanding System",
    version="1.0.0"
)

app.include_router(upload_router)


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