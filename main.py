from fastapi import FastAPI

app = FastAPI(
    title = "Bookmark API",
    description = "First REST API - Phase 1",
    version= "0.1.0",
)

@app.get("/")
def home():
    return {"message": "Bookmark API is running"}
@app.get("/health")
def health():
    return {"status": "ok"}