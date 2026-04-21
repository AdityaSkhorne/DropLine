from fastapi import FastAPI, HTTPException
from models.schemas import AnalyzeRequest, AnalyzeResponse
from extractors.link_analyzer import analyze_link, fetch_full_content, fetch_youtube_transcript
from models.schemas import AnalyzeRequest, AnalyzeResponse, ChatRequest, ChatResponse
from models.ai_engine import generate_teaching_insights, chat_with_document
from utils.helpers import is_valid_url

app = FastAPI(title="DropLine API", version="0.2.0")


@app.get("/")
def root():
    return {"message": "DropLine API is running with AI capabilities"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    if not is_valid_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    # Step 1: Base Analysis (Title, Metadata, Platform)
    result = analyze_link(request.url)
    
    # Defaults for new fields
    result["full_text"] = None
    result["analysis"] = None

    # Step 2: Extract text based on the platform
    full_text = None
    
    if result["content_type"] == "webpage":
        full_text = fetch_full_content(result["final_url"])
    elif result["platform"] == "youtube":
        full_text = fetch_youtube_transcript(result["final_url"])
        
    if full_text:
        result["full_text"] = full_text
        
        # Step 3: Send to Gemini for Teaching Mode
        ai_insights = generate_teaching_insights(full_text)
        if ai_insights:
            result["analysis"] = ai_insights
        else:
            result["details"]["ai_status"] = "AI generation failed or text too short."
    else:
        result["details"]["extraction_status"] = "Could not extract text or transcript from this link."

    return result
