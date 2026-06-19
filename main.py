#!/usr/bin/env python3
"""
JARVIS Windows — jádro hlasového asistenta v reálném čase
Pracovní postup přizpůsobený prostředí Windows
"""

import asyncio
import datetime
import threading
import traceback
import os
import re
import uuid
from importlib import import_module
from pathlib import Path

import pyaudio  # type: ignore[reportMissingModuleSource]
from google import genai  # type: ignore[reportMissingImports]
from google.genai import types  # type: ignore[reportMissingImports]

from app_config import get_app_config_value, save_app_config
from ui import JarvisUI
from memory.memory_manager import (
    load_memory,
    update_memory,
    delete_memory,
    format_memory_for_prompt,
    save_conversation_turn,
    save_long_term_decision,
    format_long_term_decisions_for_prompt,
)
from actions.sys_info  import sys_info
from actions.reminders import get_reminders, add_reminder
from actions.browser   import browser_control
from actions.shell     import shell_run
from actions.whatsapp  import send_whatsapp_message, save_whatsapp_contact
from actions.media     import play_media
from actions.action_loader import load_action_function
from actions.tool_catalog import get_tool_declaration
from actions.screen_vision import analyze_screen
from actions.youtube_stats import get_youtube_channel_report
from wakeup_listener import WakeGestureListener

elevenlabs_voice = import_module("features.001_elevenlabs_voice.provider")
telegram_bridge_module = import_module("features.002_telegram_bridge.bridge")

get_weather_summary = load_action_function(
    "actions.001_weather.weather",
    "get_weather_summary",
)
get_calendar_events = load_action_function(
    "actions.002_calendar.calendar",
    "get_calendar_events",
)
add_calendar_event = load_action_function(
    "actions.002_calendar.calendar",
    "add_calendar_event",
)
delete_calendar_event = load_action_function(
    "actions.002_calendar.calendar",
    "delete_calendar_event",
)
open_app = load_action_function(
    "actions.003_open_app.open_app",
    "open_app",
)

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
ELEVENLABS_PCM_SAMPLE_RATE = 24000
CHUNK_SIZE       = 1024
pya              = pyaudio.PyAudio()

# ── Definice nástrojů ───────────────────────────────────────────────────────
TOOL_DECLARATIONS = [
    get_tool_declaration("open_app"),
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
    get_tool_declaration("get_weather"),
    get_tool_declaration("get_calendar_events"),
    get_tool_declaration("add_calendar_event"),
    get_tool_declaration("delete_calendar_event"),
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
        "description": (
            "Uloží běžnou dlouhodobou faktickou informaci o uživateli, například jméno, preference nebo projekt. "
            "Nepoužívej pro trvalá rozhodnutí; ta ukládej pouze nástrojem save_long_term_decision po výslovném potvrzení uživatele."
        ),
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
        "name": "save_long_term_decision",
        "description": (
            "Uloží dlouhodobé rozhodnutí do samostatné dlouhodobé paměti. "
            "Použij pouze tehdy, když bylo rozhodnutí nejprve výslovně navrženo a uživatel jej následně jasně potvrdil. "
            "Nepoužívej pro běžnou provozní konverzaci ani pro nepotvrzené návrhy."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "title": {
                    "type": "STRING",
                    "description": "Krátký název rozhodnutí."
                },
                "decision": {
                    "type": "STRING",
                    "description": "Jednoznačný text potvrzeného rozhodnutí."
                },
                "rationale": {
                    "type": "STRING",
                    "description": "Volitelný důvod nebo kontext rozhodnutí."
                },
                "source": {
                    "type": "STRING",
                    "description": "Volitelný odkaz na zdroj v konverzaci nebo modul, kterého se rozhodnutí týká."
                },
                "confirmed": {
                    "type": "BOOLEAN",
                    "description": "Musí být true pouze po výslovném potvrzení uživatelem."
                },
                "confirmation_text": {
                    "type": "STRING",
                    "description": "Doslovný nebo stručně citovaný text uživatelského potvrzení."
                }
            },
            "required": ["title", "decision", "confirmed", "confirmation_text"]
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
        self.tts_text_queue = None
        self.out_queue      = None
        self._loop          = None
        self._is_speaking   = False
        self._speaking_lock = threading.Lock()
        self._session_id    = uuid.uuid4().hex
        self._voice_restart_requested = False
        self._external_text_lock = asyncio.Lock()
        self._pending_text_replies: list[asyncio.Future] = []
        self._telegram_bridge = None

        self.ui.on_text_command  = self._on_text_command
        self.ui.on_pause_toggle  = self._on_pause_toggle
        self.ui.on_voice_change  = self._on_voice_change
        self.ui.on_voice_provider_change = self._on_voice_provider_change
        self.ui.on_effects_state_change = self._on_effects_state_change
        self._paused             = False

    def _on_pause_toggle(self, paused: bool):
        self._paused = paused

    def _on_voice_change(self, voice: str):
        if self._uses_elevenlabs_voice():
            self.ui.write_log(
                "SYS: Hlas Gemini byl uložen. ElevenLabs používá ELEVENLABS_VOICE_ID z .env."
            )
            return
        self.ui.write_log(f"SYS: Přepínám hlas na {voice}. Obnovuji hlasovou relaci...")
        if not self._loop or not self.session:
            return
        self._voice_restart_requested = True
        asyncio.run_coroutine_threadsafe(self._restart_session_for_voice_change(), self._loop)

    def _on_voice_provider_change(self, provider: str):
        normalized = "elevenlabs" if str(provider).strip().lower() == "elevenlabs" else "gemini"
        label = "ElevenLabs" if normalized == "elevenlabs" else "Gemini Live"
        self.ui.write_log(f"SYS: Přepínám hlasový výstup na {label}. Obnovuji hlasovou relaci...")
        if not self._loop or not self.session:
            return
        self._voice_restart_requested = True
        asyncio.run_coroutine_threadsafe(self._restart_session_for_voice_change(), self._loop)

    async def _restart_session_for_voice_change(self):
        try:
            if self.session:
                await self.session.close()
        except Exception as exc:
            self.ui.write_debug(f"Obnova hlasové relace: {exc}", level="WARN")

    def _on_effects_state_change(self, enabled: bool):
        pass

    def _active_voice_provider(self) -> str:
        provider = str(get_app_config_value("voice_provider", "auto") or "auto").strip().lower()
        if provider == "elevenlabs":
            return "elevenlabs"
        if provider in {"auto", "gemini"}:
            return "gemini"
        self.ui.write_debug(
            f"Neznámý hlasový provider '{provider}', používám Gemini Live.",
            level="WARN",
        )
        return "gemini"

    def _uses_elevenlabs_voice(self) -> bool:
        return self._active_voice_provider() == "elevenlabs"

    def _focus_ui_section_for_tool(self, tool_name: str, args: dict):
        if tool_name == "sys_info":
            query = str(args.get("query", "")).strip().lower()
            if query in {"time", "date", "čas", "datum"}:
                self.ui.focus_panel("time", duration_ms=5200)
            else:
                self.ui.focus_panel("system", duration_ms=5200)
        elif tool_name == "get_weather":
            self.ui.focus_panel("weather", duration_ms=5600)

    def _remember_turn(self, role: str, content: str, metadata: dict | None = None):
        try:
            save_conversation_turn(role, content, self._session_id, metadata)
        except Exception as exc:
            self.ui.write_debug(f"Paměť konverzace: {exc}", level="WARN")

    def _on_text_command(self, text: str):
        if self._paused:
            return
        self.ui.write_log(f"Vy: {text}")
        self._remember_turn("user", text, {"source": "text"})
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

    def start_telegram_bridge(self):
        try:
            config = telegram_bridge_module.load_config()
            if not telegram_bridge_module.is_configured(config):
                self.ui.write_debug("Telegram bridge není nakonfigurovaný.", level="INFO")
                return
            self._telegram_bridge = telegram_bridge_module.TelegramBotBridge(
                config=config,
                on_text=self._handle_telegram_text,
                on_voice=self._handle_telegram_voice,
                logger=lambda message: self.ui.write_debug(message, level="INFO"),
            )
            self._telegram_bridge.start()
            self.ui.write_log("SYS: Telegram bridge je spuštěný.")
        except Exception as exc:
            self.ui.write_log(f"ERR: Telegram bridge se nepodařilo spustit: {exc}")

    def _handle_telegram_text(self, text: str, chat_id: int) -> str:
        if self._paused:
            return "JARVIS je pozastavený."
        if not self._loop or not self.session:
            return "JARVIS ještě není připojený. Zkuste to za chvíli."
        future = asyncio.run_coroutine_threadsafe(
            self._ask_text_external(text, source="telegram", chat_id=chat_id),
            self._loop,
        )
        try:
            return future.result(timeout=90)
        except Exception as exc:
            self.ui.write_debug(f"Telegram text: {exc}", level="WARN")
            return "Odpověď se nepodařilo získat včas."

    def _handle_telegram_voice(self, path: Path, chat_id: int, voice: dict) -> str:
        self.ui.write_log(f"SYS: Přijata hlasová zpráva z Telegramu: {path.name}")
        return (
            "Hlasová zpráva dorazila. Přepis hlasu z Telegramu zatím není zapojený; "
            "pošli prosím textovou zprávu."
        )

    async def _ask_text_external(self, text: str, source: str, chat_id: int | None = None) -> str:
        async with self._external_text_lock:
            if not self.session:
                return "JARVIS ještě není připojený."
            loop = asyncio.get_running_loop()
            reply_future: asyncio.Future = loop.create_future()
            self._pending_text_replies.append(reply_future)
            self.ui.write_log(f"Vy ({source}): {text}")
            metadata = {"source": source}
            if chat_id is not None:
                metadata["chat_id"] = chat_id
            self._remember_turn("user", text, metadata)
            await self.session.send_client_content(
                turns={"parts": [{"text": text}]},
                turn_complete=True,
            )
            try:
                return await asyncio.wait_for(reply_future, timeout=85)
            finally:
                if reply_future in self._pending_text_replies:
                    self._pending_text_replies.remove(reply_future)

    def _notify_text_reply(self, text: str) -> None:
        if not text or not self._pending_text_replies:
            return
        future = self._pending_text_replies.pop(0)
        if not future.done():
            future.set_result(text)

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
        decisions_str = format_long_term_decisions_for_prompt()
        sys_p   = load_system_prompt()
        now     = datetime.datetime.now()
        time_ctx = f"[AKTUÁLNÍ ČAS]\n{now.strftime('%d.%m.%Y — %H:%M')}\n\n"

        parts = [time_ctx]
        if mem_str:
            parts.append(mem_str + "\n\n")
        if decisions_str:
            parts.append(decisions_str + "\n\n")
        parts.append(sys_p)

        config_kwargs = {
            "response_modalities": ["AUDIO"],
            "output_audio_transcription": {},
            "input_audio_transcription": {},
            "system_instruction": "\n".join(parts),
            "tools": [{"function_declarations": TOOL_DECLARATIONS}],
        }
        config_kwargs["speech_config"] = types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name=str(get_app_config_value("voice", "Charon") or "Charon")
                )
            )
        )
        return types.LiveConnectConfig(**config_kwargs)

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

            elif name == "save_long_term_decision":
                result = save_long_term_decision(
                    args.get("title", ""),
                    args.get("decision", ""),
                    args.get("rationale", ""),
                    args.get("source", ""),
                    bool(args.get("confirmed", False)),
                    "user",
                    args.get("confirmation_text", ""),
                    {"session_id": self._session_id},
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
                    None,
                    lambda: get_weather_summary(
                        args.get("location") or None,
                        args.get("mode", "current"),
                        int(args.get("days", 3) or 3),
                    ),
                )
                result = r or "Informace o počasí byly načteny."

            elif name == "get_calendar_events":
                r = await loop.run_in_executor(
                    None,
                    lambda: get_calendar_events(
                        args.get("query", "today"),
                        int(args.get("limit", 6) or 6),
                        args.get("calendar_name", ""),
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
                        int(args.get("duration_minutes", 60) or 60),
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

        self._remember_turn(
            "tool",
            f"{name}: {result}",
            {"tool_name": name, "args": args, "failed": tool_failed},
        )
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
        text_out_buf = []
        output_noise = False
        output_noise_samples = []
        try:
            while True:
                async for response in self.session.receive():
                    if response.data and not self._uses_elevenlabs_voice():
                        self.audio_in_queue.put_nowait(response.data)

                    if response.text:
                        text = str(response.text).strip()
                        if text:
                            text_out_buf.append(text)

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
                            if not self._uses_elevenlabs_voice():
                                self.audio_in_queue.put_nowait(None)

                            full_in = " ".join(in_buf).strip()
                            if full_in:
                                self.ui.write_log(f"Vy: {full_in}")
                                self._remember_turn("user", full_in, {"source": "voice"})
                            in_buf = []

                            full_out = " ".join(out_buf).strip()
                            if not full_out:
                                full_out = " ".join(text_out_buf).strip()
                            if full_out:
                                self.ui.write_log(f"JARVIS: {full_out}")
                                self._remember_turn("assistant", full_out, {"source": "voice"})
                                self._notify_text_reply(full_out)
                                if self._uses_elevenlabs_voice() and self.tts_text_queue:
                                    self.tts_text_queue.put_nowait(full_out)
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
                            text_out_buf = []
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
            if self._voice_restart_requested and "1000" in str(e):
                return
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

    async def _play_elevenlabs_text(self):
        print("[JARVIS] 🔊 ElevenLabs hlasový výstup spuštěn")
        stream = await asyncio.to_thread(
            pya.open,
            format=FORMAT,
            channels=CHANNELS,
            rate=ELEVENLABS_PCM_SAMPLE_RATE,
            output=True,
        )
        try:
            while True:
                text = await self.tts_text_queue.get()
                if not text:
                    continue
                self.set_speaking(True)
                try:
                    cfg = elevenlabs_voice.load_config()
                    pcm_cfg = elevenlabs_voice.ElevenLabsVoiceConfig(
                        api_key=cfg.api_key,
                        voice_id=cfg.voice_id,
                        model_id=cfg.model_id,
                        output_format="pcm_24000",
                    )
                    audio = await asyncio.to_thread(
                        elevenlabs_voice.synthesize_to_bytes,
                        text,
                        pcm_cfg,
                    )
                    await asyncio.to_thread(stream.write, audio)
                except elevenlabs_voice.ElevenLabsPaymentRequiredError as exc:
                    self.ui.write_log(
                        "ERR: ElevenLabs účet nemá dostupný kredit nebo vyžaduje platbu. "
                        "Přepínám hlasový výstup zpět na Gemini Live."
                    )
                    self.ui.write_debug(str(exc), level="WARN")
                    save_app_config({"voice_provider": "gemini"})
                    if hasattr(self.ui, "set_voice_provider"):
                        self.ui.set_voice_provider("gemini")
                    self._voice_restart_requested = True
                    await self._restart_session_for_voice_change()
                    break
                except elevenlabs_voice.ElevenLabsVoiceError as exc:
                    self.ui.write_log(f"ERR: ElevenLabs hlasový výstup selhal: {exc}")
                    self.ui.set_state("ERROR")
                except Exception as exc:
                    self.ui.write_log(f"ERR: ElevenLabs hlasový výstup selhal: {exc}")
                    self.ui.set_state("ERROR")
                finally:
                    self.set_speaking(False)
        except Exception as e:
            print(f"[JARVIS] ❌ ElevenLabs zvuk: {e}")
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
                uses_elevenlabs = self._uses_elevenlabs_voice()

                async with (
                    client.aio.live.connect(model=LIVE_MODEL, config=config) as session,
                    asyncio.TaskGroup() as tg,
                ):
                    self.session        = session
                    self._loop          = asyncio.get_event_loop()
                    self.audio_in_queue = asyncio.Queue()
                    self.tts_text_queue = asyncio.Queue()
                    self.out_queue      = asyncio.Queue(maxsize=10)

                    provider_label = "ElevenLabs" if uses_elevenlabs else "Gemini Live"
                    print(f"[JARVIS] ✅ Připojeno. Hlas: {provider_label}")
                    self.ui.set_state("LISTENING")
                    self.ui.write_log(f"SYS: JARVIS je připraven. Hlas: {provider_label}. Poslouchám...")

                    tg.create_task(self._send_realtime())
                    tg.create_task(self._listen_audio())
                    tg.create_task(self._receive_audio())
                    if uses_elevenlabs:
                        tg.create_task(self._play_elevenlabs_text())
                    else:
                        tg.create_task(self._play_audio())

                self.session = None
                self.audio_in_queue = None
                self.tts_text_queue = None
                self.out_queue = None
                if self._voice_restart_requested:
                    self._voice_restart_requested = False
                    self.set_speaking(False)
                    self.ui.set_state("THINKING")
                    self.ui.write_log(
                        f"SYS: Hlas {get_app_config_value('voice', 'Charon')} bude aktivní po obnovení spojení."
                    )
                    await asyncio.sleep(0.5)

            except Exception as e:
                self.session = None
                self.audio_in_queue = None
                self.tts_text_queue = None
                self.out_queue = None
                if self._voice_restart_requested:
                    self._voice_restart_requested = False
                    self.set_speaking(False)
                    self.ui.set_state("THINKING")
                    self.ui.write_log(
                        f"SYS: Hlas {get_app_config_value('voice', 'Charon')} bude aktivní po obnovení spojení."
                    )
                    await asyncio.sleep(0.5)
                    continue
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
        jarvis.start_telegram_bridge()
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
