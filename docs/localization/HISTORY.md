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

## 2026-06-16 — L10N-011 — Dočištění dashboardu

Stav: `DONE`

Provedeno:

- Odstraněn autorský/social panel z dashboardu v `ui.py`, včetně ikon a odkazů.
- Odstraněna nepoužitá závislost `Image`/`ImageTk` navázaná pouze na tento panel.
- Odstraněn autorský řádek s tureckým vlastním jménem z hlaviček `main.py` a
  `ui.py`.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py ui.py`
- Cílené hledání výrazů `Alp`, `Ünlü`, `alppunlu`, `alpunlu`, `instagram`,
  `youtube-logo`, `_social_bar`, `_build_social_bar` v `main.py` a `ui.py`.
- Cílené hledání vybraných tureckých dashboardových výrazů v `main.py` a
  `ui.py`.
- `git diff --check`

Známá omezení:

- Nebyl spouštěn plný funkční regresní test aplikace ani vizuální GUI smoke test.

## 2026-06-16 — MEM-001 — Lokální databázová paměť konverzací

Stav: `DONE`

Provedeno:

- Přidána lokální SQLite databáze `memory/jarvis_memory.sqlite3` pro paměť
  asistenta.
- `memory/memory_manager.py` zachovává stávající API `load_memory`,
  `update_memory`, `delete_memory` a `format_memory_for_prompt`.
- Doplněno ukládání konverzačních turnů přes `save_conversation_turn`.
- Přidány pomocné čtecí funkce `recent_conversation_turns` a
  `search_conversation_text`.
- `main.py` ukládá textové vstupy, hlasové přepisy uživatele, přepisy odpovědí
  asistenta a výsledky nástrojů.
- Lokální SQLite soubor a jeho vedlejší soubory jsou ignorované v `.gitignore`.
- Přidáno ADR-007 pro lokální SQLite paměť konverzací.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py memory\memory_manager.py`
- Izolovaný test zápisu a čtení dlouhodobého faktu, uložení konverzačního turnu,
  načtení posledních turnů a smazání testovacího faktu.
- Cílené hledání vybraných tureckých textů v `main.py` a
  `memory/memory_manager.py`.

Známá omezení:

- Vektorové embeddingy zatím nejsou implementované.
- Do promptu se zatím nadále vkládají pouze dlouhodobé fakty, nikoli
  relevantně vyhledané konverzační úryvky.
- Nebyl spouštěn plný funkční regresní test živé audio relace.

## 2026-06-17 — MEM-002 — Krátkodobá paměť a dlouhodobá rozhodnutí

Stav: `DONE`

Provedeno:

- Přidána tabulka `short_term_conversation_turns` pro provozní konverzační
  záznamy.
- Krátkodobá paměť se při zápisu nového turnu promazává o záznamy starší než
  31 dní.
- Přidána tabulka `long_term_decisions` pro potvrzená dlouhodobá rozhodnutí bez
  automatického mazání.
- Přidán nástroj `save_long_term_decision`, který vyžaduje potvrzení a text
  potvrzení uživatele.
- Dlouhodobá rozhodnutí se vkládají do systémového kontextu v samostatné sekci
  `[DLOUHODOBÁ PAMĚŤ — POTVRZENÁ ROZHODNUTÍ]`.
- Doplněno ADR-008 pro oddělení krátkodobé paměti a dlouhodobých rozhodnutí.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py memory\memory_manager.py`
- Smoke test zápisu krátkodobého turnu, promazání záznamu staršího než 31 dní a
  zachování potvrzeného dlouhodobého rozhodnutí.
- Smoke test, že nepotvrzené dlouhodobé rozhodnutí se neuloží.
- Cílené hledání vybraných tureckých textů v `main.py` a
  `memory/memory_manager.py`.

Známá omezení:

- Starší kompatibilní tabulka `conversation_turns` zůstává v databázi kvůli
  migraci, nové zápisy jdou do `short_term_conversation_turns`.
- Změna nebo zrušení dlouhodobého rozhodnutí zatím nemá samostatný nástroj;
  očekává se nové potvrzené rozhodnutí podle ADR-008.
- Plný funkční regresní test živé audio relace nebyl spouštěn.

## 2026-06-17 — MEM-003 — Úklid starých souborů paměti po migraci

Stav: `DONE`

Provedeno:

- Odstraněny nepoužívané šablony původní JSON paměti
  `memory/memory.example.json` a `memory/phone_book.example.json`.
- Odstraněn runtime adresář `memory/__pycache__`.
- Zachovány používané soubory `memory/memory_manager.py`, `memory/__init__.py`
  a lokální SQLite databáze `memory/jarvis_memory.sqlite3`.

Ověření:

- Vyhledání referencí na odstraněné JSON šablony v kódu a dokumentaci.
- `.\.venv\Scripts\python.exe -m py_compile memory\memory_manager.py`
- Kontrola finálního obsahu adresáře `memory`.

Známá omezení:

- `py_compile` při ověření znovu vytvoří `__pycache__`; cache byla po ověření
  znovu odstraněna.

## 2026-06-17 — ACT-001 — Revize akčních modulů

Stav: `DONE`

Provedeno:

- Zmapovány moduly ve složce `actions` a jejich veřejné funkce.
- Porovnáno zapojení modulů proti deklaracím nástrojů v `main.py` a proti
  aktivnímu `core/prompt.txt`.
- Přidán dokument `docs/actions/REVIEW.md` se stavem jednotlivých modulů.
- Doplněno ADR-009: nové funkce, nástroje a agentní integrace se přidávají do
  složky `actions`.
- `core/prompt.txt` byl srovnán s aktuální paměťovou logikou a nástrojem
  `save_long_term_decision`.

Ověření:

- `.\.venv\Scripts\python.exe -m compileall -q actions`
- Import jednotlivých modulů přes `importlib`.
- Bezpečné smoke testy vybraných funkcí bez otevírání aplikací/prohlížeče a bez
  síťového volání.
- Kontrola `requirements.txt` proti importům v `actions`.

Známá omezení:

- Aktuální projektové `.venv` neobsahuje balíčky z `requirements.txt`, proto
  část akčních modulů nelze v tomto prostředí importovat.
- Nebyl proveden plný integrační test akcí, které otevírají aplikace, prohlížeč,
  WhatsApp, obrazovku nebo externí API.

## 2026-06-17 — ACT-002 — První ověřený akční modul

Stav: `IN PROGRESS`

Provedeno:

- Stanoven importovatelný formát číslování ověřených akcí `_NNN_nazev.py`.
- Doplněno ADR-010 pro číslování ověřených akčních modulů.
- Otestován modul počasí reálným dotazem na `wttr.in` pro Prahu.
- Modul `actions/weather.py` byl po úspěšném testu přejmenován na
  `actions/_001_weather.py`.
- Aktualizovány importy v `main.py` a `ui.py`.
- Aktualizován revizní dokument `docs/actions/REVIEW.md`.

Ověření:

- `.\.venv\Scripts\python.exe -c "from actions._001_weather import get_weather_summary; ..."`
- `.\.venv\Scripts\python.exe -m py_compile main.py ui.py actions\_001_weather.py`
- Cílená kontrola, že v kódu nezůstává import `actions.weather`.

Známá omezení:

- `ACT-002` zůstává rozpracovaný, protože ostatní akční moduly ještě nejsou
  postupně otestované a očíslované.

## 2026-06-17 — ACT-003 — Katalog popisů nástrojů pro agenta

Stav: `DONE`

Provedeno:

- Založen `actions/tool_catalog.py` jako jednotné místo pro popisy nástrojů
  volaných agentem.
- Do katalogu byl doplněn první ověřený nástroj `get_weather` včetně modulu,
  funkce, stavu ověření, parametrů, příkladů použití a známých omezení.
- `main.py` nyní pro deklaraci `get_weather` používá katalog místo lokálního
  ručního popisu.
- Doplněno ADR-011 s pravidlem pro ukládání popisů nástrojů.
- Aktualizován revizní dokument `docs/actions/REVIEW.md` a slovník termínů.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py actions\tool_catalog.py actions\_001_weather.py`
- `.\.venv\Scripts\python.exe -c "from actions.tool_catalog import get_tool_declaration, get_tool_metadata; ..."`
- `git diff --check`

Známá omezení:

- Katalog je zatím napojený jen na ověřený nástroj `get_weather`.
- Ostatní deklarace v `main.py` se budou do katalogu přesouvat postupně při
  revizi jednotlivých akčních modulů.
- `get_weather` je popsán jako nástroj pro aktuální počasí, ne jako vícedenní
  předpověď.

## 2026-06-17 — ACT-004 — Zestručnění promptu a pravidlo katalogu

Stav: `DONE`

Provedeno:

- `core/prompt.txt` byl zestručněn: detailní seznam nástrojů a příklady volání
  byly nahrazeny obecným odkazem na `actions/tool_catalog.py`.
- ADR-011 bylo doplněno o pravidlo, že při vytvoření nebo zapojení nové akce
  musí vzniknout odpovídající záznam v katalogu nástrojů.
- Stejné pravidlo bylo doplněno do `docs/actions/REVIEW.md`, kořenového
  `AGENTS.md` a `docs/localization/CHECKLIST.md`.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py actions\tool_catalog.py`
- Cílená kontrola odkazů na `actions/tool_catalog.py`.
- `git diff --check`

Známá omezení:

- Katalog zatím obsahuje pouze ověřený nástroj `get_weather`; další nástroje se
  budou doplňovat při postupné revizi akcí.

## 2026-06-17 — ACT-005 — Rozšíření počasí o libovolné místo a předpověď

Stav: `DONE`

Provedeno:

- `actions/_001_weather.py` byl rozšířen o režimy `current` a `forecast`.
- Aktuální počasí lze dotazovat pro libovolné místo předané parametrem
  `location`; bez místa zůstává výchozí Praha nebo `JARVIS_WEATHER_LOCATION`.
- Předpověď používá stejný zdroj `wttr.in` a vrací krátký souhrn až na 3 dny.
- `main.py` předává do `get_weather_summary` nové parametry `mode` a `days`.
- `actions/tool_catalog.py` byl aktualizován o parametry `location`, `mode` a
  `days`, příklady kombinovaných dotazů a nová omezení.
- Doplněny překlady běžných anglických meteorologických frází vracených službou
  `wttr.in`.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py actions\_001_weather.py actions\tool_catalog.py`
- `get_weather_summary("Brno", "current")` vrátil aktuální počasí pro Brno.
- `get_weather_summary("Ostrava", "forecast", 2)` vrátil dvoudenní předpověď pro
  Ostravu.
- `get_tool_declaration("get_weather")` obsahuje parametry `location`, `mode` a
  `days`.
- `git diff --check`

Známá omezení:

- Předpověď je omezená na data dostupná z `wttr.in`, v praxi nejvýše 3 dny.
- Některé méně časté meteorologické fráze může externí služba stále vrátit
  anglicky; překlady se budou doplňovat podle dalších testů.

## 2026-06-17 — ARCH-001 — Oddělení nástrojů a běhových vlastností asistenta

Stav: `DONE`

Provedeno:

- Založen adresář `features` pro běhové vlastnosti asistenta, komunikační kanály,
  bridge adaptéry, hlasové moduly a poskytovatele služeb.
- Doplněno ADR-012: `actions` obsahuje pouze tools volané agentem přes
  tool/function calling, zatímco Telegram bridge, mobilní kanály a hlasové
  moduly typu ElevenLabs patří do `features`.
- Doplněn `features/README.md` s hranicí mezi `actions` a `features`.
- Aktualizovány `AGENTS.md`, `docs/actions/REVIEW.md`,
  `docs/localization/CHECKLIST.md` a `docs/localization/GLOSSARY.md`.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile features\__init__.py`
- Kontrola pravidel a odkazů na `actions`, `features` a `actions/tool_catalog.py`.
- `git diff --check`

Známá omezení:

- Telegram bridge ani ElevenLabs modul zatím nejsou implementované; vzniklo jen
  cílové místo a pravidla pro jejich budoucí umístění.

## 2026-06-17 — ARCH-002 — Číslované podadresáře pro actions a features

Stav: `DONE`

Provedeno:

- Doplněno ADR-013: nové a revidované akce se ukládají do `actions/NNN_name`,
  nové a revidované features do `features/NNN_name`.
- Ověřená weather akce byla přesunuta z jednosouborového tvaru
  `actions/_001_weather.py` do `actions/001_weather/weather.py`.
- Přidán `actions/action_loader.py`, aby bylo možné načítat moduly z adresářů,
  jejichž název začíná číslicí.
- `main.py`, `ui.py` a `actions/tool_catalog.py` byly přepojeny na modulovou
  cestu `actions.001_weather.weather`.
- Doplněny dokumentační soubory `actions/001_weather/README.md` a pravidla v
  `actions/README.md`, `AGENTS.md`, `docs/actions/REVIEW.md`, `features/README.md`,
  `docs/localization/CHECKLIST.md` a `docs/localization/GLOSSARY.md`.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py ui.py actions\action_loader.py actions\tool_catalog.py actions\001_weather\weather.py actions\001_weather\__init__.py`
- Import `load_action_function("actions.001_weather.weather", "get_weather_summary")`.
- Import katalogu `get_tool_metadata("get_weather")` a kontrola nové modulové cesty.
- `git diff --check`

Známá omezení:

- Starší ploché soubory v `actions` zatím zůstávají jako legacy stav a budou se
  přesouvat do číslovaných podadresářů postupně při revizi dané akce.
- Číslované adresáře nelze importovat přímým syntaktickým zápisem
  `from actions.001_weather ...`; pro tyto importy se používá loader nebo
  `importlib`.

## 2026-06-17 — ARCH-003 — Sdílený základ a specializované profily

Stav: `DONE`

Provedeno:

- Založen adresář `profiles` pro budoucí specializované varianty agenta.
- Doplněn výchozí šablonový profil `profiles/000_base` s `prompt.txt`,
  `actions.json`, `features.json` a dokumentací.
- Doplněno ADR-014: stabilní společný základ se má oddělit od specializace
  agenta, která bude určovaná profilem.
- `features/README.md` byl rozšířen o vztah mezi sdílenými features a profily.
- Aktualizovány `AGENTS.md`, `docs/localization/CHECKLIST.md`,
  `docs/localization/GLOSSARY.md` a `docs/localization/PLAN.md`.

Ověření:

- Kontrola JSON souborů `profiles/000_base/actions.json` a
  `profiles/000_base/features.json`.
- Kontrola dokumentačních odkazů na `profiles`, `features` a
  `actions/tool_catalog.py`.
- `git diff --check`

Známá omezení:

- Profilový loader zatím není implementovaný; aktuální aplikace nadále používá
  `core/prompt.txt` a globální katalog nástrojů.
- `profiles/000_base` je šablona pro budoucí architekturu, ne aktivní runtime
  konfigurace.

## 2026-06-17 — FEAT-001 — ElevenLabs hlasový provider

Stav: `DONE`

Provedeno:

- Založena feature `features/001_elevenlabs_voice`.
- Přidán provider pro ElevenLabs Text to Speech API se syntézou textu do audio
  souboru přes `requests`.
- Provider čte konfiguraci z `.env` přes `app_config.py`.
- Podporované klíče: `ELEVENLABS_API_KEY`, kompatibilní alias
  `ELEVEN_LABS_API_KEY`, `ELEVENLABS_VOICE_ID`, `ELEVENLABS_MODEL_ID` a
  `ELEVENLABS_OUTPUT_FORMAT`.
- `.env.example` byl doplněn o prázdné konfigurační položky ElevenLabs.
- Lokální `.env` byl doplněn o chybějící prázdné položky bez výpisu tajných
  hodnot.
- `profiles/000_base/features.json` nyní uvádí `001_elevenlabs_voice` jako
  zapnutou šablonovou feature.
- `runtime/` byl přidán do `.gitignore` pro budoucí generované audio soubory.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile app_config.py features\001_elevenlabs_voice\__init__.py features\001_elevenlabs_voice\provider.py`
- Import provideru přes `importlib`.
- Bezpečný smoke test `build_text_to_speech_request` s testovací konfigurací bez
  síťového volání.
- Kontrola lokální konfigurace bez výpisu hodnot API klíčů.
- JSON validace `profiles/000_base/features.json`.

Známá omezení:

- Provider zatím není napojený jako hlasový výstup živé Gemini relace.
- Reálná syntéza vyžaduje vyplněný `ELEVENLABS_VOICE_ID`.
- Nebylo provedeno reálné volání ElevenLabs API, aby se bez potvrzení
  nespotřebovával kredit ani neposílal testovací text do externí služby.

## 2026-06-17 — UI-001 — Dashboardový přepínač hlasu

Stav: `DONE`

Provedeno:

- Do levého dolního rohu dashboardu byl přidán kompaktní přepínač hlasu.
- Přepínač používá stejný seznam hlasů jako nastavení.
- Dashboardový přepínač a přepínač v nastavení sdílí stejnou proměnnou, takže
  zůstávají synchronizované.
- Výběr hlasu se ukládá přes existující `save_app_config({"voice": ...})` do
  `JARVIS_VOICE` v lokálním `.env`.
- Levý informační panel byl zkrácen tak, aby se nové ovládání nepřekrývalo s
  kartami dashboardu.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile ui.py app_config.py`
- Kontrola aktuální hodnoty `voice` přes `load_app_config()`.
- Cílená kontrola nových UI metod `_build_dashboard_voice_selector` a
  `_place_dashboard_voice_selector`.

Známá omezení:

- Přepínač zatím vybírá hlas Gemini Live relace přes `JARVIS_VOICE`.
- ElevenLabs hlasový provider má samostatné nastavení `ELEVENLABS_VOICE_ID` a
  zatím není napojený jako živý výstup dashboardu.

## 2026-06-17 — UI-002 — Oprava přepínání hlasu za běhu

Stav: `DONE`

Provedeno:

- `main.py` nyní připojuje `ui.on_voice_change` na handler `JarvisLive`.
- Po změně hlasu se uložená hodnota `JARVIS_VOICE` použije při obnovení Gemini
  Live session.
- Aktivní session se při změně hlasu zavře přes `AsyncSession.close()`.
- Hlavní běhová smyčka rozlišuje běžnou chybu připojení od plánovaného restartu
  kvůli změně hlasu.
- UI zapisuje stavovou zprávu, že hlas bude aktivní po obnovení spojení.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py ui.py app_config.py`
- Kontrola, že `google.genai.live.AsyncSession` obsahuje metodu `close`.
- Cílená kontrola napojení `on_voice_change` a příznaku
  `_voice_restart_requested`.

Známá omezení:

- Hlas Gemini Live nelze změnit uvnitř už otevřené session bez reconnectu, proto
  přepnutí krátce obnoví spojení.
- Reálný GUI test nebyl spuštěn automaticky, aby se bez vyžádání neotevíralo
  okno aplikace.

## 2026-06-17 — FEAT-002 — ElevenLabs jako živý hlasový výstup

Stav: `DONE`

Provedeno:

- ElevenLabs provider byl rozšířen o `synthesize_to_bytes`, aby runtime mohl
  přehrávat audio bez ukládání mezisouboru.
- Přidán režim hlasového provideru `JARVIS_VOICE_PROVIDER` s hodnotami
  `auto`, `gemini` a `elevenlabs`.
- V režimu ElevenLabs používá Gemini Live textový výstup a výsledný text se
  předává do ElevenLabs TTS.
- Živý ElevenLabs výstup používá PCM formát `pcm_24000` a přehrávání přes
  `pyaudio`.
- Dashboardový přepínač hlasu zůstává přepínačem Gemini hlasů; při aktivním
  ElevenLabs výstupu pouze uloží `JARVIS_VOICE` a upozorní, že ElevenLabs hlas
  určuje `ELEVENLABS_VOICE_ID`.
- Dokumentace feature a profilu byla doplněna o rozdíl mezi Gemini hlasem a
  ElevenLabs `voice_id`.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py app_config.py features\001_elevenlabs_voice\provider.py features\001_elevenlabs_voice\__init__.py`
- Bezpečný smoke test `build_text_to_speech_request` pro `pcm_24000` bez
  reálného API volání.
- Kontrola lokální konfigurace bez výpisu tajných hodnot: `voice_provider=auto`,
  API klíč ElevenLabs nastaven, `ELEVENLABS_VOICE_ID` nastaven.

Známá omezení:

- Nebylo provedeno reálné volání ElevenLabs API ani poslechový test, aby se bez
  výslovného potvrzení neposílal testovací text do externí služby a
  nespotřebovával kredit.
- Dashboard zatím neumí vybírat konkrétní ElevenLabs hlasy; ty se nastavují
  proměnnou `ELEVENLABS_VOICE_ID` v `.env`.

## 2026-06-18 — FEAT-003 — Stabilizace výchozího hlasového provideru

Stav: `DONE`

Provedeno:

- Režim `JARVIS_VOICE_PROVIDER="auto"` už automaticky nepřepíná živou relaci na
  ElevenLabs jen proto, že je v `.env` vyplněný `ELEVENLABS_VOICE_ID`.
- Výchozí a automatický režim zůstává stabilní Gemini Live audio výstup.
- ElevenLabs se zapne pouze výslovně přes `JARVIS_VOICE_PROVIDER="elevenlabs"`.
- Neznámá hodnota provideru spadne zpět na Gemini Live a zapíše varování do
  debug logu.
- Dokumentace ElevenLabs feature a základního profilu byla upravena podle nového
  bezpečnějšího chování.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py app_config.py features\001_elevenlabs_voice\provider.py features\001_elevenlabs_voice\__init__.py`
- Smoke test volby provideru: `auto -> gemini`, `elevenlabs -> elevenlabs`,
  neznámá hodnota -> `gemini`.
- Kontrola konfigurace bez výpisu tajných hodnot potvrdila, že lokální `.env`
  stále obsahuje `voice_provider=auto` a vyplněný `ELEVENLABS_VOICE_ID`.

Známá omezení:

- Reálný poslechový test ElevenLabs nebyl spuštěn. Pro aktivaci ElevenLabs je
  nyní nutné výslovně nastavit `JARVIS_VOICE_PROVIDER="elevenlabs"`.

## 2026-06-18 — UI-003 — Přepínač hlasového provideru v dashboardu

Stav: `DONE`

Provedeno:

- Do levého dolního dashboardového bloku byl doplněn druhý řádek `VÝSTUP` s
  volbou `Gemini / ElevenLabs`.
- Stejná volba byla přidána do panelu nastavení jako `PROVIDER`.
- Výběr se ukládá do `JARVIS_VOICE_PROVIDER` v lokálním `.env`.
- `main.py` nyní přijímá callback `on_voice_provider_change` a při změně
  provideru obnoví živou relaci.
- Výchozí hodnota `auto` se v UI zobrazuje jako stabilní volba `Gemini`.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py ui.py app_config.py`
- Kontrola konfigurace bez výpisu tajných hodnot: `voice_provider=auto`,
  `ELEVENLABS_VOICE_ID` je nastavený.
- Cílená kontrola nových UI prvků `_build_voice_provider_selector`,
  `_dashboard_provider_menu` a callbacku `on_voice_provider_change`.

Známá omezení:

- Přepínač vybírá pouze provider výstupu. Konkrétní ElevenLabs hlas se zatím
  stále nastavuje přes `ELEVENLABS_VOICE_ID` v `.env`.
- Nebyl spuštěn reálný GUI test ani poslechový test ElevenLabs, aby se bez
  potvrzení neotevíralo okno aplikace a neposílal testovací text do externí
  služby.

## 2026-06-18 — FEAT-004 — Oprava ElevenLabs režimu pro native audio model

Stav: `DONE`

Provedeno:

- Opravena chyba `1007`, kdy se ElevenLabs režim pokoušel spustit
  `response_modalities=["TEXT"]` nad modelem
  `models/gemini-2.5-flash-native-audio-latest`.
- Live konfigurace nyní vždy používá `response_modalities=["AUDIO"]`, protože
  native audio model nepodporuje textovou response modalitu.
- Výstupní přepis odpovědi (`output_audio_transcription`) zůstává zapnutý a v
  ElevenLabs režimu se používá jako text pro ElevenLabs TTS.
- Při aktivním ElevenLabs režimu se nativní Gemini audio neukládá do fronty a
  nepřehrává.
- Očekávané zavření session s kódem `1000` při přepnutí provideru se v přijímací
  úloze bere jako korektní ukončení.
- Dokumentace ElevenLabs feature byla upravena podle skutečného fungování s
  native audio modelem.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py ui.py app_config.py features\001_elevenlabs_voice\provider.py features\001_elevenlabs_voice\__init__.py`
- Kontrola sestavení Live konfigurace v `main.py`: modalita zůstává `AUDIO`,
  `output_audio_transcription` je zapnutý.
- `git diff --check`

Známá omezení:

- Reálný poslechový test ElevenLabs nebyl spuštěn automaticky, aby se bez
  potvrzení neposílal text do externí služby a nespotřebovával kredit.

## 2026-06-18 — UI-004 — Hlasové nastavení pouze v panelu nastavení

Stav: `DONE`

Provedeno:

- Odstraněn hlasový blok z levého dolního rohu dashboardu.
- Nastavení hlasu a provideru nyní probíhá pouze v panelu nastavení vlevo nahoře.
- Nabídka `HLAS` se filtruje podle vybraného `PROVIDER`.
- Pro `Gemini` se zobrazují pouze Gemini hlasy `Charon`, `Puck`, `Aoede`,
  `Kore`, `Fenrir`, `Leda`, `Orus` a `Zephyr`.
- Pro `ElevenLabs` se zobrazuje pouze položka `ElevenLabs (.env)`, protože
  konkrétní hlas určuje `ELEVENLABS_VOICE_ID`.
- Při volbě ElevenLabs hlasu se nepřepisuje `JARVIS_VOICE`; ukládá se pouze
  provider přes `JARVIS_VOICE_PROVIDER`.
- Levému dashboardovému panelu byl vrácen prostor dříve rezervovaný pro spodní
  hlasový selector.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile ui.py main.py app_config.py`
- Kontrola, že v `ui.py` nezůstaly reference na dashboardový hlasový selector.
- Smoke test helperů pro filtrování hlasů bez spuštění GUI.

Známá omezení:

- Výběr konkrétního ElevenLabs hlasu zatím není v UI; používá se hodnota
  `ELEVENLABS_VOICE_ID` v `.env`.

## 2026-06-18 — FEAT-005 — Fallback při nedostupném ElevenLabs účtu

Stav: `DONE`

Provedeno:

- ElevenLabs provider nyní rozpoznává odpověď `402 Payment Required` jako
  samostatnou chybu `ElevenLabsPaymentRequiredError`.
- Chyby ElevenLabs TTS už nevypisují syrovou `requests` hlášku s celou URL, ale
  srozumitelný český text.
- Při chybě 402 aplikace zapíše `JARVIS_VOICE_PROVIDER="gemini"`, synchronizuje
  volbu provideru v panelu nastavení a obnoví živou relaci s Gemini Live.
- Obecné chyby ElevenLabs TTS zůstávají zachycené jako chyba hlasového výstupu bez
  automatického přepnutí provideru.
- Dokumentace `features/001_elevenlabs_voice/README.md` popisuje fallback při
  nedostupném kreditu nebo požadované platbě.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py ui.py app_config.py features\001_elevenlabs_voice\provider.py features\001_elevenlabs_voice\__init__.py`
- Bezpečný smoke test bez reálného API volání: monkeypatch `requests.post` vrátil
  simulovanou odpověď 402 a provider vyhodil `ElevenLabsPaymentRequiredError`.

Známá omezení:

- Reálný ElevenLabs účet stále musí mít dostupný kredit nebo aktivní tarif. Fallback
  pouze zabrání tomu, aby asistent zůstal v nefunkčním ElevenLabs režimu.

## 2026-06-18 — ACT-006 — Revize Google Calendar akce

Stav: `DONE`

Provedeno:

- Původní plochý fallback `actions/calendar.py`, který pouze otevíral Kalendář
  Google v prohlížeči, byl nahrazen číslovanou akcí `actions/002_calendar`.
- Nová akce používá Google Calendar API přes OAuth a podporuje nástroje
  `get_calendar_events`, `add_calendar_event` a `delete_calendar_event`.
- `get_calendar_events` umí dotazy na dnes, zítra, týden, příští týden,
  nadcházející události, vyhledání podle názvu a volitelný název kalendáře.
- `add_calendar_event` vyžaduje název události, začátek, trvání nebo konec a
  cílový kalendář; pokud údaj chybí, vrací českou validační hlášku.
- `actions/tool_catalog.py` byl doplněn o pravidla, že se agent má před přidáním
  události doptat na chybějící název, datum, čas, trvání a kalendář.
- `main.py` používá nový modul přes `actions.action_loader` a deklarace nástrojů
  bere z katalogu.
- Do `requirements.txt` byly přidány Google Calendar OAuth knihovny a `tzdata`.
- `.env.example`, `.gitignore`, `docs/actions/REVIEW.md` a slovník byly
  aktualizovány podle nové integrace.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py actions\tool_catalog.py actions\action_loader.py actions\002_calendar\calendar.py actions\002_calendar\__init__.py`
- Smoke test bez reálného Google API volání ověřil rozpoznání dotazů `zítra` a
  `příští týden`.
- Smoke test validace ověřil českou hlášku při chybějícím názvu události.
- Smoke test katalogu ověřil deklarace `get_calendar_events`, `add_calendar_event`
  a `delete_calendar_event`.
- Smoke test loaderu ověřil import `actions.002_calendar.calendar`.
- Test bez OAuth credentials ověřil srozumitelnou hlášku pro chybějící
  `config/google_calendar_credentials.json`.

Známá omezení:

- Reálné čtení a zápis do Kalendáře Google vyžaduje lokální OAuth soubor
  `config/google_calendar_credentials.json` a první přihlášení uživatele.
- Reálný integrační test vůči Google API nebyl spuštěn, aby se bez připraveného
  OAuth klienta neotevíral přihlašovací tok a neměnila skutečná kalendářová data.

## 2026-06-18 — ACT-006 — Test Google Calendar OAuth spojení

Stav: `DONE`

Provedeno:

- První OAuth přihlášení bylo dokončeno přes lokální prohlížečový flow a vznikl
  token `runtime/google_calendar_token.json`.
- Ověřeno načtení primárního kalendáře pro dnešek a příští týden.
- Ověřeno hlášení dostupných kalendářů při neexistujícím názvu kalendáře.
- Výběr kalendáře byl doplněn o porovnávání bez diakritiky, aby dotaz
  `calendar_name="Anežka"` našel kalendář `anezka.travnickova5@gmail.com`.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile actions\002_calendar\calendar.py`
- Reálný Google Calendar API test `get_calendar_events("today", 5)`.
- Reálný Google Calendar API test `get_calendar_events("next_week", 5)`.
- Reálný Google Calendar API test `get_calendar_events("next_week", 3, "Anežka")`.

Známá omezení:

- Aplikace je zatím Googlem neověřená; pro veřejný provoz je potřeba dokončit OAuth
  verification v Google Cloud Console.

## 2026-06-18 — ACT-006 — Oprava čtení událostí napříč kalendáři

Stav: `DONE`

Provedeno:

- Opravena příčina, kdy `get_calendar_events` při chybějícím `calendar_name` četl
  pouze primární kalendář, zatímco nové události mohly být uložené například v
  kalendáři `Rodina`.
- Výchozí dotaz bez názvu kalendáře nyní prohledává primární,
  vlastněné/zapisovatelné a vybrané kalendáře.
- Výsledek z více kalendářů uvádí u každé události název kalendáře v hranatých
  závorkách.
- `actions/tool_catalog.py` a `actions/002_calendar/README.md` byly aktualizovány
  podle nového výchozího chování.

Ověření:

- Diagnostika Google Calendar API ukázala události mimo primární kalendář,
  zejména v kalendáři `Rodina`.
- Reálný Google Calendar API test `get_calendar_events("Konec intru", 5)` našel
  událost v kalendáři `Rodina` bez zadání `calendar_name`.
- `.\.venv\Scripts\python.exe -m py_compile actions\002_calendar\calendar.py`

Známá omezení:

- Výchozí dotaz záměrně nebere všechny čtenářské kalendáře bez výběru, aby se do
  osobní agendy automaticky nemíchaly například svátkové kalendáře.

## 2026-06-18 — ACT-006 — Oprava parsování celých českých dotazů na kalendář

Stav: `DONE`

Provedeno:

- `resolve_query_window` nyní rozpoznává celé české věty typu
  `jaké události mám na zítřek`, `jaké události mám na příští týden` a
  `jaké události mám tento týden`.
- Dotazy na konkrétní událost typu `na kdy mám naplánovanou událost Konec intru`
  se čistí na vyhledávací text `Konec intru`, aby Google Calendar nehledal celou
  větu.
- Katalog nástrojů byl doplněn o doporučení používat normalizované hodnoty
  `tomorrow`, `next_week`, `week` a podobně pro běžné časové dotazy.

Ověření:

- Lokální smoke test mapování celých vět na období a vyhledávací text.
- Reálný Google Calendar API test
  `get_calendar_events("na kdy mám naplánovanou událost Konec intru", 5)` našel
  událost v kalendáři `Rodina`.
- Reálný Google Calendar API test
  `get_calendar_events("jaké události mám na příští týden", 5)` vrátil událost
  `Barcelona`.
- `.\.venv\Scripts\python.exe -m py_compile actions\002_calendar\calendar.py`

Známá omezení:

- Parser pokrývá běžné české formulace. Specifické relativní formulace mimo tento
  rozsah je vhodné v agentovi posílat jako normalizované hodnoty z katalogu.

## 2026-06-18 — ACT-006 — Oprava dotazů na kalendář podle českých měsíců

Stav: `DONE`

Provedeno:

- `resolve_query_window` nyní rozpoznává české názvy měsíců včetně pádů, například
  `srpen`, `v srpnu`, `červenec`, `v červenci`.
- Pokud dotaz obsahuje rok, použije se zadaný rok; jinak se použije nejbližší
  výskyt daného měsíce od aktuálního data.
- Dotaz na osobu v měsíčním období, například `jaké události má Anežka na červenec`,
  použije měsíc jako časové okno a jméno jako vyhledávací text.
- Katalog nástrojů byl zpřesněn, aby agent neposílal `calendar_name="Anežka"`,
  pokud se uživatel ptá na osobu a ne výslovně na kalendář Anežka.

Ověření:

- Lokální smoke test mapování `srpen`, `červenec`, `Anežka na červenec`.
- Reálný Google Calendar API test
  `get_calendar_events("jaké mám já v kalendáři události na srpen?", 10)` vrátil
  srpnové události včetně `Zubařka`.
- Reálný Google Calendar API test
  `get_calendar_events("jaké události má Anežka na červenec", 10)` vrátil červencové
  události s Anežkou z kalendáře `Rodina`.
- `.\.venv\Scripts\python.exe -m py_compile actions\002_calendar\calendar.py actions\tool_catalog.py`

Známá omezení:

- Dotazy na méně běžné časové výrazy mimo podporované měsíce, týdny a relativní
  formulace je dál vhodné předávat nástroji jako normalizované období.

## 2026-06-18 — ACT-006 — Pevné mapování dotazů na kalendáře

Stav: `DONE`

Provedeno:

- `get_calendar_events` nyní z textu dotazu odvozuje cílový kalendář podle pevného
  pravidla:
  `moje/já/můj` -> `travnicek.michal5@gmail.com`,
  `Anežka` -> `travnickova.anezka@gmail.com`,
  `Márinka` -> `marinka.travnickova`,
  `rodina` -> `Rodina`.
- Vyhledání kalendáře je tolerantní k aktuálnímu názvu/emailu vrácenému Googlem,
  takže `travnickova.anezka@gmail.com` se v dostupných kalendářích správně najde
  jako `anezka.travnickova5@gmail.com`.
- Pokud je kalendář odvozený z dotazu, nepoužívá se zároveň jméno osoby jako
  fulltextový filtr událostí.
- `actions/tool_catalog.py` a `actions/002_calendar/README.md` byly aktualizovány
  podle pevného mapování.

Ověření:

- Lokální smoke test inferencí pro vlastní kalendář, Anežku, Márinku a rodinu.
- Reálný Google Calendar API test mapování názvů kalendářů.
- Reálný Google Calendar API test pro `jaké mám události na srpen` vrátil událost
  `Zubařka` z kalendáře `travnicek.michal5@gmail.com`.
- Reálný Google Calendar API test pro `jaké události má rodina na srpen` vrátil
  srpnové události z kalendáře `Rodina`.
- Reálný Google Calendar API test pro `Anežka` a `Márinka` ověřil správné cílové
  kalendáře.

Známá omezení:

- Pokud se skutečný Google kalendář přejmenuje tak, že už nepůjde spárovat podle
  aliasů nebo emailových částí, bude potřeba aktualizovat mapování v
  `actions/002_calendar/calendar.py`.

## 2026-06-18 — FEAT-006 — Telegram bridge pro textovou komunikaci

Stav: `DONE`

Provedeno:

- Založena feature `features/002_telegram_bridge`.
- Přidán Telegram Bot API bridge přes long polling bez nové externí knihovny.
- Konfigurace probíhá přes `.env`: `TELEGRAM_BRIDGE_ENABLED`,
  `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_CHAT_IDS` a `TELEGRAM_DOWNLOAD_DIR`.
- Přístup je omezený přes allowlist chat ID; nepovolené chaty nedostanou přístup k
  agentovi.
- `main.py` umí předat textovou Telegram zprávu do běžící Gemini Live session a
  vrátit další dokončenou odpověď zpět do Telegramu.
- Hlasové Telegram zprávy se přijmou a uloží do `runtime/telegram`, ale přepis
  hlasu zatím vrací informaci, že STT není zapojené.
- `.env.example`, `features/README.md`, feature README a slovník byly
  aktualizovány.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py features\002_telegram_bridge\bridge.py features\002_telegram_bridge\__init__.py`
- Lokální smoke test `parse_allowed_chat_ids`.
- Lokální smoke test dělení dlouhých Telegram odpovědí.

Známá omezení:

- Reálný Telegram API test nebyl spuštěn, protože zatím není doplněný bot token a
  allowlist chat ID.
- Hlasové zprávy zatím nejsou přepisované do textu. Další krok musí doplnit STT
  nebo konverzi Telegram OGG/Opus audia do podporovaného formátu.

## 2026-06-19 — ARCH-004 — Telegram jako klientský kanál nad backendem agenta

Stav: `DONE`

Provedeno:

- Doplněno ADR-015: komunikační kanály jsou klienti nad sdíleným agentním
  backendem.
- Upřesněno, že Telegram bridge není dashboardový přepisovač, ale samostatný
  komunikační kanál k agentovi.
- Do dokumentace `features` bylo doplněno pravidlo, že Desktop UI, Telegram a
  budoucí webové nebo mobilní rozhraní mají používat stejný agentní runtime.
- README `features/002_telegram_bridge` bylo aktualizováno podle tohoto pravidla.
- Slovník byl doplněn o termíny `Agent backend` a `Agent runtime`.

Ověření:

- Zkontrolována platná ADR v `DECISIONS.md`.
- Aktualizován plán `ARCH-004` z `IN PROGRESS` na `DONE`.
- Prošel jsem `docs/localization/CHECKLIST.md`; změna se týká pouze Markdown
  dokumentace, proto nebyl potřeba `py_compile`.

Známá omezení:

- Oddělené agentní runtime rozhraní zatím není implementované v kódu. Toto ADR
  stanovuje směr pro další refaktor.

## 2026-06-19 — ACT-002 — Přesun akce `open_app`

Stav: `IN PROGRESS`

Provedeno:

- Plochý modul `actions/open_app.py` byl přesunut do číslovaného podadresáře
  `actions/003_open_app/open_app.py`.
- `main.py` načítá funkci `open_app` přes `actions/action_loader.py`.
- Deklarace nástroje `open_app` byla přesunuta z ručního bloku v `main.py` do
  `actions/tool_catalog.py`.
- Přidána dokumentace `actions/003_open_app/README.md`.
- Aktualizován plán a revizní přehled akčních modulů.

Ověření:

- `C:\Users\travn\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m py_compile main.py actions\tool_catalog.py actions\action_loader.py actions\003_open_app\open_app.py actions\003_open_app\__init__.py`
- Smoke test importu přes loader a katalogové deklarace `open_app`.
- Smoke test prázdného názvu aplikace bez otevírání externích programů.
- Cílená kontrola, že v kódu nezůstává import `actions.open_app`.

Známá omezení:

- Nebyl spouštěn test, který by skutečně otevřel aplikaci ve Windows, aby se bez
  výslovného pokynu neměnil stav uživatelského prostředí.
- Projektové `.\.venv\Scripts\python.exe` ani `.\venv\Scripts\python.exe` se v
  aktuálním prostředí nespustily, protože odkazují na nedostupný základní
  interpreter `C:\Users\travn\AppData\Local\Programs\Python\Python311\python.exe`.
- `ACT-002` zůstává rozpracovaný, protože další ploché akční moduly ještě čekají
  na postupnou revizi a přesun.
