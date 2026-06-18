# 001_elevenlabs_voice

Feature pro hlasový výstup přes ElevenLabs Text to Speech API.

Tato feature není agentní tool a nepatří do `actions/tool_catalog.py`. Slouží jako
runtime hlasový provider, který může později použít desktopová aplikace,
Telegram bridge, mobilní rozhraní nebo konkrétní profil agenta.

## Konfigurace

Skutečné hodnoty patří pouze do lokálního `.env`.

```env
JARVIS_VOICE_PROVIDER="auto"
ELEVENLABS_API_KEY=""
ELEVEN_LABS_API_KEY=""
ELEVENLABS_VOICE_ID=""
ELEVENLABS_MODEL_ID="eleven_multilingual_v2"
ELEVENLABS_OUTPUT_FORMAT="mp3_44100_128"
```

`ELEVEN_LABS_API_KEY` je podporovaný kvůli existující lokální konfiguraci.
Preferovaný nový název je `ELEVENLABS_API_KEY`.

`JARVIS_VOICE_PROVIDER` určuje živý hlasový výstup desktopové aplikace:

- `auto` ponechá stabilní Gemini Live hlas. ElevenLabs se nezapíná automaticky jen
  podle přítomnosti `ELEVENLABS_VOICE_ID`.
- `elevenlabs` vynutí ElevenLabs výstup.
- `gemini` vynutí původní Gemini Live hlas.

Dashboardový přepínač hlasu mění hodnotu `JARVIS_VOICE`, tedy výběr Gemini hlasu.
Při aktivním ElevenLabs výstupu se konkrétní hlas řídí proměnnou
`ELEVENLABS_VOICE_ID`.

Hlasový provider lze přepnout v panelu nastavení volbou `Gemini / ElevenLabs`.
Přepnutí se uloží do `JARVIS_VOICE_PROVIDER` a živá relace se obnoví s novým
providerem. Nabídka hlasů v nastavení se filtruje podle provideru: Gemini ukazuje
Gemini hlasy, ElevenLabs ukazuje pouze hlas nastavený přes `ELEVENLABS_VOICE_ID`.

## Použití

```python
from importlib import import_module

synthesize_to_file = import_module(
    "features.001_elevenlabs_voice.provider"
).synthesize_to_file
synthesize_to_file("Ahoj, jsem JARVIS.", "runtime/voice/sample.mp3")
```

Kvůli číslovanému adresáři bude běžný runtime typicky používat `importlib` nebo
budoucí feature loader, ne přímý `from features.001_elevenlabs_voice ...`.

Při výslovném nastavení `JARVIS_VOICE_PROVIDER="elevenlabs"` zůstává živá
desktopová relace na Gemini native audio modelu, protože tento model nepodporuje
textovou response modalitu. Aplikace proto nepřehrává nativní Gemini audio,
použije jeho výstupní přepis a tento text předá do ElevenLabs. Pro přehrávání
přes `pyaudio` se používá PCM výstup `pcm_24000`, aby nebylo nutné dekódovat MP3
během hovoru.

Pokud ElevenLabs API vrátí `402 Payment Required`, aplikace zobrazí českou hlášku,
uloží `JARVIS_VOICE_PROVIDER="gemini"` a obnoví živou relaci s Gemini Live. Tento
fallback řeší stav, kdy účet ElevenLabs nemá dostupný kredit nebo vyžaduje platbu.

## Zdroj API

ElevenLabs Text to Speech API používá endpoint
`POST /v1/text-to-speech/:voice_id`, hlavičku `xi-api-key` a JSON s textem a
modelem. Výchozí model této feature je `eleven_multilingual_v2`.
