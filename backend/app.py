from fastapi import FastAPI, HTTPException
from models.schemas import AnalyzeRequest, AnalyzeResponse
from extractors.link_analyzer import analyze_link
from utils.helpers import is_valid_url

app = FastAPI(title="DropLine API", version="0.1.0")

@app.get("/")
def root():
    return {"message": "DropLine API is running"}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    if not is_valid_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    result = analyze_link(request.url)
    return result