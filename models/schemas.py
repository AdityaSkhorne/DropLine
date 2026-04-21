from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class AnalyzeRequest(BaseModel):
    url: str

# New schema for Gemini AI output
class AIAnalysis(BaseModel):
    summary: str
    key_concepts: List[str]
    explanation: str
    suggested_questions: List[str]

class AnalyzeResponse(BaseModel):
    input_url: str
    final_url: Optional[str] = None
    platform: str
    content_type: str
    title: Optional[str] = None
    description: Optional[str] = None
    full_text: Optional[str] = None      # Added for Milestone 2
    analysis: Optional[Dict] = None      # Added for Milestone 3
    status: str
    details: Dict[str, Any] = {}


# ... (keep your existing code above this)

class ChatRequest(BaseModel):
    context_text: str  # The raw text of the article/video
    question: str      # The user's follow-up question

class ChatResponse(BaseModel):
    answer: str
    error: Optional[str] = None
