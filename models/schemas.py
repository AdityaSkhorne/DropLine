from pydantic import BaseModel
from typing import Optional, Dict, Any

class AnalyzeRequest(BaseModel):
    url: str

class AnalyzeResponse(BaseModel):
    input_url: str
    final_url: Optional[str] = None
    platform: str
    content_type: str
    title: Optional[str] = None
    description: Optional[str] = None
    status: str
    details: Dict[str, Any] = {}