"""Tools the agent can call. Kept small, typed and individually testable."""
from __future__ import annotations

import html
import re

import httpx
from langchain_core.tools import tool

MAX_PAGE_CHARS = 4000
USER_AGENT = "briefbot/0.1 (+https://github.com/)"


def clean_html(raw: str) -> str:
    """Strip scripts, styles and tags from HTML and collapse whitespace."""
    raw = re.sub(r"(?is)<(script|style|noscript).*?>.*?</\1>", " ", raw)
    text = re.sub(r"(?s)<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def is_safe_url(url: str) -> bool:
    """Only plain http(s) URLs; refuse local/private hosts (basic SSRF guard)."""
    m = re.match(r"^https?://([^/:?#]+)", url.strip(), re.I)
    if not m:
        return False
    host = m.group(1).lower()
    if host in {"localhost", "0.0.0.0"} or host.endswith(".local") or host.endswith(".internal"):
        return False
    if re.match(r"^(127\.|10\.|192\.168\.|169\.254\.|172\.(1[6-9]|2\d|3[01])\.)", host):
        return False
    return True


@tool
def web_search(query: str, max_results: int = 5) -> str:
    """Search the web. Returns numbered results with title, URL and a snippet."""
    from ddgs import DDGS

    try:
        hits = list(DDGS().text(query, max_results=max_results))
    except Exception as e:  # network or rate-limit problems should not crash the agent
        return f"Search failed: {e}"
    if not hits:
        return "No results."
    return "\n".join(
        f"{i}. {h.get('title', '')}\n   {h.get('href', '')}\n   {h.get('body', '')}"
        for i, h in enumerate(hits, 1)
    )


@tool
def fetch_page(url: str) -> str:
    """Download a web page and return its readable text (truncated)."""
    if not is_safe_url(url):
        return "Refused: only public http(s) URLs are allowed."
    try:
        r = httpx.get(url, timeout=15, follow_redirects=True, headers={"User-Agent": USER_AGENT})
        r.raise_for_status()
    except Exception as e:
        return f"Fetch failed: {e}"
    return clean_html(r.text)[:MAX_PAGE_CHARS]


TOOLS = [web_search, fetch_page]