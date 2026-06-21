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

## 2026-06-19 — ACT-002 — Ne blokující spouštění `open_app` v okně

Stav: `IN PROGRESS`

Provedeno:

- `actions/003_open_app/open_app.py` už nepoužívá čekající `subprocess.run` pro
  Windows `start`.
- Spustitelné soubory z `PATH` se otevírají přes neblokující `subprocess.Popen`
  s Windows příznaky pro nové okno a procesovou skupinu.
- Fallback přes Windows `start` se spouští neblokujícím způsobem v samostatném
  okně.
- Dokumentace `actions/003_open_app/README.md`, `actions/tool_catalog.py` a
  `docs/actions/REVIEW.md` byla zpřesněna podle nového chování.
- Plán `ACT-002` byl doplněn o hotový kontrolní bod pro oddělené spouštění
  aplikací v samostatném okně.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile actions\003_open_app\open_app.py actions\003_open_app\__init__.py actions\tool_catalog.py`
- Bezpečný smoke test importu přes loader, validace prázdného názvu a sestavení
  neblokujícího Windows `start` příkazu bez reálného otevření aplikace.
- Prošel jsem `docs/localization/CHECKLIST.md`.

Známá omezení:

- Reálné otevření aplikace nebylo spuštěno automaticky, aby se bez dalšího
  pokynu neměnil stav uživatelského prostředí.
- `ACT-002` zůstává rozpracovaný, protože další ploché akční moduly ještě čekají
  na postupnou revizi a přesun.

## 2026-06-19 — UI-005 — Spouštění dashboardu v samostatném okně

Stav: `DONE`

Provedeno:

- Výchozí start `JarvisUI` byl změněn z fullscreen režimu na běžné samostatné
  okno s vypočtenou centrovanou geometrií.
- `ui.py` nyní při startu explicitně nastavuje `-fullscreen` na `False`.
- Původní automatické volání `_enter_fullscreen` po startu bylo nahrazeno
  vynucením běžné startovní velikosti okna.
- Ruční přepnutí fullscreen režimu přes `F11` a `Ctrl+F` zůstalo zachované.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile ui.py`
- Prošel jsem `docs/localization/CHECKLIST.md`.

Známá omezení:

- Reálný GUI smoke test nebyl spuštěn automaticky, aby se bez výslovného pokynu
  neotevíralo okno aplikace na ploše.

## 2026-06-19 — UI-005 — Povolení zmenšení dashboardového okna

Stav: `DONE`

Provedeno:

- `ui.py` už nenastavuje minimální velikost okna na startovní rozměry dashboardu.
- Přidány menší minimální rozměry `WINDOW_MIN_W` a `WINDOW_MIN_H`, aby šlo okno
  ručně zmenšit a zároveň zůstalo použitelné.
- Přidán handler `<Configure>`, který při ruční změně velikosti přepočítá layout
  přes `_resize_surface`.
- Poslední běžná velikost okna se ukládá do `_normal_size` a `_window_geometry`,
  takže návrat z fullscreen režimu respektuje aktuální velikost okna.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile ui.py`
- Prošel jsem `docs/localization/CHECKLIST.md`.

Známá omezení:

- Reálný GUI resize test nebyl spuštěn automaticky, aby se bez výslovného pokynu
  neotevíralo okno aplikace na ploše.

## 2026-06-19 — FEAT-007 — Telegram hlasové zprávy a servisní příkazy

Stav: `DONE`

Provedeno:

- Telegram bridge nyní podporuje servisní příkazy `/start`, `/help`, `/id`,
  `/chatid` a `/chat_id`.
- Nepovolený chat může přes tyto servisní příkazy zjistit vlastní `chat_id`, ale
  nedostane přístup k agentovi, dokud není v `TELEGRAM_ALLOWED_CHAT_IDS`.
- Hlasové zprávy z Telegramu se stáhnou do `runtime/telegram` a v `main.py` se
  přepisují přes Gemini `generate_content`.
- Přepsaný text se předává do stejné cesty `_handle_telegram_text`, kterou
  používají běžné textové Telegram zprávy. Agent tak sdílí stejný runtime,
  actions, paměť i odpovědi.
- Do `.env.example` byla přidána proměnná `TELEGRAM_TRANSCRIPTION_MODEL`.
- Aktualizována dokumentace `features/002_telegram_bridge/README.md` a přehled
  `features/README.md`.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py features\002_telegram_bridge\bridge.py features\002_telegram_bridge\__init__.py`
- Smoke test servisních příkazů Telegram bridge.
- Smoke test dělení dlouhých Telegram odpovědí.
- Smoke test MIME typu pro Telegram audio soubory `.oga`, `.opus` a `.m4a`.
- Izolovaný test přepisu hlasové zprávy s monkeypatchovaným `genai.Client`, bez
  reálného síťového volání.
- Prošel jsem `docs/localization/CHECKLIST.md`.

Známá omezení:

- Reálný Telegram Bot API test nebyl spuštěn automaticky, protože vyžaduje
  skutečný bot token a síťové volání.
- Reálný Gemini přepis hlasové zprávy nebyl spuštěn automaticky, aby se bez
  potvrzení neposílal testovací audio obsah do externí služby.

## 2026-06-19 — FEAT-008 — Telegram hlasové odpovědi podle typu vstupu

Stav: `DONE`

Provedeno:

- Telegram bridge nyní rozlišuje typ vstupu: textový dotaz vrací textovou
  odpověď a hlasový dotaz vrací audio odpověď.
- `features/002_telegram_bridge/bridge.py` byl rozšířen o `TelegramBridgeReply`
  a odesílání audio souboru přes Telegram Bot API `sendAudio`.
- `main.py` po přepisu hlasové zprávy získá odpověď agenta stejnou cestou jako u
  textové Telegram zprávy a následně ji převede přes ElevenLabs do MP3 souboru.
- Pokud ElevenLabs není nakonfigurovaný nebo TTS selže, Telegram dostane textový
  fallback s odpovědí agenta.
- Dokumentace `features/002_telegram_bridge/README.md` a `features/README.md`
  byla aktualizována podle nového chování.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py features\002_telegram_bridge\bridge.py features\002_telegram_bridge\__init__.py`
- Smoke test odesílání audio odpovědi přes interní Telegram bridge bez reálného
  Telegram API volání.
- Smoke test syntézy Telegram odpovědi s monkeypatchovaným ElevenLabs providerem
  bez reálného ElevenLabs API volání.
- Izolovaný test celé hlasové větve s falešným přepisem, falešnou odpovědí agenta
  a falešným audio souborem.
- Prošel jsem `docs/localization/CHECKLIST.md`.

Známá omezení:

- Reálné odeslání audio odpovědi přes Telegram nebylo spuštěno automaticky,
  protože vyžaduje síťové volání a skutečný bot token.
- Hlasové odpovědi pro Telegram nyní vyžadují funkční ElevenLabs konfiguraci;
  bez ní se vrací textový fallback.

## 2026-06-19 — FEAT-009 — Dočasné vypnutí ElevenLabs runtime feature

Stav: `DONE`

Provedeno:

- ElevenLabs runtime byl dočasně vypnutý konstantou `ELEVENLABS_RUNTIME_ENABLED = False`.
- `main.py` nyní vynucuje Gemini Live jako aktivní hlasový provider i v případě,
  že je v `.env` uložené `JARVIS_VOICE_PROVIDER="elevenlabs"`.
- Dashboard už nenabízí ElevenLabs jako volbu provideru a hodnotu `elevenlabs`
  z konfigurace bere jako Gemini.
- `app_config.py` a `.env.example` používají jako výchozí provider `gemini`.
- Telegram hlasové dotazy se dál přepisují přes Gemini, ale odpověď se dočasně
  vrací textem, protože ElevenLabs TTS není dostupný.
- Dokumentace `features/001_elevenlabs_voice/README.md`,
  `features/002_telegram_bridge/README.md` a `features/README.md` byla
  aktualizována podle dočasného vypnutí.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py ui.py app_config.py features\002_telegram_bridge\bridge.py features\001_elevenlabs_voice\provider.py`
- Smoke test potvrdil, že aktivní hlasový provider je Gemini a ElevenLabs se
  nepoužívá.
- Smoke test potvrdil, že dashboard nabízí pouze provider `Gemini`.
- Smoke test potvrdil, že Telegram hlasová větev vrátí textový fallback bez TTS.
- Prošel jsem `docs/localization/CHECKLIST.md`.

Známá omezení:

- Telegram hlasové vstupy dočasně nevrací audio odpověď. Po opětovném zapnutí
  funkčního TTS provideru bude možné audio odpovědi vrátit.
- Implementace ElevenLabs zůstává v repozitáři, ale runtime ji nepoužívá.

## 2026-06-19 — FEAT-010 — Opětovné zapnutí ElevenLabs runtime feature

Stav: `DONE`

Provedeno:

- ElevenLabs runtime byl znovu povolený v `main.py` a `ui.py`.
- Dashboard v panelu nastavení znovu nabízí providery Gemini a ElevenLabs.
- Backend při výslovné volbě `JARVIS_VOICE_PROVIDER="elevenlabs"` znovu používá
  ElevenLabs jako aktivní hlasový provider.
- Telegram hlasové dotazy znovu vrací audio odpověď přes ElevenLabs, pokud je TTS
  nakonfigurované; při selhání zůstává textový fallback.
- `.env.example` a dokumentace `features/001_elevenlabs_voice/README.md`,
  `features/002_telegram_bridge/README.md` a `features/README.md` byly
  aktualizované podle obnoveného chování.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py ui.py app_config.py features\001_elevenlabs_voice\provider.py features\002_telegram_bridge\bridge.py`
- Smoke test potvrdil, že dashboard znovu nabízí provider `ElevenLabs`.
- Smoke test potvrdil, že backend při nastavení `JARVIS_VOICE_PROVIDER="elevenlabs"`
  vrací aktivní provider `elevenlabs`.
- Smoke test potvrdil vytvoření Telegram audio odpovědi přes mockovaný ElevenLabs
  provider bez reálného API volání.
- Prošel jsem `docs/localization/CHECKLIST.md`.

Známá omezení:

- Reálné volání ElevenLabs API nebylo spuštěné automaticky, aby se bez potvrzení
  neposílal obsah do externí služby a nespotřebovával kredit.
- Desktopový hlas přes ElevenLabs vyžaduje výslovnou volbu provideru ElevenLabs v
  nastavení nebo hodnotu `JARVIS_VOICE_PROVIDER="elevenlabs"` v lokálním `.env`.

## 2026-06-19 — FEAT-011 — Oprava Telegram hlasových odpovědí přes ElevenLabs

Stav: `DONE`

Provedeno:

- Odpověď na externí Telegram dotaz se po předání čekajícímu Telegram handleru už
  neposílá do lokální ElevenLabs fronty pro přehrání na desktopové stanici.
- `_notify_text_reply` nyní vrací informaci, zda odpověď převzal externí klient.
- Telegram TTS nejdřív zkouší MP3 soubor a při selhání použije WAV soubor z PCM
  výstupu ElevenLabs.
- ElevenLabs provider při HTTP chybě přidává krátký detail odpovědi API do
  diagnostické výjimky.
- Dokumentace Telegram bridge a přehled `features` byly aktualizované podle
  nového chování.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py features\001_elevenlabs_voice\provider.py features\002_telegram_bridge\bridge.py`
- Smoke test potvrdil, že externí Telegram odpověď se označí jako doručená a
  desktopová větev ji může přeskočit.
- Smoke test potvrdil WAV fallback při simulovaném selhání MP3 syntézy bez
  reálného ElevenLabs API volání.
- Prošel jsem `docs/localization/CHECKLIST.md`.

Známá omezení:

- Reálné odeslání MP3 nebo WAV odpovědi přes Telegram Bot API nebylo spuštěné
  automaticky, protože vyžaduje síťové volání a skutečný bot token.
- Pokud ElevenLabs selže i při PCM syntéze, Telegram dál vrátí textový fallback.

## 2026-06-19 — FEAT-012 — Windows TTS fallback pro Telegram hlasové odpovědi

Stav: `DONE`

Provedeno:

- Telegram hlasová odpověď nyní používá více kroků: ElevenLabs MP3, ElevenLabs
  PCM/WAV a nakonec lokální Windows SAPI WAV.
- Pokud ElevenLabs selže nebo není nakonfigurovaný, aplikace se pokusí vytvořit
  WAV soubor přes lokální Windows hlasový engine.
- Windows TTS fallback předává text a cílovou cestu do PowerShellu přes lokální
  environment proměnné procesu, aby se předešlo chybám escapování argumentů.
- Debug log zapisuje důvod selhání ElevenLabs i Windows TTS větve.
- Dokumentace Telegram bridge a přehled `features` byly aktualizované podle
  nového fallbacku.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py features\001_elevenlabs_voice\provider.py features\002_telegram_bridge\bridge.py`
- Smoke test potvrdil směrování na Windows fallback při simulovaném selhání
  ElevenLabs.
- Lokální test potvrdil, že Windows SAPI přes PowerShell vytvoří platný WAV soubor.
- Integrační smoke test potvrdil, že při simulovaném selhání ElevenLabs vznikne
  Telegram audio soubor `*_windows.wav`.
- Prošel jsem `docs/localization/CHECKLIST.md`.

Známá omezení:

- Reálné odeslání fallback WAV souboru přes Telegram Bot API nebylo spuštěné
  automaticky, protože vyžaduje síťové volání a skutečný bot token.
- Windows fallback používá systémový Windows hlas, takže nemusí znít stejně jako
  vybraný ElevenLabs hlas.

## 2026-06-19 — FEAT-013 — Gemini Live hlas pro Telegram odpovědi

Stav: `DONE`

Provedeno:

- Windows SAPI fallback pro Telegram hlasové odpovědi byl odpojený, protože
  používal jiný systémový hlas než desktopová aplikace.
- Hlasový Telegram dotaz při aktivním Gemini Live provideru sbírá audio chunky
  z `response.data` a ukládá je do WAV souboru pro Telegram.
- Audio odpověď určená pro Telegram se nepřehrává lokálně na desktopové stanici.
- Textový Telegram dotaz dál vrací text a případné Live audio se při externím
  pending dotazu neposílá do lokálních reproduktorů.
- Při aktivním ElevenLabs provideru zůstává Telegram hlasová odpověď napojená na
  ElevenLabs MP3/PCM syntézu; Windows TTS se už nepoužívá.
- Dokumentace Telegram bridge a přehled `features` byly aktualizované podle
  nového chování.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py features\001_elevenlabs_voice\provider.py features\002_telegram_bridge\bridge.py`
- Smoke test potvrdil vytvoření WAV souboru z nasbíraných Gemini Live audio chunků.
- Smoke test potvrdil, že textový Telegram dotaz potlačí lokální audio bez ukládání
  a hlasový Telegram dotaz audio chunky uloží.
- Smoke test potvrdil, že bez pending externího dotazu se audio dál může přehrát
  lokálně běžnou desktopovou cestou.
- Prošel jsem `docs/localization/CHECKLIST.md`.

Známá omezení:

- Reálné odeslání Gemini Live WAV souboru přes Telegram Bot API nebylo spuštěné
  automaticky, protože vyžaduje síťové volání a skutečný bot token.
- Gemini Live hlas pro Telegram je dostupný při aktivním Gemini provideru. Pokud
  je desktop přepnutý na ElevenLabs, Telegram použije ElevenLabs syntézu.

## 2026-06-19 — ARCH-005 — Základ serverové architektury FastAPI/PostgreSQL

Stav: `DONE`

Provedeno:

- Do `DECISIONS.md` bylo přidáno `ADR-016` pro postupnou migraci na serverový
  backend FastAPI, Uvicorn a PostgreSQL.
- Založen balíček `backend` oddělený od současné desktop aplikace.
- Přidána FastAPI aplikace s verzovaným prefixem `/api/v1`.
- Přidány endpointy `GET /api/v1/health`, `GET /api/v1/status` a připravený
  `POST /api/v1/messages`.
- Přidána konfigurační vrstva pro backend host, port, reload režim a
  `DATABASE_URL`.
- Přidána lazy PostgreSQL health kontrola přes SQLAlchemy async engine a
  `asyncpg`, která bezpečně hlásí i stav bez nastavené databáze.
- `.env.example`, `requirements.txt`, `backend/README.md` a slovník lokalizace
  byly aktualizované pro nový backend.
- Nové backend závislosti byly nainstalované do projektového `.venv`.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile backend\__init__.py backend\config.py backend\database.py backend\api.py backend\app.py backend\__main__.py`
- Import test potvrdil dostupnost `fastapi`, `uvicorn`, `sqlalchemy` a `asyncpg`.
- Smoke test přes `fastapi.testclient.TestClient` ověřil `/api/v1/health`,
  `/api/v1/status` a `/api/v1/messages`.
- Prošel jsem `docs/localization/CHECKLIST.md`.

Známá omezení:

- Agentní runtime zatím zůstává v `main.py`; endpoint `POST /api/v1/messages`
  vrací `not_implemented`.
- PostgreSQL není v lokálním `.env` zatím nastavené, takže `/api/v1/status`
  pouze hlásí, že `DATABASE_URL` chybí.
- Backend zatím není automaticky spouštěný společně s desktopovou aplikací.

## 2026-06-19 — ARCH-006 — Migrační plán a první agentní runtime kontrakt

Stav: `DONE`

Provedeno:

- Byl založen samostatný migrační plán `docs/MIGRATION_PLAN.md`.
- Plán popisuje fáze `MIG-001` až `MIG-009` pro agentní kontrakt, konverzační
  relace, PostgreSQL persistenci, migraci paměti, Telegram přes backend, desktop
  přes backend, WebSocket API, mobilní API kontrakt a autentizaci.
- Přidány Pydantic modely `MessageRequest` a `MessageResponse` v
  `backend/schemas.py`.
- Přidána služba `backend/services/agent_runtime.py` jako první mezivrstva mezi
  HTTP API a budoucím sdíleným agentním runtime.
- `POST /api/v1/messages` byl napojený na `AgentRuntime` a vrací stabilní
  odpověďový model se stavem `runtime_unavailable`.
- `GET /api/v1/status` nově vrací i stav `agent_runtime`.
- `backend/README.md` byl aktualizovaný o message kontrakt.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile backend\__init__.py backend\config.py backend\database.py backend\schemas.py backend\api.py backend\app.py backend\__main__.py backend\services\__init__.py backend\services\agent_runtime.py`
- API smoke test přes `fastapi.testclient.TestClient` ověřil validní payload pro
  `POST /api/v1/messages`, stav `runtime_unavailable`, generování `message_id` a
  `conversation_id` a stav `agent_runtime` v `/api/v1/status`.
- Prošel jsem `docs/localization/CHECKLIST.md`.

Známá omezení:

- `AgentRuntime` zatím nevolá živou Gemini session ani actions; funguje jako
  stabilní backend kontrakt pro další migrační krok.
- Migrační plán byl nově založen jako `docs/MIGRATION_PLAN.md`; nepřejmenovával se
  existující soubor, protože samostatný migrační plán v repozitáři dosud nebyl.

## 2026-06-19 — ARCH-007 — Sdílený model konverzační relace v backendu

Stav: `DONE`

Provedeno:

- Přidány backend modely `StoredMessage`, `ConversationSummary` a
  `ConversationDetail`.
- Přidáno dočasné in-memory úložiště `ConversationStore` pro konverzační relace.
- `AgentRuntime` při `POST /api/v1/messages` zakládá nebo načítá relaci podle
  `conversation_id`, ukládá turn uživatele a přechodovou odpověď asistenta.
- Přidány endpointy `GET /api/v1/conversations` a
  `GET /api/v1/conversations/{conversation_id}`.
- `docs/MIGRATION_PLAN.md` označuje `MIG-002` jako dokončený a popisuje omezení
  in-memory úložiště.
- `backend/README.md` byl aktualizovaný o endpointy relací.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile backend\schemas.py backend\api.py backend\services\agent_runtime.py backend\services\conversations.py`
- API smoke test přes `fastapi.testclient.TestClient` ověřil vytvoření relace,
  seznam relací, detail relace, uložené role `user` a `assistant` i 404 pro
  neexistující relaci.
- Prošel jsem `docs/localization/CHECKLIST.md`.

Známá omezení:

- Konverzační relace jsou zatím uložené pouze v paměti procesu a po restartu
  backendu se ztratí.
- Trvalé uložení do PostgreSQL patří do navazujícího kroku `MIG-003`.

## 2026-06-19 — ARCH-008 — Repository rozhraní pro konverzační persistenci

Stav: `DONE`

Provedeno:

- `ConversationStore` byl rozdělený na abstraktní `ConversationRepository` a
  konkrétní `InMemoryConversationRepository`.
- `AgentRuntime` nyní závisí na repository rozhraní, ne na konkrétní in-memory
  implementaci.
- Přidána factory `backend/storage.py` pro vytváření conversation repository.
- API dál používá in-memory fallback, ale už přes factory, takže PostgreSQL
  implementaci půjde zapojit bez změny endpointů.
- `docs/MIGRATION_PLAN.md` označuje `MIG-003` jako `IN PROGRESS` a má hotové
  kontrolní body pro repository kontrakt.
- `backend/README.md` popisuje aktuální repository fallback.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile backend\api.py backend\storage.py backend\services\agent_runtime.py backend\services\conversations.py`
- API smoke test přes `fastapi.testclient.TestClient` ověřil, že vytvoření zprávy,
  seznam relací a detail relace dál fungují nad repository factory.
- Prošel jsem `docs/localization/CHECKLIST.md`.

Známá omezení:

- PostgreSQL repository zatím není implementované; factory vždy vrací in-memory
  fallback.
- Relace se stále ztratí po restartu backendu, dokud nebude dokončená další část
  `MIG-003`.

## 2026-06-19 — ARCH-009 — SQLAlchemy 2.0 modely pro konverzační data

Stav: `DONE`

Provedeno:

- Přidán balíček `backend/db` se SQLAlchemy 2.0 declarative base.
- Přidány ORM modely `Client`, `Conversation` a `Message` pro tabulky `clients`,
  `conversations` a `messages`.
- Doplněny vazby mezi klienty, konverzacemi a zprávami, mazání zpráv při smazání
  konverzace, základní indexy a timestamp sloupce.
- Sloupec databázové tabulky `messages.metadata` je v Pythonu mapovaný jako
  `metadata_json`, protože `metadata` je rezervovaný atribut SQLAlchemy modelu.
- `docs/MIGRATION_PLAN.md` označuje hotový kontrolní bod pro SQLAlchemy modely v
  rámci `MIG-003`.
- `backend/README.md` popisuje aktuální stav databázových modelů.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile backend\db\__init__.py backend\db\base.py backend\db\models.py`
- Import SQLAlchemy metadata ověřil tabulky `clients`, `conversations` a
  `messages`.
- Kompilace `CreateTable` přes PostgreSQL dialect proběhla bez chyby.
- API smoke test přes `fastapi.testclient.TestClient` ověřil, že vytvoření zprávy,
  seznam relací a detail relace dál fungují nad in-memory fallbackem.
- Prošel jsem `docs/localization/CHECKLIST.md`.

Známé omezení:

- PostgreSQL repository zatím není napojené na tyto modely; backend dál používá
  in-memory fallback přes `ConversationRepository`.
- Inicializace databázového schématu a přepnutí factory podle `DATABASE_URL`
  zůstává v dalších kontrolních bodech `MIG-003`.

## 2026-06-20 — DOC-001 — Uložení stavu projektu a konverzace před restartem

Stav: `DONE`

Provedeno:

- Přidán `docs/PROJECT_STATE.md` s aktuálním stavem migrace, dokončenými kroky,
  rozpracovaným `MIG-003`, důležitými soubory a doporučeným dalším krokem.
- Přidán `docs/CONVERSATION_STATE.md` s pracovním kontextem aktuální konverzace a
  doporučeným promptem pro navázání po restartu.
- Stav byl uložen bez hodnot z `.env`, tokenů, API klíčů a databázových connection
  stringů.
- `docs/localization/PLAN.md` doplněn o dokumentační krok `DOC-001`.

Ověření:

- Zkontrolováno, že stav navazuje na `MIG-003` v `docs/MIGRATION_PLAN.md`.
- Prošel jsem `docs/localization/CHECKLIST.md` v rozsahu relevantním pro
  dokumentační změnu.

Známé omezení:

- Nebyly spouštěny Python testy, protože změna upravuje pouze Markdown
  dokumentaci.

## 2026-06-20 — ARCH-010 — PostgreSQL repository pro konverzační data

Stav: `IN PROGRESS`

Provedeno:

- `ConversationRepository` bylo převedeno na async rozhraní, aby backend mohl
  používat SQLAlchemy async engine bez blokování FastAPI event loopu.
- Přidán `PostgresConversationRepository` nad modely `Client`, `Conversation` a
  `Message`.
- Přidány DB utility pro vytvoření async engine, `async_sessionmaker`, nastavení
  `search_path` a vývojovou inicializaci schématu přes `Base.metadata.create_all`.
- `backend/storage.py` při nastaveném `DATABASE_URL` vytváří PostgreSQL repository.
- Bez `DATABASE_URL` zůstává zachovaný in-memory fallback.
- Při nastavené, ale nedostupné nebo chybně autentizované databázi backend bezpečně
  přechází na in-memory fallback místo pádu endpointu.
- Doplněna volitelná konfigurace `DATABASE_SCHEMA` do backend nastavení a
  `.env.example`.
- Aktualizovány `docs/MIGRATION_PLAN.md`, `backend/README.md` a slovník termínů.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile backend\config.py backend\database.py backend\storage.py backend\api.py backend\services\agent_runtime.py backend\services\conversations.py backend\services\postgres_conversations.py backend\db\session.py backend\db\models.py`
- API smoke test bez databáze ověřil `POST /api/v1/messages`,
  `GET /api/v1/conversations` a `GET /api/v1/conversations/{conversation_id}`.
- API smoke test s nastaveným `DATABASE_URL` a chybně autentizovanou lokální
  PostgreSQL databází ověřil bezpečný přechod na in-memory fallback.
- `GET /api/v1/status` při chybné autentizaci hlásí databázi jako nakonfigurovanou,
  ale nedostupnou.
- Prošel jsem `docs/localization/CHECKLIST.md` v rozsahu relevantním pro backend
  změnu.

Známé omezení:

- Reálný zápis do PostgreSQL nebyl dokončen, protože lokální PostgreSQL server
  vyžaduje heslo pro dostupné uživatele. Zbývá doplnit platné přihlášení nebo
  upravit lokální autentizaci a provést plný PostgreSQL smoke test.
- `ARCH-010` a `MIG-003` proto zůstávají rozpracované.

## 2026-06-20 — ARCH-010 — Test PostgreSQL připojení přes `.env`

Stav: `IN PROGRESS`

Provedeno:

- Backend konfigurace byla rozšířena o samostatné `DATABASE_USER`,
  `DATABASE_PASS` a `DATABASE_NAME`.
- Tvorba SQLAlchemy async engine nyní umí doplnit uživatele, heslo a název databáze
  do `DATABASE_URL`, pokud je URL neobsahuje.
- Databázový health check nyní rozlišuje funkční spojení od stavu, kdy cílové
  schéma neexistuje a uživatel ho nemůže vytvořit.
- `.env.example` a `backend/README.md` byly aktualizovány o nové databázové
  proměnné bez skutečných hodnot.
- Bylo provedeno testovací připojení k PostgreSQL přes hodnoty z lokálního `.env`.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile backend\config.py backend\db\session.py backend\database.py backend\storage.py backend\services\postgres_conversations.py`
- Připojení k databázi vrátilo `SELECT 1`.
- `GET /api/v1/status` vrací databázi jako nakonfigurovanou, ale nepřipravenou pro
  zápis kvůli chybějícímu schématu a nedostatečnému oprávnění.
- Ověření práv potvrdilo, že cílové schéma zatím neexistuje a použitý databázový
  uživatel nemá oprávnění `CREATE` nad databází.
- Skutečné hodnoty z `.env`, uživatelské heslo ani connection string nebyly
  vypsány do dokumentace.

Známé omezení:

- Plný PostgreSQL repository smoke test zatím nemůže vytvořit schéma ani tabulky.
  Je potřeba vytvořit cílové schéma ručně nebo udělit databázovému uživateli
  potřebné oprávnění.

## 2026-06-20 — ARCH-010 — Dokončení PostgreSQL repository smoke testu

Stav: `DONE`

Provedeno:

- Po úpravě databázových oprávnění bylo znovu ověřeno PostgreSQL připojení přes
  hodnoty z lokálního `.env`.
- Vývojová inicializace schématu vytvořila tabulky `clients`, `conversations` a
  `messages`.
- Přímý test `PostgresConversationRepository` ověřil vytvoření konverzace, zápis
  uživatelské a asistentovy zprávy, čtení detailu relace a seznam konverzací.
- Backend API smoke test přes `TestClient` ověřil `/api/v1/status`,
  `POST /api/v1/messages`, `GET /api/v1/conversations/{conversation_id}` a
  `GET /api/v1/conversations`.
- `docs/MIGRATION_PLAN.md` a `docs/localization/PLAN.md` byly aktualizovány a
  `MIG-003` / `ARCH-010` jsou označené jako dokončené.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile backend\config.py backend\db\session.py backend\database.py backend\storage.py backend\services\postgres_conversations.py backend\api.py backend\services\agent_runtime.py`
- Přímá inicializace databáze potvrdila dostupné cílové schéma a tabulky
  `clients`, `conversations`, `messages`.
- API smoke test zapsal testovací konverzaci do PostgreSQL a následná SQL kontrola
  potvrdila jednoho klienta, jednu konverzaci a dvě zprávy pro testovací relaci.
- Prošel jsem `docs/localization/CHECKLIST.md` v rozsahu relevantním pro backend
  změnu.

Známé omezení:

- TestClient musí být při více požadavcích nad asyncpg repository použitý jako
  context manager, aby testovací event loop zůstal během celé smoke sady otevřený.
- Migrace stávající krátkodobé paměti a dlouhodobých rozhodnutí do PostgreSQL
  zůstává navazující krok `MIG-004`.

## 2026-06-20 — ARCH-011 — Backend storage pro krátkodobou paměť a dlouhodobá rozhodnutí

Stav: `DONE`

Provedeno:

- Do SQLAlchemy modelů byly přidány tabulky `short_term_memory_turns` a
  `long_term_decisions`.
- Přidáno repository rozhraní `MemoryRepository`, in-memory fallback a
  `PostgresMemoryRepository`.
- `backend/storage.py` nyní vytváří memory repository podle stejného pravidla jako
  conversation repository: PostgreSQL při nastavené databázi, jinak in-memory
  fallback.
- Přidány backend API endpointy pro zápis, čtení, vyhledávání a promazání
  krátkodobé paměti.
- Přidány backend API endpointy pro zápis a čtení dlouhodobých rozhodnutí.
- Přidán idempotentní import současných SQLite záznamů přes
  `POST /api/v1/memory/import/sqlite`.
- `docs/MIGRATION_PLAN.md`, `backend/README.md`, slovník a lokalizační plán byly
  aktualizovány podle dokončeného `MIG-004`.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile backend\db\models.py backend\schemas.py backend\storage.py backend\api.py backend\services\memory.py backend\services\postgres_memory.py backend\services\memory_migration.py`
- In-memory fallback bez databáze ověřil zápis, čtení a vyhledání krátkodobého
  turnu i zápis a čtení dlouhodobého rozhodnutí.
- PostgreSQL API smoke test ověřil `/api/v1/status`,
  `POST /api/v1/memory/short-term`, `GET /api/v1/memory/short-term`,
  `GET /api/v1/memory/short-term/search`, `POST /api/v1/memory/decisions` a
  `GET /api/v1/memory/decisions`.
- Přímá SQL kontrola potvrdila existenci tabulek `short_term_memory_turns` a
  `long_term_decisions` a fyzický zápis testovacích záznamů.
- SQLite import přenesl 228 krátkodobých turnů a 1 dlouhodobé rozhodnutí; druhé
  spuštění importu přidalo 0 duplicit.
- Prošel jsem `docs/localization/CHECKLIST.md` v rozsahu relevantním pro backend
  změnu.

Známé omezení:

- Běžné dlouhodobé faktické záznamy z `memory_items` zůstávají v kompatibilní
  lokální SQLite vrstvě. Jejich případný přesun do sdíleného backend storage je
  samostatné navazující rozhodnutí.

## 2026-06-20 — FEAT-014 — Telegram pouze s textovými odpověďmi

Stav: `DONE`

Provedeno:

- Telegram bridge dál přijímá textové zprávy a hlasové zprávy.
- Hlasové zprávy se dál stahují a přepisují přes Gemini do textu.
- Odesílání audio odpovědí přes Telegram bylo odstraněno z bridge i z napojení v
  `main.py`.
- Telegram po textovém i hlasovém vstupu odpovídá pouze textovou zprávou přes
  `sendMessage`.
- Dokumentace Telegram bridge, ElevenLabs feature, přehled features a migrační
  plán byly aktualizované podle nového chování.
- Návratové soubory `docs/PROJECT_STATE.md` a `docs/CONVERSATION_STATE.md` byly
  aktualizované pro rozpracovaný `MIG-005`.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py features\002_telegram_bridge\bridge.py`
- Izolovaný smoke test `TelegramBotBridge` bez externího Telegram API volání
  ověřil, že textový i hlasový update používají `sendMessage` a nevolají
  `sendAudio`.
- `git diff --check`
- Prošel jsem `docs/localization/CHECKLIST.md` v rozsahu relevantním pro změnu
  Telegram feature.

Známé omezení:

- Telegram bridge po této změně stále volá živý desktopový runtime přes `main.py`.
  Přímé napojení na backend API zůstává další část rozpracovaného `MIG-005`.
- Desktopový `memory/memory_manager.py` zůstává kompatibilní přechodová vrstva;
  nový backend storage je připravený pro klienty a budoucí přesun runtime.

## 2026-06-21 — ARCH-012 — Telegram backend klient a desktopový fallback

Stav: `DONE`

Provedeno:

- Přidán `features/002_telegram_bridge/backend_client.py` jako synchronní klient
  pro `POST /api/v1/messages`.
- Telegram textové vstupy se v `main.py` posílají nejdřív do backend API s
  `channel="telegram"` a `client_id` ve tvaru `telegram:{chat_id}`.
- Přepsané hlasové vstupy z Telegramu používají stejnou backend cestu jako text.
- `conversation_id` z backendu se ukládá per Telegram chat a posílá se v dalších
  zprávách stejného chatu.
- Při nedostupném backendu nebo stavech `runtime_unavailable` / `not_implemented`
  zůstává zachovaný desktopový fallback přes současnou živou relaci v `main.py`.
- Přidány konfigurační proměnné `TELEGRAM_BACKEND_ENABLED`,
  `TELEGRAM_BACKEND_BASE_URL` a `TELEGRAM_BACKEND_TIMEOUT_SECONDS` do
  `.env.example`.
- Dokumentace Telegram feature, přehled features, backend dokumentace, migrační
  plán, slovník a návratové stavové soubory byly aktualizované.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py features\002_telegram_bridge\bridge.py features\002_telegram_bridge\backend_client.py backend\api.py backend\schemas.py backend\services\agent_runtime.py`
- Smoke test `TelegramBackendClient` ověřil URL, JSON payload, timeout a finální
  backend odpověď bez fallbacku.
- Smoke test `main.py` ověřil použití finální backend odpovědi a desktopový
  fallback při `runtime_unavailable` pro textový i přepsaný hlasový vstup.
- API smoke test nad in-memory backendem ověřil `POST /api/v1/messages`,
  `conversation_id`, `client_id="telegram:123"`, kanál `telegram` a očekávaný
  stav `runtime_unavailable`.
- Prošel jsem `docs/localization/CHECKLIST.md` v rozsahu relevantním pro změnu
  Telegram feature a backend klienta.

Známé omezení:

- Backend zatím negeneruje živou agentní odpověď. Dokud `AgentRuntime` vrací
  `runtime_unavailable` nebo `not_implemented`, Telegram používá desktopový
  fallback. Další část `MIG-005` je připojení živého runtime přímo k backendu.

## 2026-06-21 — ARCH-013 — Embedded backend s živým agentním runtime

Stav: `DONE`

Provedeno:

- Backend `AgentRuntime` nyní podporuje volitelný live handler přes `connect()` a
  `disconnect()`.
- `POST /api/v1/messages` při připojeném handleru vrací skutečnou odpověď agenta se
  stavem `ok` a ukládá ji do konverzace.
- Samostatný backend bez live handleru dál vrací řízený stav `runtime_unavailable`.
- FastAPI aplikace ukládá instanci runtime do `app.state.agent_runtime`, aby ji mohl
  embedded desktop backend připojit k živé relaci.
- Desktopová aplikace spouští embedded backend, pokud je
  `JARVIS_EMBEDDED_BACKEND_ENABLED="true"`.
- Po navázání Gemini Live relace se runtime handler z `main.py` zaregistruje do
  backendu; při reconnectu nebo chybě relace se zase odpojí.
- Telegram backend klient používá krátký connect timeout a delší read timeout, aby
  mohl čekat na skutečnou odpověď live modelu.
- Doplněno `ADR-017` pro embedded backend jako přechodovou architekturu.
- `MIG-005` je označený jako dokončený; další krok je `MIG-006` — Desktop přes
  backend.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py backend\app.py backend\api.py backend\services\agent_runtime.py features\002_telegram_bridge\backend_client.py`
- Smoke test `AgentRuntime` ověřil připojený async live handler, stav `ok` a uložení
  zpráv do in-memory repository.
- FastAPI smoke test ověřil `app.state.agent_runtime.connect(...)`, stav
  `agent_runtime.connected=true` v `/api/v1/status` a skutečnou odpověď přes
  `/api/v1/messages`.
- Smoke test Telegram backend klienta ověřil dvojici timeoutů
  `(connect_timeout, read_timeout)`.
- Prošel jsem `docs/localization/CHECKLIST.md` v rozsahu relevantním pro backend a
  Telegram runtime změnu.

Známé omezení:

- Embedded backend je přechodová architektura. Živá agentní orchestrace pořád běží
  v desktopovém procesu. Samostatný backend bez desktop handleru dál vrací
  `runtime_unavailable`.

## 2026-06-21 — ARCH-014 — Desktop textový vstup přes backend

Stav: `DONE`

Provedeno:

- Přidán obecný HTTP klient `backend.client` pro `POST /api/v1/messages`.
- Desktopový textový vstup z dashboardu nyní používá backend API jako první cestu s
  `channel="desktop"` a `client_id` ve tvaru `desktop:{session_id}`.
- Desktopová textová relace si ukládá backend `conversation_id` a posílá ho v
  navazujících zprávách.
- Při vypnutém, nedostupném nebo přechodovém backendu zůstává zachovaný přímý
  fallback do současné Gemini Live session.
- Live handler rozlišuje desktopové a Telegram požadavky: desktopové požadavky
  zachovávají lokální audio/TTS, Telegram požadavky ho dál potlačují.
- Doplněny konfigurační proměnné `JARVIS_BACKEND_CLIENT_ENABLED`,
  `JARVIS_BACKEND_BASE_URL`, `JARVIS_BACKEND_CONNECT_TIMEOUT_SECONDS` a
  `JARVIS_BACKEND_TIMEOUT_SECONDS` do `.env.example`.
- `MIG-006` je označený jako `IN PROGRESS`, protože audio a další ztenčení
  `main.py` zůstává navazující práce.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py backend\client.py backend\app.py backend\api.py backend\services\agent_runtime.py features\002_telegram_bridge\backend_client.py features\002_telegram_bridge\bridge.py`
- Smoke test `BackendClient` ověřil URL, JSON payload, `conversation_id` a timeouty
  pro desktopový `POST /api/v1/messages`.
- Izolovaný smoke test `main.py` ověřil desktopový fallback při `runtime_unavailable`
  a ukládání backend `conversation_id`.
- Smoke test pending odpovědí ověřil, že desktopový backend požadavek nepotlačuje
  lokální audio/TTS, zatímco Telegram požadavek ano.
- Prošel jsem `docs/localization/CHECKLIST.md` v rozsahu relevantním pro backend
  klienta a desktopový textový vstup.

Známé omezení:

- Desktopový text už používá backend jako první cestu, ale audio, mikrofon a živá
  agentní orchestrace zatím fyzicky zůstávají v `main.py`. Jejich přesun závisí na
  navazujícím realtime kontraktu v `MIG-007`.

## 2026-06-21 — ARCH-015 — Realtime WebSocket kontrakt backendu

Stav: `DONE`

Provedeno:

- Přidán realtime event model `RealtimeEvent` s poli pro stav, text a budoucí audio.
- Přidán `backend/services/realtime.py` s `RealtimeEventHub` pro WebSocket klienty.
- Přidán WebSocket endpoint `/api/v1/realtime`.
- WebSocket po připojení posílá `hello` event se `schema_version="realtime.v1"`.
- `/api/v1/status` vrací `realtime.schema_version` a počet připojených klientů.
- `AgentRuntime` publikuje `runtime_state` při připojení a odpojení live handleru.
- `POST /api/v1/messages` publikuje realtime `message` eventy pro uživatelský i
  asistentův turn.
- `MIG-007` je označený jako `IN PROGRESS`, protože skutečný audio stream a klientské
  řídicí příkazy zůstávají navazující práce.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile backend\schemas.py backend\services\realtime.py backend\services\agent_runtime.py backend\api.py backend\app.py`
- WebSocket smoke test ověřil `hello`, realtime stav v `/api/v1/status`, `message`
  eventy po `POST /api/v1/messages` a `pong` odpověď na `ping`.
- Smoke test runtime stavu ověřil `runtime_state` event po `AgentRuntime.connect(...)`.
- Prošel jsem `docs/localization/CHECKLIST.md` v rozsahu relevantním pro backend
  realtime kontrakt.

Známé omezení:

- WebSocket zatím neposílá reálné audio bloky a nepřijímá klientské řídicí příkazy
  kromě jednoduchého `ping`. Typ `audio` a audio pole jsou připravené pro navazující
  implementaci.

## 2026-06-21 — ARCH-016 — Desktop realtime klient nad backendem

Stav: `DONE`

Provedeno:

- Přidán `backend/realtime_client.py` jako synchronní WebSocket klient pro
  `/api/v1/realtime`.
- Doplněna explicitní závislost `websockets` do `requirements.txt`.
- Doplněna konfigurace `JARVIS_BACKEND_REALTIME_ENABLED`,
  `JARVIS_BACKEND_REALTIME_URL`, `JARVIS_BACKEND_REALTIME_OPEN_TIMEOUT_SECONDS` a
  `JARVIS_BACKEND_REALTIME_RECONNECT_SECONDS` do `.env.example`.
- Desktopová aplikace spouští realtime klienta po startu embedded backendu.
- `main.py` zpracovává `hello`, `runtime_state` a `message` eventy.
- Konverzační řádky jsou deduplikované proti současnému lokálnímu logování, aby
  dashboard nezobrazil stejný user nebo assistant turn dvakrát.
- Přechodové assistant eventy se stavem `runtime_unavailable`, `not_implemented` a
  `runtime_error` se nelogují jako běžná odpověď, protože je řeší desktop fallback.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py backend\realtime_client.py backend\client.py backend\api.py backend\app.py backend\schemas.py backend\services\realtime.py backend\services\agent_runtime.py`
- Smoke test `BackendRealtimeClient` ověřil odvození WebSocket URL, explicitní
  realtime URL a parsování JSON eventů.
- Smoke test `main.py` ověřil `hello`, `message`, deduplikaci zpráv a filtrování
  `runtime_unavailable` odpovědi.
- Smoke test ověřil signaturu `websockets.sync.client.connect` pro použité timeouty.
- Prošel jsem `docs/localization/CHECKLIST.md` v rozsahu relevantním pro desktopový
  realtime klient.

Známé omezení:

- Desktop UI je připojené jako realtime klient, ale lokální logovací cesty v
  `main.py` zatím zůstávají kvůli kompatibilitě audio a Gemini Live smyček. Reálný
  audio stream a klientské řídicí příkazy jsou další část `MIG-007`.

## 2026-06-21 — ARCH-017 — Realtime-first logování desktopových textů

Stav: `DONE`

Provedeno:

- Desktopový realtime klient nyní sleduje aktivní `hello` handshake a při reconnectu
  přepíná logování zpět na lokální fallback.
- `main.py` při aktivním realtime spojení nezapisuje desktopový user turn okamžitě
  lokálně; zobrazuje ho backend `message` event.
- Desktopová assistant odpověď z Live session se při aktivním realtime spojení také
  zobrazuje přes backend `message` event.
- Při nedostupném backendu, chybě backend HTTP klienta nebo neaktivním WebSocket
  spojení zůstává lokální fallback logování.
- Hlasové turny zůstávají lokálně logované, dokud nebude hotový realtime audio/text
  kontrakt pro mikrofonní cestu.

Ověření:

- `.\.venv\Scripts\python.exe -m py_compile main.py backend\realtime_client.py backend\client.py backend\api.py backend\app.py backend\schemas.py backend\services\realtime.py backend\services\agent_runtime.py`
- Smoke test `main.py` ověřil, že desktop source používá realtime logování jen při
  aktivním handshake.
- Smoke test ověřil, že reconnect realtime klienta vypne realtime-first logování.
- Smoke test ověřil, že při chybě backend klienta zůstává lokální fallback log s
  uživatelským textem a chybou nepřipraveného spojení.
- Prošel jsem `docs/localization/CHECKLIST.md` v rozsahu relevantním pro desktopové
  realtime logování.

Známé omezení:

- Realtime-first režim se týká desktopových textových turnů. Hlasové vstupy,
  přehrávání a audio fronty zatím zůstávají v lokální cestě `main.py`.
