#!/usr/bin/env python3
"""
JARVIS Windows — jádro hlasového asistenta v reálném čase
Vytvořil Alp Ünlü — @alppunlu
Pracovní postup přizpůsobený prostředí Windows
"""

import asyncio
import datetime
import threading
import traceback
import os
import re
from pathlib import Path

import pyaudio  # type: ignore[reportMissingModuleSource]
from google import genai  # type: ignore[reportMissingImports]
from google.genai import types  # type: ignore[reportMissingImports]

from app_config import get_app_config_value
from ui import JarvisUI
from memory.memory_manager import load_memory, update_memory, delete_memory, format_memory_for_prompt
from actions.open_app import open_app
from actions.sys_info  import sys_info
from actions.calendar import get_calendar_events, add_calendar_event, delete_calendar_event
from actions.reminders import get_reminders, add_reminder
from actions.browser   import browser_control
from actions.shell     import shell_run
from actions.whatsapp  import send_whatsapp_message, save_whatsapp_contact
from actions.media     import play_media
from actions.weather   import get_weather_summary
from actions.screen_vision import analyze_screen
from actions.youtube_stats import get_youtube_channel_report
from wakeup_listener import WakeGestureListener

# ── Paths ───────────────────────────────────────────────────────────────────
BASE_DIR        = Path(__file__).resolve().parent
PROMPT_PATH     = BASE_DIR / "core" / "prompt.txt"


CONTROL_TOKEN_RE = re.compile(r"<ctrl\d+>", re.IGNORECASE)

# ── Model ───────────────────────────────────────────────────────────────────
LIVE_MODEL = "models/gemini-2.5-flash-native-audio-latest"

# ── Audio ───────────────────────────────────────────────────────────────────
FORMAT           = pyaudio.paInt16
CHANNELS         = 1
SEND_SAMPLE_RATE = 16000
RECV_SAMPLE_RATE = 24000
CHUNK_SIZE       = 1024
pya              = pyaudio.PyAudio()

# ── Definice nástrojů ───────────────────────────────────────────────────────
TOOL_DECLARATIONS = [
    {
        "name": "open_app",
        "description": "Otevře libovolnou aplikaci ve Windows, například Spotify, Chrome, Terminál, Průzkumník souborů nebo VS Code.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "app_name": {
                    "type": "STRING",
                    "description": "Název aplikace, například 'Spotify', 'Chrome' nebo 'Terminal'"
                }
            },
            "required": ["app_name"]
        }
    },
    {
        "name": "sys_info",
        "description": "Získá systémové informace: stav baterie, CPU, RAM, disk, čas, datum nebo síťové připojení.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "query": {
                    "type": "STRING",
                    "description": "battery | cpu | ram | disk | time | date | network | all"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_weather",
        "description": (
            "Shrne aktuální počasí. Výchozí lokalitou je Praha. "
            "Použij, když se uživatel ptá na počasí, teplotu nebo déšť."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "location": {
                    "type": "STRING",
                    "description": "Město nebo lokalita. Pokud zůstane prázdná, použije se Praha."
                }
            }
        }
    },
    {
        "name": "get_calendar_events",
        "description": (
            "Načte události z Kalendáře Google. "
            "Shrne dnešní či zítřejší události, následující událost nebo nadcházející program. "
            "Použij při dotazu na schůzky, kalendář, agendu, události nebo denní program."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "query": {
                    "type": "STRING",
                    "description": (
                        "today | tomorrow | next | agenda | week nebo přirozený text, například "
                        "'následujících 30 dní', '2 týdny', 'tento měsíc', 'příští měsíc'"
                    )
                },
                "limit": {
                    "type": "NUMBER",
                    "description": "Maximální počet událostí"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "add_calendar_event",
        "description": (
            "Přidá novou událost do Kalendáře Google. "
            "Použij, když chce uživatel vytvořit schůzku, termín nebo jinou událost. "
            "Začátek předej jako skutečné datum a čas; pokud není uveden konec, použije se výchozí délka."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "title": {
                    "type": "STRING",
                    "description": "Název události, například 'Návštěva zubaře'"
                },
                "start_iso": {
                    "type": "STRING",
                    "description": "Datum a čas začátku ve formátu ISO nebo yyyy-MM-dd HH:mm."
                },
                "end_iso": {
                    "type": "STRING",
                    "description": "Volitelné datum a čas konce."
                },
                "location": {
                    "type": "STRING",
                    "description": "Volitelné místo události."
                },
                "notes": {
                    "type": "STRING",
                    "description": "Volitelné poznámky k události."
                },
                "calendar_name": {
                    "type": "STRING",
                    "description": "Volitelný název cílového kalendáře."
                },
                "all_day": {
                    "type": "BOOLEAN",
                    "description": "Hodnota true vytvoří celodenní událost."
                }
            },
            "required": ["title", "start_iso"]
        }
    },
    {
        "name": "delete_calendar_event",
        "description": (
            "Odstraní událost z Kalendáře Google. "
            "Použij, když chce uživatel odstranit schůzku, termín nebo záznam v kalendáři. "
            "Pokud existuje více událostí se stejným názvem, předej skutečné datum a čas začátku."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "title": {
                    "type": "STRING",
                    "description": "Název odstraňované události, například 'Návštěva zubaře'"
                },
                "start_iso": {
                    "type": "STRING",
                    "description": "Volitelné datum a čas pro rozlišení více událostí se stejným názvem."
                },
                "calendar_name": {
                    "type": "STRING",
                    "description": "Volitelný název kalendáře"
                },
                "delete_all_matches": {
                    "type": "BOOLEAN",
                    "description": "Hodnota true odstraní všechny odpovídající události"
                }
            },
            "required": ["title"]
        }
    },
    {
        "name": "get_reminders",
        "description": (
            "Načte připomínky z Microsoft To Do. "
            "Shrne dnešní, nadcházející, zpožděné nebo všechny otevřené připomínky. "
            "Použij při dotazu na připomínky nebo seznam úkolů."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "query": {
                    "type": "STRING",
                    "description": "today | upcoming | overdue | all | next"
                },
                "limit": {
                    "type": "NUMBER",
                    "description": "Maximální počet připomínek"
                },
                "list_name": {
                    "type": "STRING",
                    "description": "Volitelný název konkrétního seznamu připomínek"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "add_reminder",
        "description": (
            "Přidá novou připomínku do Microsoft To Do. "
            "Použij, když uživatel řekne například 'připomeň mi' nebo 'přidej připomínku'. "
            "Relativní čas převeď podle aktuálního data do pole due_iso ve formátu ISO."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "title": {
                    "type": "STRING",
                    "description": "Název připomínky"
                },
                "due_iso": {
                    "type": "STRING",
                    "description": "Volitelné datum a čas, například 2026-04-13T09:00 nebo 2026-04-13 pro celý den"
                },
                "notes": {
                    "type": "STRING",
                    "description": "Volitelná poznámka"
                },
                "list_name": {
                    "type": "STRING",
                    "description": "Volitelný seznam připomínek"
                },
                "priority": {
                    "type": "STRING",
                    "description": "low | medium | high"
                },
                "all_day": {
                    "type": "BOOLEAN",
                    "description": "Hodnota true označuje celodenní připomínku"
                }
            },
            "required": ["title"]
        }
    },
    {
        "name": "browser_control",
        "description": "Otevře URL v prohlížeči, vyhledá dotaz na Googlu nebo přehraje první výsledek na YouTube.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "action": {"type": "STRING", "description": "open_url | search | play_youtube"},
                "url":    {"type": "STRING", "description": "URL adresa pro akci open_url"},
                "query":  {"type": "STRING", "description": "Vyhledávací dotaz pro akci search nebo play_youtube"}
            },
            "required": ["action"]
        }
    },
    {
        "name": "shell_run",
        "description": "Spustí příkaz v příkazové řádce Windows. Slouží pro práci se soubory a správu systému.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "command": {
                    "type": "STRING",
                    "description": "Příkaz, který se má spustit"
                }
            },
            "required": ["command"]
        }
    },
    {
        "name": "play_media",
        "description": (
            "Otevře skladbu, hudbu nebo video na YouTube, Spotify či Apple Music. "
            "Pokud uživatel určí platformu, použij ji; jinak zvol vhodnou službu. "
            "Při pokynu 'přehraj', 'pusť' nebo 'otevři' použij autoplay=true."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "query": {
                    "type": "STRING",
                    "description": "Název skladby, interpreta, alba nebo videa"
                },
                "provider": {
                    "type": "STRING",
                    "description": "auto | youtube | spotify | apple_music"
                },
                "autoplay": {
                    "type": "BOOLEAN",
                    "description": "Hodnota true spustí obsah přímo, pokud je to možné"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_youtube_channel_report",
        "description": (
            "Vytvoří přehled veřejných statistik kanálu YouTube a výkonu posledních videí. "
            "Použij při dotazu na statistiky, počet odběratelů, poslední videa, růst nebo analýzu kanálu. "
            "Nástroj používá veřejná data YouTube Data API, nikoli YouTube Studio."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "query": {
                    "type": "STRING",
                    "description": (
                        "Požadavek na analýzu v přirozeném jazyce, například "
                        "'jaké jsou statistiky mého YouTube', 'analyzuj poslední videa' nebo "
                        "'shrň růst mého kanálu'"
                    )
                },
                "handle": {
                    "type": "STRING",
                    "description": (
                        "Volitelný handle, odkaz nebo ID kanálu. "
                        "Pokud zůstane prázdný, použije se youtube_channel_handle z nastavení."
                    )
                },
                "video_limit": {
                    "type": "NUMBER",
                    "description": "Počet posledních videí zahrnutých do analýzy. Výchozí hodnota je 6."
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "analyze_screen",
        "description": (
            "Pořídí snímek aktivního okna a analyzuje jej pomocí Gemini Vision. "
            "Použij, když se uživatel ptá, co je na obrazovce, chce přečíst chybu, text, tlačítka nebo obsah okna. "
            "Tato verze podporuje pouze aktivní okno."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "query": {
                    "type": "STRING",
                    "description": "Dotaz uživatele k obrazovce, například 'Přečti tuto chybu' nebo 'Co je na obrazovce?'"
                },
                "target": {
                    "type": "STRING",
                    "description": "Aktuálně je podporována pouze hodnota active_window."
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "save_memory",
        "description": "Uloží důležitou informaci o uživateli do trvalé paměti. Použij tiše při zjištění jména, preferencí, projektů a podobně.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "category": {
                    "type": "STRING",
                    "description": "identity | preferences | projects | notes"
                },
                "key":   {"type": "STRING", "description": "Krátký klíč, například 'name'"},
                "value": {"type": "STRING", "description": "Ukládaná hodnota"}
            },
            "required": ["category", "key", "value"]
        }
    },
    {
        "name": "delete_memory",
        "description": (
            "Odstraní záznam z trvalé paměti. "
            "Použij, když uživatel řekne například 'zapomeň to', 'odstraň to z paměti' nebo 'smaž to'. "
            "Pokud je to možné, použij category a key; jinak vyhledej odpovídající záznam pomocí match_text."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "category": {
                    "type": "STRING",
                    "description": "Kategorie záznamu, například notes | identity | preferences | projects"
                },
                "key": {
                    "type": "STRING",
                    "description": "Klíč odstraňovaného záznamu, například claude_limit_refresh"
                },
                "match_text": {
                    "type": "STRING",
                    "description": "Text pro vyhledání záznamu, například 'obnovení limitu Claude AI'"
                }
            }
        }
    },
    {
        "name": "send_whatsapp_message",
        "description": (
            "Otevře koncept nebo odešle zprávu přes WhatsApp Desktop či WhatsApp Web. "
            "Může pracovat se jménem kontaktu nebo telefonním číslem. "
            "Pokud číslo není uvedeno, nejprve vyhledej jméno v uložených kontaktech WhatsApp a importovaném adresáři. "
            "Pokud uživatel výslovně řekne 'pošli', 'odešli' nebo 'pošli hned', použij bez dalšího potvrzení send_now=true. "
            "Při požadavku 'připrav', 'otevři koncept' nebo 'napiš, ale neposílej' použij send_now=false."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "recipient_name": {
                    "type": "STRING",
                    "description": "Jméno kontaktu, například 'Máma', 'Petr' nebo 'Eva'"
                },
                "phone_number": {
                    "type": "STRING",
                    "description": "Telefonní číslo v mezinárodním formátu, například +420123456789"
                },
                "message": {
                    "type": "STRING",
                    "description": "Obsah odesílané zprávy"
                },
                "app_target": {
                    "type": "STRING",
                    "description": "desktop | web | auto. Výchozí je auto s preferencí desktop."
                },
                "send_now": {
                    "type": "BOOLEAN",
                    "description": "Hodnota true zprávu po otevření konverzace automaticky odešle"
                }
            },
            "required": ["message"]
        }
    },
    {
        "name": "save_whatsapp_contact",
        "description": (
            "Uloží často používaný kontakt WhatsApp se jménem a telefonním číslem do trvalé paměti. "
            "Použij, když uživatel definuje opakovaně použitelný kontakt, například 'máma', 'Petr' nebo 'obchodní partner'."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "display_name": {
                    "type": "STRING",
                    "description": "Ukládané jméno kontaktu, například 'Máma' nebo 'Petr'"
                },
                "phone_number": {
                    "type": "STRING",
                    "description": "Telefonní číslo v mezinárodním formátu, například +420123456789"
                },
                "aliases": {
                    "type": "STRING",
                    "description": "Alternativní oslovení oddělená čárkami, například 'máma, mamka, maminka'"
                }
            },
            "required": ["display_name", "phone_number"]
        }
    }
]


def get_api_key() -> str:
    return str(get_app_config_value("gemini_api_key", "") or "")


def load_system_prompt() -> str:
    try:
        return PROMPT_PATH.read_text(encoding="utf-8")
    except Exception:
        return (
            "Jsi JARVIS, osobní AI asistent pro Windows. "
            "Mluv česky a odpovídej stručně a jasně. "
            "Úkoly skutečně dokončuj pomocí dostupných nástrojů; nepředstírej jejich provedení."
        )


class JarvisLive:
    def __init__(self, ui: JarvisUI):
        self.ui             = ui
        self.session        = None
        self.audio_in_queue = None
        self.out_queue      = None
        self._loop          = None
        self._is_speaking   = False
        self._speaking_lock = threading.Lock()

        self.ui.on_text_command  = self._on_text_command
        self.ui.on_pause_toggle  = self._on_pause_toggle
        self.ui.on_effects_state_change = self._on_effects_state_change
        self._paused             = False

    def _on_pause_toggle(self, paused: bool):
        self._paused = paused

    def _on_effects_state_change(self, enabled: bool):
        pass

    def _focus_ui_section_for_tool(self, tool_name: str, args: dict):
        if tool_name == "sys_info":
            query = str(args.get("query", "")).strip().lower()
            if query in {"time", "date", "čas", "datum"}:
                self.ui.focus_panel("time", duration_ms=5200)
            else:
                self.ui.focus_panel("system", duration_ms=5200)
        elif tool_name == "get_weather":
            self.ui.focus_panel("weather", duration_ms=5600)

    def _on_text_command(self, text: str):
        if self._paused:
            return
        self.ui.write_log(f"Vy: {text}")
        if not self._loop or not self.session:
            self.ui.write_log("ERR: Připojení JARVIS ještě není připravené.")
            return
        asyncio.run_coroutine_threadsafe(
            self.session.send_client_content(
                turns={"parts": [{"text": text}]},
                turn_complete=True
            ),
            self._loop
        )

    async def _interrupt_audio(self):
        try:
            if self.audio_in_queue:
                while not self.audio_in_queue.empty():
                    try:
                        self.audio_in_queue.get_nowait()
                    except Exception:
                        break
            if self.session:
                await self.session.send_realtime_input(audio_stream_end=True)
            self.set_speaking(False)
        except Exception:
            pass


    def set_speaking(self, value: bool):
        with self._speaking_lock:
            self._is_speaking = value
        if value:
            self.ui.set_state("SPEAKING")
        else:
            self.ui.set_state("LISTENING")

    def speak_error(self, tool_name: str, error: str):
        short = str(error)[:120]
        self.ui.write_log(f"ERR: {tool_name} — {short}")
        self.ui.write_debug(f"{tool_name}: {short}", level="ERROR")
        self.ui.set_state("ERROR")

    @staticmethod
    def _result_looks_like_error(result) -> bool:
        text = str(result or "").strip().lower()
        if not text:
            return False
        error_markers = (
            "chyba",
            "nepodařilo",
            "selhal",
            "nenalezen",
            "nenalezena",
            "nenalezeno",
            "není dostup",
            "nejsou dostup",
            "chybí",
            "nelze",
            "nelze otevřít",
            "neplatn",
            "vyžaduje oprávnění",
            "je nutné",
            "připojení",
            "error",
        )
        return any(marker in text for marker in error_markers)

    @staticmethod
    def _should_play_success_sfx(tool_name: str, args: dict, result) -> bool:
        action_tools = {
            "open_app",
            "add_calendar_event",
            "add_reminder",
            "delete_calendar_event",
            "remove_calendar_event",
        }
        if tool_name in action_tools:
            return True

        if tool_name == "send_whatsapp_message":
            text = str(result or "").lower()
            if bool(args.get("send_now", False)):
                return (
                    "odeslána" in text
                    or "odesláno" in text
                )
            return False

        return False

    @staticmethod
    def _clean_transcript_text(text: str) -> tuple[str, bool]:
        raw = str(text or "")
        had_noise = False
        if CONTROL_TOKEN_RE.search(raw):
            had_noise = True
            raw = CONTROL_TOKEN_RE.sub(" ", raw)
        cleaned = []
        for ch in raw:
            if ch in "\n\r\t" or ord(ch) >= 32:
                cleaned.append(ch)
            else:
                had_noise = True
        normalized = " ".join("".join(cleaned).split())
        return normalized.strip(), had_noise

    def _build_config(self) -> types.LiveConnectConfig:
        memory  = load_memory()
        mem_str = format_memory_for_prompt(memory)
        sys_p   = load_system_prompt()
        now     = datetime.datetime.now()
        time_ctx = f"[AKTUÁLNÍ ČAS]\n{now.strftime('%d.%m.%Y — %H:%M')}\n\n"

        parts = [time_ctx]
        if mem_str:
            parts.append(mem_str + "\n\n")
        parts.append(sys_p)

        return types.LiveConnectConfig(
            response_modalities=["AUDIO"],
            output_audio_transcription={},
            input_audio_transcription={},
            system_instruction="\n".join(parts),
            tools=[{"function_declarations": TOOL_DECLARATIONS}],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=str(get_app_config_value("voice", "Charon") or "Charon")
                    )
                )
            ),
        )

    async def _execute_tool(self, fc) -> types.FunctionResponse:
        name = fc.name
        args = dict(fc.args or {})
        print(f"[JARVIS] 🔧 {name} {args}")
        self.ui.set_state("THINKING")

        loop   = asyncio.get_event_loop()
        result = "Hotovo."
        had_exception = False

        try:
            if name == "save_memory":
                cat = args.get("category", "notes")
                key = args.get("key", "")
                val = args.get("value", "")
                if key and val:
                    update_memory({cat: {key: {"value": val}}})
                    print(f"[Memory] 💾 {cat}/{key} = {val}")
                result = "ok"

            elif name == "delete_memory":
                result = delete_memory(
                    args.get("category", ""),
                    args.get("key", ""),
                    args.get("match_text", ""),
                )

            elif name == "open_app":
                r = await loop.run_in_executor(
                    None, lambda: open_app(args.get("app_name", "")))
                result = r or f"Aplikace {args.get('app_name')} byla otevřena."

            elif name == "sys_info":
                self._focus_ui_section_for_tool(name, args)
                r = await loop.run_in_executor(
                    None, lambda: sys_info(args.get("query", "all")))
                result = r or "Informace byly načteny."

            elif name == "get_weather":
                self._focus_ui_section_for_tool(name, args)
                r = await loop.run_in_executor(
                    None, lambda: get_weather_summary(args.get("location") or None))
                result = r or "Informace o počasí byly načteny."

            elif name == "get_calendar_events":
                r = await loop.run_in_executor(
                    None,
                    lambda: get_calendar_events(
                        args.get("query", "today"),
                        int(args.get("limit", 6) or 6),
                    ),
                )
                result = r or "Informace z kalendáře byly načteny."

            elif name == "add_calendar_event":
                r = await loop.run_in_executor(
                    None,
                    lambda: add_calendar_event(
                        args.get("title", ""),
                        args.get("start_iso", ""),
                        args.get("end_iso", ""),
                        args.get("notes", ""),
                        args.get("location", ""),
                        args.get("calendar_name", ""),
                        bool(args.get("all_day", False)),
                    ),
                )
                result = r or "Událost byla přidána do kalendáře."

            elif name == "delete_calendar_event":
                r = await loop.run_in_executor(
                    None,
                    lambda: delete_calendar_event(
                        args.get("title", ""),
                        args.get("start_iso", ""),
                        args.get("calendar_name", ""),
                        bool(args.get("delete_all_matches", False)),
                    ),
                )
                result = r or "Událost byla odstraněna z kalendáře."

            elif name == "get_reminders":
                r = await loop.run_in_executor(
                    None,
                    lambda: get_reminders(
                        args.get("query", "upcoming"),
                        int(args.get("limit", 8) or 8),
                        args.get("list_name", ""),
                    ),
                )
                result = r or "Připomínky byly načteny."

            elif name == "add_reminder":
                r = await loop.run_in_executor(
                    None,
                    lambda: add_reminder(
                        args.get("title", ""),
                        args.get("due_iso", ""),
                        args.get("notes", ""),
                        args.get("list_name", ""),
                        args.get("priority", ""),
                        bool(args.get("all_day", False)),
                    ),
                )
                result = r or "Připomínka byla přidána."

            elif name == "browser_control":
                r = await loop.run_in_executor(
                    None, lambda: browser_control(
                        args.get("action"),
                        args.get("url"),
                        args.get("query")
                    ))
                result = r or "Hotovo."

            elif name == "shell_run":
                r = await loop.run_in_executor(
                    None, lambda: shell_run(args.get("command", "")))
                result = r or "Příkaz byl spuštěn."

            elif name == "play_media":
                r = await loop.run_in_executor(
                    None,
                    lambda: play_media(
                        args.get("query", ""),
                        args.get("provider", "auto"),
                        bool(args.get("autoplay", True)),
                    ),
                )
                result = r or "Přehrávání médií bylo zahájeno."

            elif name == "get_youtube_channel_report":
                r = await loop.run_in_executor(
                    None,
                    lambda: get_youtube_channel_report(
                        args.get("query", "overview"),
                        args.get("handle", ""),
                        int(args.get("video_limit", 6) or 6),
                    ),
                )
                result = r or "Přehled kanálu YouTube byl načten."

            elif name == "analyze_screen":
                r = await loop.run_in_executor(
                    None,
                    lambda: analyze_screen(
                        args.get("query", "Co je na obrazovce?"),
                        args.get("target", "active_window"),
                    ),
                )
                result = r or "Analýza obrazovky byla dokončena."

            elif name == "send_whatsapp_message":
                r = await loop.run_in_executor(
                    None,
                    lambda: send_whatsapp_message(
                        args.get("message", ""),
                        args.get("phone_number", ""),
                        args.get("recipient_name", ""),
                        bool(args.get("send_now", False)),
                        args.get("app_target", "auto"),
                    ),
                )
                result = r or "Operace WhatsApp byla dokončena."

            elif name == "save_whatsapp_contact":
                r = await loop.run_in_executor(
                    None,
                    lambda: save_whatsapp_contact(
                        args.get("display_name", ""),
                        args.get("phone_number", ""),
                        args.get("aliases", ""),
                    ),
                )
                result = r or "Kontakt WhatsApp byl uložen."

            else:
                result = f"Neznámý nástroj: {name}"

        except Exception as e:
            result = f"Chyba: {e}"
            had_exception = True
            traceback.print_exc()
            self.speak_error(name, e)

        tool_failed = self._result_looks_like_error(result)
        if tool_failed:
            if not had_exception:
                self.ui.set_state("ERROR")
        elif self._should_play_success_sfx(name, args, result):
            self.ui.play_success_sfx()

        if not tool_failed and not self.ui.muted:
            self.ui.set_state("LISTENING")

        print(f"[JARVIS] 📤 {name} → {str(result)[:80]}")
        return types.FunctionResponse(
            id=fc.id, name=name,
            response={"result": result}
        )

    async def _send_realtime(self):
        while True:
            msg = await self.out_queue.get()
            await self.session.send_realtime_input(media=msg)

    async def _listen_audio(self):
        print("[JARVIS] 🎤 Mikrofon spuštěn")
        stream = await asyncio.to_thread(
            pya.open,
            format=FORMAT, channels=CHANNELS,
            rate=SEND_SAMPLE_RATE, input=True,
            frames_per_buffer=CHUNK_SIZE,
        )
        try:
            while True:
                data = await asyncio.to_thread(
                    stream.read, CHUNK_SIZE, exception_on_overflow=False)
                with self._speaking_lock:
                    jarvis_speaking = self._is_speaking
                if not jarvis_speaking and not self.ui.muted and not self._paused:
                    await self.out_queue.put({"data": data, "mime_type": "audio/pcm"})
        except Exception as e:
            print(f"[JARVIS] ❌ Mikrofon: {e}")
            raise
        finally:
            stream.close()

    async def _receive_audio(self):
        print("[JARVIS] 👂 Příjem spuštěn")
        out_buf, in_buf = [], []
        output_noise = False
        output_noise_samples = []
        try:
            while True:
                async for response in self.session.receive():
                    if response.data:
                        self.audio_in_queue.put_nowait(response.data)

                    if response.server_content:
                        sc = response.server_content

                        if sc.output_transcription and sc.output_transcription.text:
                            self.set_speaking(True)
                            raw_txt = sc.output_transcription.text.strip()
                            if raw_txt:
                                txt, had_noise = self._clean_transcript_text(raw_txt)
                                if had_noise:
                                    output_noise = True
                                    if len(output_noise_samples) < 4:
                                        output_noise_samples.append(raw_txt)
                                if txt:
                                    out_buf.append(txt)

                        if sc.input_transcription and sc.input_transcription.text:
                            txt = sc.input_transcription.text.strip()
                            if txt:
                                in_buf.append(txt)
                                self.ui.mark_user_activity(True)

                        if sc.turn_complete:
                            # Sentinel přepne stav SPEAKING na LISTENING
                            # po přehrání všech bloků ve zvukové frontě.
                            self.audio_in_queue.put_nowait(None)

                            full_in = " ".join(in_buf).strip()
                            if full_in:
                                self.ui.write_log(f"Vy: {full_in}")
                            in_buf = []

                            full_out = " ".join(out_buf).strip()
                            if full_out:
                                self.ui.write_log(f"JARVIS: {full_out}")
                                if output_noise_samples:
                                    self.ui.write_debug(
                                        "Částečně filtrovaný přepis zvuku: " + " | ".join(output_noise_samples),
                                        level="WARN",
                                    )
                            elif output_noise:
                                self.ui.write_log("ERR: Při přepisu hlasové odpovědi JARVIS došlo k chybě.")
                                if output_noise_samples:
                                    self.ui.write_debug(
                                        "Filtrovaný nezpracovaný přepis: " + " | ".join(output_noise_samples),
                                        level="WARN",
                                    )
                                self.ui.set_state("ERROR")
                            out_buf = []
                            output_noise = False
                            output_noise_samples = []

                    if response.tool_call:
                        fn_responses = []
                        for fc in response.tool_call.function_calls:
                            print(f"[JARVIS] 📞 {fc.name}")
                            fr = await self._execute_tool(fc)
                            fn_responses.append(fr)
                        await self.session.send_tool_response(
                            function_responses=fn_responses)

        except Exception as e:
            print(f"[JARVIS] ❌ Příjem: {e}")
            traceback.print_exc()
            raise

    async def _play_audio(self):
        print("[JARVIS] 🔊 Přehrávání zvuku spuštěno")
        stream = await asyncio.to_thread(
            pya.open,
            format=FORMAT, channels=CHANNELS,
            rate=RECV_SAMPLE_RATE, output=True,
        )
        try:
            while True:
                chunk = await self.audio_in_queue.get()
                if chunk is None:
                    # turn_complete sentinel — vše bylo přehráno, přejdi k poslechu
                    self.set_speaking(False)
                    continue
                self.set_speaking(True)
                await asyncio.to_thread(stream.write, chunk)
        except Exception as e:
            print(f"[JARVIS] ❌ Zvuk: {e}")
            raise
        finally:
            self.set_speaking(False)
            stream.close()

    async def run(self):
        client = genai.Client(
            api_key=get_api_key(),
            http_options={"api_version": "v1alpha"}
        )

        while True:
            # Při pozastavení se nepřipojuj a čekej.
            if self._paused:
                await asyncio.sleep(1)
                continue

            try:
                print("[JARVIS] 🔌 Připojování...")
                self.ui.set_state("THINKING")
                config = self._build_config()

                async with (
                    client.aio.live.connect(model=LIVE_MODEL, config=config) as session,
                    asyncio.TaskGroup() as tg,
                ):
                    self.session        = session
                    self._loop          = asyncio.get_event_loop()
                    self.audio_in_queue = asyncio.Queue()
                    self.out_queue      = asyncio.Queue(maxsize=10)

                    print("[JARVIS] ✅ Připojeno.")
                    self.ui.set_state("LISTENING")
                    self.ui.write_log("SYS: JARVIS je připraven. Poslouchám...")

                    tg.create_task(self._send_realtime())
                    tg.create_task(self._listen_audio())
                    tg.create_task(self._receive_audio())
                    tg.create_task(self._play_audio())

            except Exception as e:
                print(f"[JARVIS] ⚠️ {e}")
                traceback.print_exc()
                self.set_speaking(False)
                self.ui.write_log(f"ERR: Připojení JARVIS bylo přerušeno nebo není dostupný internet — {e}")
                self.ui.set_state("ERROR")
                print("[JARVIS] 🔄 Nový pokus o připojení za 3 sekundy...")
                await asyncio.sleep(3)


def main():
    if os.environ.get("TERM_PROGRAM") == "vscode":
        print("[JARVIS] Spuštěno z prostředí VS Code.")

    ui = JarvisUI()

    def runner():
        ui.wait_for_api_key()
        jarvis = JarvisLive(ui)
        try:
            asyncio.run(jarvis.run())
        except KeyboardInterrupt:
            print("\n🔴 Ukončování...")

    threading.Thread(target=runner, daemon=True).start()

    wake_listener = WakeGestureListener(on_wake=ui.wake_up)
    wake_listener.start()

    ui.root.mainloop()


if __name__ == "__main__":
    main()
