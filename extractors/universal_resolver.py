import asyncio
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

MEDIA_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".bmp",
    ".svg",
    ".pdf",
}


def is_direct_media(url: str) -> bool:
    lowered = url.lower().split("?")[0]
    return any(lowered.endswith(ext) for ext in MEDIA_EXTENSIONS)


async def _request_with_retry(
    client: httpx.AsyncClient,
    url: str,
    *,
    max_retries: int = 3,
) -> httpx.Response:
    last_response: Optional[httpx.Response] = None

    for attempt in range(max_retries):
        response = await client.get(url)
        last_response = response

        if response.status_code not in {429, 503}:
            response.raise_for_status()
            return response

        if attempt < max_retries - 1:
            await asyncio.sleep(3)

    if last_response is None:
        raise RuntimeError("No response returned while requesting URL")

    last_response.raise_for_status()
    return last_response


async def resolve_to_direct_link(url: str) -> str:
    async with httpx.AsyncClient(
        follow_redirects=True,
        headers=BROWSER_HEADERS,
        timeout=20.0,
    ) as client:
        response = await _request_with_retry(client, url)
        return str(response.url)


async def extract_hidden_destination(url: str) -> Optional[str]:
    async with httpx.AsyncClient(
        follow_redirects=True,
        headers=BROWSER_HEADERS,
        timeout=20.0,
    ) as client:
        response = await _request_with_retry(client, url)

    soup = BeautifulSoup(response.text, "html.parser")

    candidate_meta = [
        ("meta", {"property": "og:image"}),
        ("meta", {"property": "og:url"}),
        ("meta", {"name": "twitter:image"}),
        ("link", {"rel": "image_src"}),
    ]

    for tag_name, attrs in candidate_meta:
        tag = soup.find(tag_name, attrs=attrs)
        if not tag:
            continue
        value = tag.get("content") or tag.get("href")
        if value:
            return urljoin(str(response.url), value)

    best_src = None
    best_area = -1
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or img.get("data-original")
        if not src:
            continue

        width = int(img.get("width", 0) or 0)
        height = int(img.get("height", 0) or 0)
        area = width * height

        if area > best_area:
            best_area = area
            best_src = src

    if best_src:
        return urljoin(str(response.url), best_src)

    return None


async def resolve_universal(url: str) -> Dict[str, Any]:
    final_url = await resolve_to_direct_link(url)
    resolved_url = final_url

    if not is_direct_media(final_url):
        hidden_destination = await extract_hidden_destination(final_url)
        if hidden_destination:
            resolved_url = await resolve_to_direct_link(hidden_destination)

    is_media_type = is_direct_media(resolved_url)

    raw_data_stream: Optional[bytes] = None
    if is_media_type:
        async with httpx.AsyncClient(
            follow_redirects=True,
            headers=BROWSER_HEADERS,
            timeout=20.0,
        ) as client:
            response = await _request_with_retry(client, resolved_url)
            raw_data_stream = response.content

    return {
        "final_url": resolved_url,
        "is_media_type": is_media_type,
        "raw_data_stream": raw_data_stream,
    }
