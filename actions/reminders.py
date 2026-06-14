"""
Připomínky - verze pro Windows.

Apple Reminders fungují pouze v macOS.
Ve Windows se otevře Microsoft To Do nebo Google Tasks.
"""

from __future__ import annotations

import webbrowser


def get_reminders(query: str = "upcoming", limit: int = 8, list_name: str = "") -> str:
    webbrowser.open("https://to-do.microsoft.com/tasks")
    return (
        "Apple Reminders nejsou na této platformě podporovány. "
        "V prohlížeči byl otevřen Microsoft To Do."
    )


def add_reminder(
    title: str,
    due_iso: str = "",
    notes: str = "",
    list_name: str = "",
    priority: str = "",
    all_day: bool = False,
) -> str:
    webbrowser.open("https://to-do.microsoft.com/tasks")
    return (
        "Apple Reminders nejsou na této platformě podporovány. "
        f"V prohlížeči byl otevřen Microsoft To Do, kde lze přidat připomínku '{title}'."
    )
