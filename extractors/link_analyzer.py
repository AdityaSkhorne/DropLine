import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from utils.helpers import clean_text

def expand_url(url: str) -> str:
    try:
        r = requests.get(url, allow_redirects=True, timeout=20, headers={
            "User-Agent": "Mozilla/5.0"
        })
        return r.url
    except Exception:
        return url

def detect_platform(url: str) -> str:
    netloc = urlparse(url).netloc.lower()

    if "youtube.com" in netloc or "youtu.be" in netloc:
        return "youtube"
    if "google.com" in netloc or "googleusercontent.com" in netloc:
        return "google"
    if "github.com" in netloc:
        return "github"
    if "pdf" in url.lower():
        return "pdf"
    return "web"

def detect_content_type(url: str) -> str:
    lowered = url.lower()
    if "youtube.com" in lowered or "youtu.be" in lowered:
        return "video"
    if lowered.endswith(".pdf"):
        return "pdf"
    if any(lowered.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]):
        return "image"
    return "webpage"

def fetch_page_metadata(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title = None
    description = None

    if soup.title and soup.title.string:
        title = clean_text(soup.title.string)

    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        description = clean_text(meta_desc["content"])

    return {
        "title": title,
        "description": description,
        "html_length": len(response.text)
    }

def analyze_link(url: str):
    final_url = expand_url(url)
    platform = detect_platform(final_url)
    content_type = detect_content_type(final_url)

    details = {}
    title = None
    description = None
    status = "success"

    try:
        if content_type == "webpage":
            metadata = fetch_page_metadata(final_url)
            title = metadata["title"]
            description = metadata["description"]
            details = metadata
        else:
            details = {
                "note": f"Detected as {content_type}, metadata extraction will be added later."
            }
    except Exception as e:
        status = "partial"
        details = {
            "error": str(e),
            "note": "Could not fully extract metadata from the link."
        }

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