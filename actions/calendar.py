"""
Kalendář - verze pro Windows.

Apple Calendar a EventKit fungují pouze v macOS.
Ve Windows se otevře Kalendář Google, Outlook nebo Kalendář Windows.
"""

from __future__ import annotations

import webbrowser


def _open_google_calendar():
    webbrowser.open("https://calendar.google.com")


def get_calendar_events(query: str = "today", limit: int = 6) -> str:
    _open_google_calendar()
    return (
        "Apple Calendar není na této platformě podporován. "
        "V prohlížeči byl otevřen Kalendář Google. "
        "Pokud používáte Outlook, lze otevřít adresu 'outlookcal:'."
    )


def add_calendar_event(
    title: str,
    start_iso: str,
    end_iso: str = "",
    notes: str = "",
    location: str = "",
    calendar_name: str = "",
    all_day: bool = False,
) -> str:
    # URL pro rychlé přidání události do Kalendáře Google.
    import urllib.parse
    params = {"text": title}
    if start_iso:
        date_part = start_iso.replace(":", "").replace("-", "").split("T")[0]
        time_part = start_iso.split("T")[1].replace(":", "")[:4] if "T" in start_iso else ""
        if time_part:
            params["dates"] = f"{date_part}T{time_part}00/{date_part}T{time_part}00"
        else:
            params["dates"] = f"{date_part}/{date_part}"
    if location:
        params["location"] = location
    if notes:
        params["details"] = notes
    url = "https://calendar.google.com/calendar/render?action=TEMPLATE&" + urllib.parse.urlencode(params)
    webbrowser.open(url)
    return (
        "Apple Calendar není na této platformě podporován. "
        f"V prohlížeči bylo otevřeno vytvoření události '{title}' v Kalendáři Google."
    )


def delete_calendar_event(
    title: str,
    start_iso: str = "",
    calendar_name: str = "",
    delete_all_matches: bool = False,
) -> str:
    _open_google_calendar()
    return (
        "Apple Calendar není na této platformě podporován. "
        "V prohlížeči byl otevřen Kalendář Google, kde lze událost odstranit."
    )
