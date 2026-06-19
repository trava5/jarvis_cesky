"""Otevirani aplikaci pomoci os.startfile nebo prikazu start ve Windows."""

import os
import shutil
import subprocess


APP_ALIASES = {
    "edge": "msedge",
    "microsoft edge": "msedge",
    "chrome": "chrome",
    "google chrome": "chrome",
    "firefox": "firefox",
    "terminal": "cmd",
    "terminál": "cmd",
    "cmd": "cmd",
    "powershell": "powershell",
    "explorer": "explorer",
    "file explorer": "explorer",
    "průzkumník": "explorer",
    "průzkumník souborů": "explorer",
    "spotify": "Spotify",
    "vscode": "code",
    "vs code": "code",
    "code": "code",
    "discord": "Discord",
    "slack": "Slack",
    "whatsapp": "WhatsApp",
    "telegram": "Telegram",
    "zoom": "Zoom",
    "notepad": "notepad",
    "poznámkový blok": "notepad",
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "calculator": "calc",
    "kalkulačka": "calc",
    "task manager": "taskmgr",
    "správce úloh": "taskmgr",
    "settings": "ms-settings:",
    "nastavení": "ms-settings:",
    "paint": "mspaint",
    "wordpad": "wordpad",
    "snipping tool": "SnippingTool",
    "výstřižky": "SnippingTool",
    "photos": "ms-photos:",
    "fotky": "ms-photos:",
    "maps": "bingmaps:",
    "mapy": "bingmaps:",
    "mail": "outlookmail:",
    "pošta": "outlookmail:",
    "calendar": "outlookcal:",
    "kalendář": "outlookcal:",
    "store": "ms-windows-store:",
    "obchod": "ms-windows-store:",
    "music": "mswindowsmusic:",
    "hudba": "mswindowsmusic:",
    "notion": "Notion",
}

URI_SCHEMES = {
    "ms-settings:",
    "ms-photos:",
    "bingmaps:",
    "outlookmail:",
    "outlookcal:",
    "ms-windows-store:",
    "mswindowsmusic:",
}


def open_app(app_name: str) -> str:
    if not app_name:
        return "Nebyl zadán název aplikace."

    normalized = app_name.lower().strip()
    resolved = APP_ALIASES.get(normalized, app_name)

    # Schéma URI, například ms-settings:.
    if any(resolved.startswith(scheme) for scheme in URI_SCHEMES):
        try:
            os.startfile(resolved)
            return f"Aplikace {app_name} byla otevřena."
        except Exception as e:
            return f"Aplikaci '{app_name}' se nepodařilo otevřít: {e}"

    # Spustitelný soubor dostupný v PATH.
    exe_path = shutil.which(resolved)
    if exe_path:
        try:
            subprocess.Popen([exe_path], shell=False)
            return f"Aplikace {app_name} byla otevřena."
        except Exception as e:
            return f"Aplikaci '{app_name}' se nepodařilo otevřít: {e}"

    # Příkaz start přes shell Windows.
    try:
        result = subprocess.run(
            f'start "" "{resolved}"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return f"Aplikace {app_name} byla otevřena."
    except Exception:
        pass

    # Poslední možnost: os.startfile.
    try:
        os.startfile(resolved)
        return f"Aplikace {app_name} byla otevřena."
    except Exception as e:
        return f"Aplikaci '{app_name}' se nepodařilo najít nebo otevřít: {e}"
