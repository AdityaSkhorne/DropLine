from fastapi import FastAPI, HTTPException

from extractors.link_analyzer import analyze_link
from extractors.universal_resolver import resolve_universal
from models.schemas import AnalyzeRequest, AnalyzeResponse
from utils.helpers import is_valid_url

app = FastAPI(title="DropLine API", version="0.1.0")


@app.get("/")
def root():
    return {"message": "DropLine API is running"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    if not is_valid_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    resolution = await resolve_universal(request.url)
    result = analyze_link(resolution["final_url"])

    result["input_url"] = request.url
    result.setdefault("details", {})["resolution"] = {
        "final_url": resolution["final_url"],
        "is_media_type": resolution["is_media_type"],
        "raw_data_stream_size": len(resolution["raw_data_stream"])
        if resolution["raw_data_stream"]
        else 0,
    }

    return result
