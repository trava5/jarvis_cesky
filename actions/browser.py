"""Ovládání prohlížeče pomocí modulu webbrowser ve Windows."""

import re
import subprocess
import urllib.parse
import webbrowser

import requests

_VIDEO_ID_RE = re.compile(r'"videoId":"([A-Za-z0-9_-]{11})"')


def _open(url: str) -> None:
    webbrowser.open(url)


def _find_first_youtube_video(query: str) -> str | None:
    encoded = urllib.parse.quote_plus(query)
    response = requests.get(
        f"https://www.youtube.com/results?search_query={encoded}",
        headers={"User-Agent": "JARVIS/1.0"},
        timeout=10,
    )
    response.raise_for_status()

    seen: set[str] = set()
    for video_id in _VIDEO_ID_RE.findall(response.text):
        if video_id not in seen:
            seen.add(video_id)
            return video_id
    return None


def browser_control(action: str, url: str = None, query: str = None) -> str:
    if action == "open_url":
        if not url:
            return "Nebyla zadána URL adresa."
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        _open(url)
        return f"Otevřeno: {url}"

    elif action == "search":
        if not query:
            return "Nebyl zadán vyhledávací dotaz."
        encoded = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded}"
        _open(search_url)
        return f"Byly otevřeny výsledky vyhledávání pro dotaz '{query}'."

    elif action in ("play_youtube", "youtube_play", "play_music"):
        if not query:
            return "Nebyl zadán vyhledávací dotaz pro YouTube."

        try:
            video_id = _find_first_youtube_video(query)
        except Exception as exc:
            encoded = urllib.parse.quote(query)
            fallback_url = f"https://www.youtube.com/results?search_query={encoded}"
            _open(fallback_url)
            return (
                f"První výsledek YouTube se nepodařilo načíst ({exc}). "
                f"Byly otevřeny výsledky vyhledávání pro: {query}"
            )

        if not video_id:
            encoded = urllib.parse.quote(query)
            fallback_url = f"https://www.youtube.com/results?search_query={encoded}"
            _open(fallback_url)
            return f"Nebylo nalezeno přímé video YouTube. Byly otevřeny výsledky pro: {query}"

        watch_url = f"https://www.youtube.com/watch?v={video_id}&autoplay=1"
        _open(watch_url)
        return f"Přehrávám na YouTube: {query}"

    return f"Neznámá akce: {action}"
