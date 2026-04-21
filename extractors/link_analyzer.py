import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import trafilatura
from utils.helpers import clean_text
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import parse_qs

def expand_url(url: str) -> str:
    try:
        r = requests.get(url, allow_redirects=True, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        return r.url
    except Exception:
        return url

def detect_platform(url: str) -> str:
    netloc = urlparse(url).netloc.lower()
    if "youtube.com" in netloc or "youtu.be" in netloc: return "youtube"
    if "google.com" in netloc or "googleusercontent.com" in netloc: return "google"
    if "github.com" in netloc: return "github"
    if "pdf" in url.lower(): return "pdf"
    return "web"

def detect_content_type(url: str) -> str:
    lowered = url.lower()
    if "youtube.com" in lowered or "youtu.be" in lowered: return "video"
    if lowered.endswith(".pdf"): return "pdf"
    if any(lowered.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]): return "image"
    return "webpage"

def fetch_page_metadata(url: str):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    title = clean_text(soup.title.string) if soup.title and soup.title.string else None
    meta_desc = soup.find("meta", attrs={"name": "description"})
    description = clean_text(meta_desc["content"]) if meta_desc and meta_desc.get("content") else None
    return {"title": title, "description": description, "html_length": len(response.text)}

# NEW FUNCTION: Gets the actual body text of the article
def fetch_full_content(url: str) -> str:
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            return trafilatura.extract(downloaded)
    except Exception as e:
        print(f"Extraction error: {e}")
    return None

def fetch_youtube_transcript(url: str) -> str:
    """Extracts the transcript text from a YouTube video."""
    try:
        # Extract the video ID from the URL
        parsed = urlparse(url)
        video_id = None
        
        if "youtube.com" in parsed.netloc:
            video_id = parse_qs(parsed.query).get('v')
            if video_id: video_id = video_id[0]
        elif "youtu.be" in parsed.netloc:
            video_id = parsed.path.lstrip('/')
            
        if video_id:
            # Download the transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            # Combine all the spoken text into one big paragraph
            full_text = " ".join([segment['text'] for segment in transcript_list])
            return full_text
            
    except Exception as e:
        print(f"YouTube extraction error: {e}")
        
    return None    

def analyze_link(url: str):
    final_url = expand_url(url)
    platform = detect_platform(final_url)
    content_type = detect_content_type(final_url)

    details = {}
    title = description = None
    status = "success"

    try:
        if content_type == "webpage":
            metadata = fetch_page_metadata(final_url)
            title = metadata["title"]
            description = metadata["description"]
            details = metadata
        else:
            details = {"note": f"Detected as {content_type}, metadata extraction will be added later."}
    except Exception as e:
        status = "partial"
        details = {"error": str(e), "note": "Could not fully extract metadata."}

    return {
        "input_url": url,
        "final_url": final_url,
        "platform": platform,
        "content_type": content_type,
        "title": title,
        "description": description,
        "status": status,
        "details": details
    }