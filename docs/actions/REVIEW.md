# Revize akčních modulů

Datum: 2026-06-17

## Shrnutí

Složka `actions` je správné místo pro schopnosti asistenta. Aktuálně ale
obsahuje kombinaci plně zapojených nástrojů, fallback implementací a modulů,
které jsou připravené, ale v současném projektovém `venv` nejsou funkční kvůli
chybějícím balíčkům.

## Pravidlo pro další vývoj

Nové funkce asistenta, volání nástrojů a agentní integrace se přidávají do
složky `actions`. `main.py` slouží jako registr deklarací nástrojů, dispatcher a
orchestrace živé relace. Toto pravidlo je zapsané v `DECISIONS.md` jako
`ADR-009`.

`actions` obsahuje pouze tools volané agentem přes tool/function calling.
Komunikační kanály, bridge adaptéry, hlasové moduly a poskytovatelé služeb patří
do `features`. Telegram bridge nebo budoucí ElevenLabs hlasový modul tedy nejsou
akční moduly, pokud je agent přímo nevolá jako nástroj. Toto pravidlo je zapsané
v `DECISIONS.md` jako `ADR-012`.

Nové a revidované akce se ukládají do číslovaných podadresářů ve tvaru
`actions/NNN_name`, například `actions/001_weather`. Implementační soubory,
dokumentace a podpůrné části patří až dovnitř tohoto adresáře. Toto pravidlo je
zapsané v `DECISIONS.md` jako `ADR-013`.

Popisy nástrojů pro agenta se ukládají do `actions/tool_catalog.py`. Katalog je
zdroj pro strojovou deklaraci nástroje i pro revizní poznámky, kdy funkci volat,
kdy ji nevolat a jaká má omezení. Toto pravidlo je zapsané v `DECISIONS.md` jako
`ADR-011`. Při vytvoření nebo zapojení nové akce musí vzniknout odpovídající
záznam v katalogu; bez něj není akce považovaná za dokončenou.

## Stav modulů

| Modul | Zapojení v `main.py` | Stav | Poznámka |
|---|---:|---|---|
| `003_open_app/` | ano | ověřeno s omezením | Otevírá aplikace přes aliasy, PATH, URI schémata a `start`. Úspěch u některých aplikací nelze spolehlivě ověřit. Popis nástroje je v `actions/tool_catalog.py`. |
| `sys_info.py` | ano | částečně funkční | Importuje se i bez `psutil`; některé dotazy pak používají Windows fallback, CPU/RAM bez `psutil` vrací omezené informace. |
| `shell.py` | ano | funkční s rizikem | Spouští shell příkazy a má bloklist destruktivních příkazů. Bloklist není bezpečnostní sandbox. |
| `002_calendar/` | ano | ověřeno s konfigurací | Používá Google Calendar API přes OAuth. Umí číst události podle období, názvu a kalendáře, přidávat události a odstraňovat shody. Bez OAuth credentials vrací srozumitelnou konfigurační hlášku. |
| `reminders.py` | ano | fallback, ne plná integrace | Nečte ani nevytváří úkoly přes API. Otevírá Microsoft To Do v prohlížeči. |
| `whatsapp.py` | ano | částečně funkční | Ukládání kontaktů funguje přes paměť. Odesílání závisí na WhatsApp Desktop/Web, schránce a volitelně `pyautogui`. |
| `browser.py` | ano | nefunkční v aktuálním `venv` | Chybí `requests`. Po instalaci otevře URL/vyhledávání a umí najít první YouTube video. |
| `media.py` | ano | nefunkční v aktuálním `venv` | Selže importem přes `actions.browser`, protože chybí `requests`. Spotify otevření je jen URI/search fallback. |
| `001_weather/` | ano | ověřeno | Reálný dotaz na `wttr.in` pro Prahu prošel. Modul je první očíslovaná dokončená akce v adresářové struktuře. Popis nástroje je v `actions/tool_catalog.py`; podporuje aktuální počasí i krátkou předpověď do 3 dnů pro zadané místo. |
| `youtube_stats.py` | ano | nefunkční v aktuálním `venv` | Chybí `requests`; pro reálný běh navíc vyžaduje YouTube API klíč. |
| `screen_vision.py` | ano | nefunkční v aktuálním `venv` | Chybí `google-genai`; pro plný běh také potřebuje `mss`, `Pillow` a Gemini API klíč. |
| `health.py` | ne | nezapojené | Importuje se, ale není deklarované jako nástroj v `main.py` ani uvedené v aktivním promptu. Vyžaduje lokální export zdravotních dat. |
| `tts.py` | ne | nezapojené | Importuje se, ale živá relace používá Gemini audio výstup. Modul může být užitečný pro samostatný TTS fallback. |

## Ověření

- `.\.venv\Scripts\python.exe -m compileall -q actions`
- Import jednotlivých modulů přes `importlib`.
- Bezpečné smoke testy bez otevírání aplikací/prohlížeče a bez síťového volání.
- Kontrola `requirements.txt`.

## Zjištěné problémy

- Aktuální projektové `.venv` neobsahuje balíčky uvedené v `requirements.txt`
  (`requests`, `google-genai`, `psutil`, `Pillow`, `pyaudio`, `mss`,
  `pyperclip`, `pyautogui`).
- `main.py` jako celek v tomto `venv` také nepůjde spustit, protože importuje
  `pyaudio`, `google-genai`, `psutil` přes UI a další běhové závislosti.
- `core/prompt.txt` byl po revizi srovnán s aktuální paměťovou logikou a novým
  nástrojem `save_long_term_decision`.

## Doporučené další kroky

- Obnovit projektové `venv` přes `setup.bat` nebo `pip install -r requirements.txt`.
- Doplnit `pyautogui` do `requirements.txt`, pokud má automatické odesílání
  WhatsApp zpráv zůstat podporované.
- Rozhodnout, jestli `health.py` a `tts.py` mají být zapojené jako nástroje,
  nebo ponechané jako nepoužívané podpůrné moduly.
- Postupně nahrazovat fallback modul `reminders.py` skutečnou integrací, pokud má
  asistent umět data číst a zapisovat bez ručního dokončení v prohlížeči.
