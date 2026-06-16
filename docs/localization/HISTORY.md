# Historie lokalizace

Historie je vedena chronologicky a je append-only. Nové záznamy přidávej na
konec souboru.

## 2026-06-14 — L10N-001 — Jádro a systémový prompt

Stav: `DONE`

Provedeno:

- Přeloženy popisy nástrojů a provozní hlášky v `main.py`.
- Přeložen systémový prompt v `core/prompt.txt`.
- Opraveny odkazy z macOS a Apple služeb na Windows, Kalendář Google a
  Microsoft To Do.
- Přidán český prefix uživatelských zpráv `Vy:` a jeho rozpoznání v `ui.py`.
- Doplněny české markery pro rozpoznání chyb a úspěšného odeslání zprávy.
- Časový kontext převeden na jednoznačný formát `dd.mm.rrrr — HH:MM`.

Ověření:

- `venv\Scripts\python.exe -m py_compile main.py ui.py`
- Cílené hledání původních tureckých uživatelských textů v `main.py` a
  `core/prompt.txt`.

Známá omezení:

- `ui.py`, moduly `actions` a `memory` stále obsahují turecké uživatelské texty.
- Turecké markery v interní detekci výsledků byly dočasně zachovány kvůli
  kompatibilitě s dosud nepřeloženými moduly.

## 2026-06-14 — L10N-002 — Dokumentace procesu

Stav: `DONE`

Provedeno:

- Přidán `AGENTS.md` s povinností aktualizovat plán a historii při každé změně.
- Založen adresář `docs/localization`.
- Vytvořen plán, kontrolní seznam, historie a překladový slovník.
- Do plánu byly zapsány všechny známé oblasti zbývající lokalizace.

Ověření:

- Ověřena existence všech dokumentů a jejich vzájemné odkazy.
- Počáteční stav plánu odpovídá dosud provedené práci.

## 2026-06-14 — L10N-002 — Registr projektových rozhodnutí

Stav: `DONE`

Provedeno:

- Přidán kořenový `DECISIONS.md` ve zjednodušeném formátu ADR.
- Zapsána rozhodnutí o češtině jako výchozím jazyku, zachování technických
  identifikátorů a povinné průběžné dokumentaci.
- Registr rozhodnutí byl přidán do `AGENTS.md`, lokalizačního rozcestníku a
  kontrolního seznamu.
- Stanoveno pravidlo, že přijatá rozhodnutí se nahrazují novým ADR a
  nepřepisují se zpětně.

Ověření:

- Ověřena existence `DECISIONS.md`.
- Ověřeny odkazy z `AGENTS.md` a `docs/localization/README.md`.
- Ověřena konzistence stavů `L10N-001` a `L10N-002` v plánu.

## 2026-06-14 — L10N-003 až L10N-008 — Úplná textová lokalizace

Stav: `DONE`

Provedeno:

- Přeloženo grafické rozhraní v `ui.py`, včetně stavů, ovládacích prvků,
  nastavení API, informačních panelů a systémových zpráv.
- Přidána česká zobrazovací mapa interních stavů bez změny jejich technických
  identifikátorů.
- Přidáno české formátování názvů měsíců a dnů v týdnu.
- Přeloženy textové návraty systémových, webových, kalendářových,
  připomínkových, mediálních, WhatsApp, obrazových a YouTube akcí.
- Přeložen `memory/memory_manager.py` a formát paměti vkládaný do promptu.
- Přeložen dosud nepřipojený modul `actions/health.py` a doplněny české
  dotazovací aliasy.
- Přeloženy konzolové zprávy v `wakeup_listener.py` a instalační `setup.bat`.
- Odstraněny turecké kompatibilní markery z `main.py`.
- Výchozí lokalita počasí změněna na Prahu a lokální telefonní předvolba na
  `+420`.
- Hlasový modul `actions/tts.py` byl podle ADR-004 ponechán pro samostatný krok
  `L10N-009`.
- Soubor `config/api_keys.json` nebyl při lokalizaci měněn ani vypisován.

Ověření:

- `venv\Scripts\python.exe -m compileall -q main.py ui.py app_config.py
  wakeup_listener.py actions memory`
- Smoke test českých návratů akcí, parseru počasí, telefonní normalizace a
  zdravotních dotazů.
- Krátký start aplikace v projektovém `venv`.
- Vizuální kontrola celoobrazovkového UI; dlouhý text zdravotní karty byl
  následně zkrácen.
- Cílené hledání tureckých znaků a frází mimo `venv`. Jediným výskytem
  tureckých znaků zůstává vlastní jméno autora Alp Ünlü.

Známá omezení:

- Hlas, TTS a česká výslovnost nejsou součástí této změny.
- Úplný funkční regresní test integračních akcí zůstává v kroku `L10N-010`.

## 2026-06-14 — SEC-001 — Citlivá konfigurace v `.env`

Stav: `DONE`

Provedeno:

- Přidán lokální kořenový `.env` a verzovatelná šablona `.env.example` bez
  skutečných tajných hodnot.
- Přidány proměnné `GEMINI_API_KEY`, `YOUTUBE_API_KEY`,
  `YOUTUBE_CHANNEL_HANDLE`, `JARVIS_VOICE` a ukázková
  `JARVIS_WEATHER_LOCATION`.
- `app_config.py` byl převeden z JSON konfigurace na načítání a bezpečně
  uvozovaný zápis `.env`.
- Zachováno stávající rozhraní konfiguračního modulu, a tím také ukládání z UI.
- Přidána přednost proměnných nastavených operačním systémem.
- Existující hodnoty byly jednorázově migrovány bez jejich výpisu a původní
  `config/api_keys.json` byl po úspěšné migraci odstraněn.
- `.gitignore` nyní výslovně ignoruje `.env`.
- `setup.bat` vytváří `.env` z `.env.example`.
- Odstraněna zastaralá šablona `config/api_keys.example.json`.

Ověření:

- `venv\Scripts\python.exe -m py_compile app_config.py`
- `venv\Scripts\python.exe -m compileall -q main.py ui.py app_config.py
  wakeup_listener.py actions memory`
- Izolovaný test migrace, načtení, zápisu a přednosti systémové proměnné.
- Ověřena existence `.env`, absence starého JSON a přítomnost očekávaných názvů
  proměnných bez výpisu jejich hodnot.
- Cílená kontrola verzovatelných souborů nenalezla pravděpodobný API klíč ani
  jiný tajný řetězec.

Známá omezení:

- `.env` je lokální textový soubor, nikoli šifrované úložiště tajemství.
- API klíč, který byl dříve uložen v prostém JSON, je vhodné preventivně
  zneplatnit a vytvořit nový.
