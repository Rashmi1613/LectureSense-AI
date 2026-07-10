from fastapi import FastAPI
from api.upload import router as upload_router
from api.lectures import router as lectures_router
from api.analyze import router as analyze_router
from database import init_db
app = FastAPI(
    title="LectureSense AI",
    description="Multimodal Lecture Understanding System",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    init_db()
app.include_router(upload_router)
app.include_router(lectures_router)
app.include_router(analyze_router)

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