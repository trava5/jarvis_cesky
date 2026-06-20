# Plán české lokalizace

Aktualizováno: 2026-06-19

## Přehled

| ID | Oblast | Stav |
|---|---|---|
| L10N-001 | Jádro hlasové aplikace a systémový prompt | DONE |
| L10N-002 | Dokumentace procesu lokalizace | DONE |
| L10N-003 | Grafické rozhraní `ui.py` | DONE |
| L10N-004 | Systémové a základní akce | DONE |
| L10N-005 | Komunikační a multimediální akce | DONE |
| L10N-006 | Kalendář a připomínky | DONE |
| L10N-007 | Paměť asistenta | DONE |
| L10N-008 | Zbývající moduly a úplná jazyková kontrola | DONE |
| L10N-009 | Hlasové výstupy a česká výslovnost | TODO |
| L10N-010 | Funkční regresní test lokalizované aplikace | TODO |
| L10N-011 | Dočištění dashboardu od autorských a tureckých zbytků | DONE |
| MEM-001 | Lokální databázová paměť konverzací | DONE |
| MEM-002 | Oddělení krátkodobé paměti a dlouhodobých rozhodnutí | DONE |
| MEM-003 | Úklid starých souborů paměti po migraci | DONE |
| ACT-001 | Revize akčních modulů a pravidlo pro nové funkce | DONE |
| ACT-002 | Postupné testování a číslování akčních modulů | IN PROGRESS |
| ACT-003 | Katalog popisů nástrojů pro agenta | DONE |
| ACT-004 | Zestručnění promptu a pravidlo katalogu pro nové akce | DONE |
| ACT-005 | Rozšíření počasí o libovolné místo a předpověď | DONE |
| ACT-006 | Revize Google Calendar akce | DONE |
| ARCH-001 | Oddělení nástrojů a běhových vlastností asistenta | DONE |
| ARCH-002 | Číslované podadresáře pro actions a features | DONE |
| ARCH-003 | Architektura sdíleného základu a specializovaných profilů | DONE |
| ARCH-004 | Telegram jako klientský kanál nad backendem agenta | DONE |
| ARCH-005 | Základ serverové architektury FastAPI/PostgreSQL | DONE |
| ARCH-006 | Migrační plán a první agentní runtime kontrakt | DONE |
| ARCH-007 | Sdílený model konverzační relace v backendu | DONE |
| ARCH-008 | Repository rozhraní pro konverzační persistenci | DONE |
| ARCH-009 | SQLAlchemy 2.0 modely pro konverzační data | DONE |
| FEAT-001 | Feature hlasového provideru ElevenLabs | DONE |
| UI-001 | Dashboardový přepínač hlasu | DONE |
| UI-002 | Oprava přepínání hlasu za běhu | DONE |
| UI-003 | Přepínač hlasového provideru v dashboardu | DONE |
| UI-004 | Hlasové nastavení pouze v panelu nastavení | DONE |
| UI-005 | Spouštění dashboardu v samostatném okně | DONE |
| FEAT-002 | Napojení ElevenLabs na živý hlasový výstup | DONE |
| FEAT-003 | Stabilizace výchozího hlasového provideru | DONE |
| FEAT-004 | Oprava ElevenLabs režimu pro native audio model | DONE |
| FEAT-005 | Fallback při nedostupném ElevenLabs účtu | DONE |
| FEAT-006 | Telegram bridge pro textovou komunikaci | DONE |
| FEAT-007 | Telegram bridge pro hlasové zprávy a servisní příkazy | DONE |
| FEAT-008 | Telegram hlasové odpovědi podle typu vstupu | DONE |
| FEAT-009 | Dočasné vypnutí ElevenLabs runtime feature | DONE |
| FEAT-010 | Opětovné zapnutí ElevenLabs runtime feature | DONE |
| FEAT-011 | Oprava Telegram hlasových odpovědí přes ElevenLabs | DONE |
| FEAT-012 | Windows TTS fallback pro Telegram hlasové odpovědi | DONE |
| FEAT-013 | Gemini Live hlas pro Telegram odpovědi | DONE |
| SEC-001 | Přesun citlivé konfigurace do `.env` | DONE |

## L10N-001 — Jádro a prompt

Stav: `DONE`

- [x] Přeložit popisy nástrojů v `main.py`.
- [x] Přeložit provozní hlášky v `main.py`.
- [x] Přeložit `core/prompt.txt` a opravit Windows integrace.
- [x] Přidat český prefix uživatele `Vy:`.
- [x] Po překladu závislých modulů nahradit turecké markery českou detekcí.
- [x] Ověřit syntaxi `main.py` a `ui.py`.

## L10N-002 — Dokumentace procesu

Stav: `DONE`

- [x] Přidat kořenový `AGENTS.md`.
- [x] Založit plán s jednoznačnými stavovými hodnotami.
- [x] Založit append-only historii.
- [x] Založit kontrolní seznam.
- [x] Založit překladový slovník.
- [x] Založit registr projektových rozhodnutí.

## L10N-003 — Grafické rozhraní

Stav: `DONE`

- [x] Zmapovat uživatelské texty v `ui.py`.
- [x] Přeložit navigaci, stavové texty, nastavení a nápovědu.
- [x] Přeložit texty prvotního nastavení API.
- [x] Zachovat interní názvy stavů `LISTENING`, `THINKING`, `SPEAKING` a `ERROR`.
- [x] Ověřit, že delší české texty nepřetékají z prvků UI.
- [x] Ověřit syntaxi a spustit GUI.

## L10N-004 — Systémové a základní akce

Stav: `DONE`

- [x] Přeložit `actions/open_app.py`.
- [x] Přeložit `actions/sys_info.py`.
- [x] Přeložit modul počasí `actions/001_weather/weather.py`.
- [x] Přeložit `actions/browser.py`.
- [x] Přeložit `actions/shell.py`.
- [x] Zachovat rozpoznávání stávajících strojových hodnot.
- [x] Ověřit syntaxi upravených modulů.

## L10N-005 — Komunikace a média

Stav: `DONE`

- [x] Přeložit `actions/whatsapp.py`.
- [x] Přeložit `actions/media.py`.
- [x] Přeložit `actions/youtube_stats.py`.
- [x] Přeložit `actions/screen_vision.py`.
- [x] Přeložit textové návraty související s médii; `actions/tts.py` ponechat
  pro krok `L10N-009`.
- [x] Ověřit návratové zprávy používané detekcí úspěchu a chyb.
- [x] Ověřit syntaxi upravených modulů.

## L10N-006 — Kalendář a připomínky

Stav: `DONE`

- [x] Přeložit `actions/calendar.py`.
- [x] Přeložit `actions/reminders.py`.
- [x] Ověřit české relativní datumové výrazy.
- [x] Ověřit formátování českých dat a časů.
- [x] Zachovat hodnoty `today`, `tomorrow`, `next`, `upcoming` a další API klíče.
- [x] Ověřit syntaxi upravených modulů.

## L10N-007 — Paměť

Stav: `DONE`

- [x] Přeložit uživatelské texty v `memory/memory_manager.py`.
- [x] Zachovat interní kategorie `identity`, `preferences`, `projects` a `notes`.
- [x] Ověřit formát paměti vkládaný do systémového promptu.
- [x] Ověřit syntaxi modulu.

## L10N-008 — Úplná jazyková kontrola

Stav: `DONE`

- [x] Prověřit `actions/health.py` a rozhodnout, zda je aktivně používaný.
- [x] Prověřit `wakeup_listener.py`, `app_config.py` a `setup.bat`.
- [x] Vyhledat zbývající turecké znaky a fráze mimo `venv`.
- [x] Rozlišit uživatelské texty od kompatibilních interních markerů.
- [x] Aktualizovat slovník podle výsledků kontroly.
- [x] Spustit `compileall` nad projektem.

## L10N-009 — Hlasové výstupy a česká výslovnost

Stav: `TODO`

- [ ] Prověřit `actions/tts.py`.
- [ ] Vybrat a ověřit hlas vhodný pro češtinu.
- [ ] Ověřit českou výslovnost diakritiky, čísel, času a názvů aplikací.
- [ ] Ověřit hlasové přerušení, mute a pause.
- [ ] Zapsat výsledek hlasového testu do historie.

## L10N-010 — Regresní test

Stav: `TODO`

- [x] Spustit aplikaci v projektovém `venv`.
- [ ] Ověřit českou textovou konverzaci.
- [ ] Ověřit českou hlasovou odpověď.
- [ ] Ověřit alespoň jednu informační akci.
- [ ] Ověřit alespoň jednu akci měnící stav.
- [ ] Ověřit chybovou hlášku a reconnect.
- [ ] Zapsat výsledek testu do historie.

## L10N-011 — Dočištění dashboardu

Stav: `DONE`

- [x] Odstranit autorský panel a sociální odkazy z dashboardu.
- [x] Odstranit autorský řádek s tureckým vlastním jménem z hlaviček.
- [x] Cíleně ověřit, že v dashboardu nezůstaly turecké zbytky.
- [x] Ověřit syntaxi `main.py` a `ui.py`.
- [x] Zapsat výsledek do historie.

## MEM-001 — Lokální databázová paměť konverzací

Stav: `DONE`

- [x] Přidat lokální SQLite databázi pro paměť.
- [x] Zachovat stávající API dlouhodobých faktů v `memory_manager.py`.
- [x] Ukládat turny uživatele, asistenta a nástrojů z `main.py`.
- [x] Ignorovat lokální databázový soubor v Gitu.
- [x] Ověřit syntaxi a základní databázové operace.
- [x] Zapsat výsledek do historie.

## MEM-002 — Krátkodobá paměť a dlouhodobá rozhodnutí

Stav: `DONE`

- [x] Oddělit provozní konverzační záznamy do krátkodobé paměti.
- [x] Nastavit automatické mazání krátkodobých záznamů starších než 1 měsíc.
- [x] Přidat samostatnou tabulku pro dlouhodobá potvrzená rozhodnutí.
- [x] Přidat nástroj pro uložení dlouhodobého rozhodnutí až po výslovném potvrzení.
- [x] Vkládat dlouhodobá rozhodnutí do systémového kontextu odděleně od běžných faktů.
- [x] Ověřit syntaxi a základní databázové operace.
- [x] Zapsat výsledek do historie.

## MEM-003 — Úklid starých souborů paměti po migraci

Stav: `DONE`

- [x] Odstranit nepoužívané JSON šablony původní paměti.
- [x] Odstranit runtime bytecode artefakty z adresáře `memory`.
- [x] Ověřit, že používané soubory paměti zůstaly zachované.
- [x] Ověřit syntaxi modulu paměti.
- [x] Zapsat výsledek do historie.

## ACT-001 — Revize akčních modulů

Stav: `DONE`

- [x] Zmapovat moduly ve složce `actions`.
- [x] Porovnat moduly s deklarovanými nástroji v `main.py` a `core/prompt.txt`.
- [x] Ověřit importy a syntaxi akčních modulů v projektovém `venv`.
- [x] Zapsat pravidlo pro budoucí funkce a agenty do ADR.
- [x] Zapsat výsledek revize do dokumentace.
- [x] Zapsat výsledek do historie.

## ACT-002 — Testování a číslování akčních modulů

Stav: `IN PROGRESS`

- [x] Stanovit importovatelný tvar číslování ověřených akčních modulů.
- [x] Otestovat a očíslovat modul počasí.
- [x] Aktualizovat napojení v `main.py`.
- [x] Ověřit syntaxi a importy po přejmenování.
- [x] Zapsat průběžný výsledek do historie.
- [x] Otestovat a přesunout `open_app` do `actions/003_open_app`.
- [x] Upravit `open_app`, aby spouštěl aplikace odděleně v samostatném Windows okně.
- [ ] Otestovat a přesunout zbývající akce do číslovaných podadresářů.

## ACT-003 — Katalog popisů nástrojů pro agenta

Stav: `DONE`

- [x] Zvolit jednotné místo pro popisy funkcí volaných agentem.
- [x] Založit katalog popisů ve složce `actions`.
- [x] Napojit ověřený nástroj počasí na katalog.
- [x] Ověřit syntaxi a import katalogu.
- [x] Zapsat výsledek do historie.

## ACT-004 — Zestručnění promptu a pravidlo katalogu

Stav: `DONE`

- [x] Zestručnit `core/prompt.txt` tak, aby odkazoval na katalog nástrojů.
- [x] Doplnit pravidlo, že nová akce musí mít záznam v `actions/tool_catalog.py`.
- [x] Ověřit syntaxi a konzistenci odkazů.
- [x] Zapsat výsledek do historie.

## ACT-005 — Rozšíření počasí o libovolné místo a předpověď

Stav: `DONE`

- [x] Rozšířit `actions/001_weather/weather.py` o předpověď počasí.
- [x] Zachovat možnost dotazu na aktuální počasí pro libovolné místo.
- [x] Umožnit kombinaci místa a typu dotazu v deklaraci nástroje.
- [x] Aktualizovat `actions/tool_catalog.py`.
- [x] Ověřit syntaxi a funkční smoke testy.
- [x] Zapsat výsledek do historie.

## ACT-006 — Revize Google Calendar akce

Stav: `DONE`

- [x] Přesunout calendar akci do `actions/002_calendar`.
- [x] Nahradit prohlížečový fallback skutečnou integrací Google Calendar API.
- [x] Podporovat dotazy na zítřek, týden, příští týden, vyhledání události a konkrétní kalendář.
- [x] Podporovat přidání události s názvem, datem, časem, trváním a cílovým kalendářem.
- [x] Doplnit pravidla pro doptávání chybějících údajů do `actions/tool_catalog.py`.
- [x] Přepojit `main.py` na katalog a nový číslovaný adresář.
- [x] Ověřit syntaxi a bezpečné smoke testy bez reálného Google API volání.
- [x] Ověřit a doladit výběr kalendáře podle běžného jména bez diakritiky.
- [x] Opravit čtení událostí tak, aby dotazy bez názvu kalendáře nečetly pouze primární kalendář.
- [x] Opravit parsování celých českých vět v parametru `query`.
- [x] Opravit parsování dotazů na české názvy měsíců.
- [x] Nastavit pevné mapování dotazů na osobní a rodinné kalendáře.
- [x] Zapsat výsledek do historie.

## ARCH-001 — Oddělení nástrojů a běhových vlastností asistenta

Stav: `DONE`

- [x] Založit adresář pro běhové vlastnosti a komunikační kanály asistenta.
- [x] Zapsat pravidlo, že `actions` obsahuje pouze tools volané agentem.
- [x] Zapsat pravidlo, že Telegram bridge, hlasové moduly a podobné integrace patří mimo `actions`.
- [x] Ověřit syntaxi nového balíčku.
- [x] Zapsat výsledek do historie.

## ARCH-002 — Číslované podadresáře pro actions a features

Stav: `DONE`

- [x] Zavést pravidlo, že každá nová nebo revidovaná akce má vlastní adresář `actions/NNN_name`.
- [x] Zavést pravidlo, že každá nová nebo revidovaná feature má vlastní adresář `features/NNN_name`.
- [x] Přesunout ověřenou weather akci do `actions/001_weather`.
- [x] Aktualizovat importy, katalog nástrojů a dokumentaci.
- [x] Ověřit syntaxi a importy.
- [x] Zapsat výsledek do historie.

## ARCH-003 — Sdílený základ a specializované profily

Stav: `DONE`

- [x] Zapsat pravidlo pro společný základ asistenta.
- [x] Zapsat pravidlo pro budoucí specializované kopie/profily agenta.
- [x] Založit dokumentaci pro profily agenta.
- [x] Doplnit pravidla pro sdílené features a profilově volené actions.
- [x] Ověřit strukturu dokumentace.
- [x] Zapsat výsledek do historie.

## ARCH-004 — Telegram jako klientský kanál nad backendem agenta

Stav: `DONE`

- [x] Zapsat rozhodnutí, že Telegram bridge není dashboardový přepisovač, ale samostatný klientský kanál k backendu agenta.
- [x] Zapsat pravidlo, že Desktop UI, Telegram a budoucí klienti mají sdílet stejný agentní runtime.
- [x] Aktualizovat dokumentaci Telegram feature podle tohoto pravidla.
- [x] Zapsat výsledek do historie.

## ARCH-005 — Základ serverové architektury FastAPI/PostgreSQL

Stav: `DONE`

- [x] Zapsat architektonické rozhodnutí pro backend FastAPI, Uvicorn a PostgreSQL.
- [x] Založit backend balíček oddělený od současné desktop aplikace.
- [x] Přidat základní health/status endpointy pro budoucí mobilní frontend.
- [x] Připravit konfigurační proměnné pro server a PostgreSQL.
- [x] Aktualizovat závislosti a dokumentaci spuštění backendu.
- [x] Ověřit syntaxi nových backend modulů.
- [x] Zapsat výsledek do historie.

## ARCH-006 — Migrační plán a první agentní runtime kontrakt

Stav: `DONE`

- [x] Založit `docs/MIGRATION_PLAN.md` jako samostatný plán migrace.
- [x] Popsat fáze migrace backendu, PostgreSQL a mobilních klientů.
- [x] Přidat backend službu pro první agentní runtime kontrakt.
- [x] Napojit `POST /api/v1/messages` na agentní runtime službu.
- [x] Aktualizovat dokumentaci backendu.
- [x] Ověřit syntaxi a API smoke testy.
- [x] Zapsat výsledek do historie.

## ARCH-007 — Sdílený model konverzační relace v backendu

Stav: `DONE`

- [x] Přidat backend modely pro relaci a uloženou zprávu.
- [x] Přidat dočasné in-memory úložiště relací pro fázi před PostgreSQL.
- [x] Napojit `POST /api/v1/messages` na relace podle `conversation_id`, `client_id` a `channel`.
- [x] Přidat endpoint pro načtení konverzační relace.
- [x] Aktualizovat `docs/MIGRATION_PLAN.md` a `backend/README.md`.
- [x] Ověřit syntaxi a API smoke testy.
- [x] Zapsat výsledek do historie.

## ARCH-008 — Repository rozhraní pro konverzační persistenci

Stav: `DONE`

- [x] Oddělit repository rozhraní od in-memory implementace konverzací.
- [x] Přidat factory pro volbu conversation repository.
- [x] Zachovat in-memory fallback bez `DATABASE_URL`.
- [x] Aktualizovat `docs/MIGRATION_PLAN.md` a backend dokumentaci.
- [x] Ověřit syntaxi a API smoke testy.
- [x] Zapsat výsledek do historie.

## ARCH-009 — SQLAlchemy 2.0 modely pro konverzační data

Stav: `DONE`

- [x] Přidat SQLAlchemy 2.0 declarative base pro backend databázovou vrstvu.
- [x] Přidat ORM modely `Client`, `Conversation` a `Message`.
- [x] Definovat vazby, indexy a timestamp sloupce pro PostgreSQL persistenci.
- [x] Aktualizovat `docs/MIGRATION_PLAN.md` a backend dokumentaci.
- [x] Ověřit syntaxi a kompilaci SQLAlchemy metadata.
- [x] Zapsat výsledek do historie.

## FEAT-001 — ElevenLabs hlasový provider

Stav: `DONE`

- [x] Založit `features/001_elevenlabs_voice`.
- [x] Přidat konfiguraci přes `.env` a `.env.example`.
- [x] Přidat modul pro syntézu textu do audio souboru.
- [x] Doplnit dokumentaci feature a pravidla použití.
- [x] Ověřit syntaxi a bezpečný smoke test bez API volání.
- [x] Zapsat výsledek do historie.

## UI-001 — Dashboardový přepínač hlasu

Stav: `DONE`

- [x] Přidat přepínač hlasu vlevo dole v dashboardu.
- [x] Napojit přepínač na existující ukládání `JARVIS_VOICE`.
- [x] Synchronizovat přepínač s hlasem v nastavení.
- [x] Ověřit syntaxi `ui.py`.
- [x] Zapsat výsledek do historie.

## UI-002 — Oprava přepínání hlasu za běhu

Stav: `DONE`

- [x] Napojit callback `on_voice_change` z UI do `main.py`.
- [x] Po změně hlasu obnovit živou Gemini session s novým hlasem.
- [x] Zobrazit uživateli stav změny hlasu.
- [x] Ověřit syntaxi `main.py` a `ui.py`.
- [x] Zapsat výsledek do historie.

## UI-003 — Přepínač hlasového provideru v dashboardu

Stav: `DONE`

- [x] Přidat přepínač `Gemini / ElevenLabs` do dashboardu.
- [x] Přidat stejnou volbu do panelu nastavení.
- [x] Ukládat volbu do `JARVIS_VOICE_PROVIDER`.
- [x] Po změně provideru obnovit živou relaci.
- [x] Ověřit syntaxi `main.py`, `ui.py` a konfiguraci.
- [x] Zapsat výsledek do historie.

## UI-004 — Hlasové nastavení pouze v panelu nastavení

Stav: `DONE`

- [x] Odstranit hlasový selector z levého dolního rohu dashboardu.
- [x] Ponechat nastavování hlasu a provideru pouze v panelu nastavení.
- [x] Filtrovat nabídku hlasů podle vybraného provideru.
- [x] U Gemini zobrazovat pouze Gemini hlasy.
- [x] U ElevenLabs zobrazovat pouze hlas z `ELEVENLABS_VOICE_ID`.
- [x] Ověřit syntaxi `ui.py`, `main.py` a konfiguraci.
- [x] Zapsat výsledek do historie.

## UI-005 — Spouštění dashboardu v samostatném okně

Stav: `DONE`

- [x] Změnit výchozí start dashboardu z fullscreen režimu na běžné samostatné okno.
- [x] Povolit zmenšení okna na menší použitelné rozměry.
- [x] Přepočítávat layout při ruční změně velikosti okna.
- [x] Zachovat ruční přepnutí fullscreen režimu přes klávesové zkratky.
- [x] Ověřit syntaxi `ui.py`.
- [x] Zapsat výsledek do historie.

## FEAT-002 — ElevenLabs jako živý hlasový výstup

Stav: `DONE`

- [x] Rozšířit ElevenLabs provider o syntézu do audio bytes.
- [x] Přidat konfiguraci hlasového provideru `auto/gemini/elevenlabs`.
- [x] Přepnout Gemini Live na textový režim při použití ElevenLabs.
- [x] Přehrávat ElevenLabs PCM audio přes `pyaudio`.
- [x] Ověřit syntaxi a bezpečné integrační části bez reálného API volání.
- [x] Zapsat výsledek do historie.

## FEAT-003 — Stabilizace výchozího hlasového provideru

Stav: `DONE`

- [x] Upravit režim `auto`, aby sám nepřepínal stabilní Gemini Live výstup na ElevenLabs.
- [x] Zachovat možnost výslovně zapnout ElevenLabs přes `JARVIS_VOICE_PROVIDER="elevenlabs"`.
- [x] Aktualizovat dokumentaci feature.
- [x] Ověřit syntaxi a bezpečný smoke test konfigurace.
- [x] Zapsat výsledek do historie.

## FEAT-004 — Oprava ElevenLabs režimu pro native audio model

Stav: `DONE`

- [x] Nepoužívat `response_modalities=["TEXT"]` s native audio modelem.
- [x] V ElevenLabs režimu zachovat Live audio výstup s přepisem odpovědi.
- [x] Nepřehrávat ani nefrontovat nativní Gemini audio, pokud je aktivní ElevenLabs.
- [x] Potlačit očekávanou chybu zavření session při přepnutí provideru.
- [x] Ověřit syntaxi a sestavení Live konfigurace.
- [x] Zapsat výsledek do historie.

## FEAT-005 — Fallback při nedostupném ElevenLabs účtu

Stav: `DONE`

- [x] Rozpoznat chybu `402 Payment Required` z ElevenLabs TTS API.
- [x] Zobrazit srozumitelnou českou hlášku bez technického URL.
- [x] Přepnout hlasový provider zpět na Gemini Live a obnovit relaci.
- [x] Aktualizovat dokumentaci ElevenLabs feature.
- [x] Ověřit syntaxi a bezpečný smoke test bez reálného API volání.
- [x] Zapsat výsledek do historie.

## FEAT-006 — Telegram bridge pro textovou komunikaci

Stav: `DONE`

- [x] Založit `features/002_telegram_bridge`.
- [x] Přidat konfiguraci přes `.env` a `.env.example`.
- [x] Implementovat Telegram long polling přes Bot API.
- [x] Omezit přístup přes allowlist chat ID.
- [x] Napojit textové Telegram zprávy na běžící Gemini Live session.
- [x] Přijímat hlasové zprávy a připravit místo pro navazující STT krok.
- [x] Aktualizovat dokumentaci feature.
- [x] Ověřit syntaxi a bezpečné smoke testy bez reálného Telegram API volání.
- [x] Zapsat výsledek do historie.

## FEAT-007 — Telegram bridge pro hlasové zprávy a servisní příkazy

Stav: `DONE`

- [x] Přidat servisní Telegram příkazy pro ověření bota a zjištění `chat_id`.
- [x] Přepisovat Telegram hlasové zprávy do textu přes Gemini.
- [x] Předat přepsaný text do stejné agentní cesty jako textovou Telegram zprávu.
- [x] Aktualizovat `.env.example` a dokumentaci feature.
- [x] Ověřit syntaxi a bezpečné smoke testy bez reálného Telegram API volání.
- [x] Zapsat výsledek do historie.

## FEAT-008 — Telegram hlasové odpovědi podle typu vstupu

Stav: `DONE`

- [x] Zachovat textovou odpověď pro textové Telegram dotazy.
- [x] U hlasových Telegram dotazů převést odpověď agenta na audio soubor.
- [x] Odeslat audio odpověď zpět do Telegramu.
- [x] Přidat textový fallback, pokud TTS není nakonfigurované nebo selže.
- [x] Aktualizovat dokumentaci feature.
- [x] Ověřit syntaxi a bezpečné smoke testy bez reálného Telegram API volání.
- [x] Zapsat výsledek do historie.

## FEAT-009 — Dočasné vypnutí ElevenLabs runtime feature

Stav: `DONE`

- [x] Vynutit Gemini Live jako jediný aktivní hlasový provider v runtime.
- [x] Skrýt nebo deaktivovat ElevenLabs volbu v dashboardu.
- [x] U Telegram hlasových dotazů vracet textový fallback místo ElevenLabs audio odpovědi.
- [x] Aktualizovat dokumentaci ElevenLabs a Telegram feature.
- [x] Ověřit syntaxi a bezpečné smoke testy bez externího API volání.
- [x] Zapsat výsledek do historie.

## FEAT-010 — Opětovné zapnutí ElevenLabs runtime feature

Stav: `DONE`

- [x] Znovu povolit ElevenLabs runtime v backendu aplikace.
- [x] Vrátit ElevenLabs provider do panelu nastavení dashboardu.
- [x] Obnovit ElevenLabs audio odpovědi pro hlasové Telegram dotazy.
- [x] Aktualizovat dokumentaci ElevenLabs a Telegram feature.
- [x] Ověřit syntaxi a bezpečné smoke testy bez externího API volání.
- [x] Zapsat výsledek do historie.

## FEAT-011 — Oprava Telegram hlasových odpovědí přes ElevenLabs

Stav: `DONE`

- [x] Zabránit lokálnímu přehrání odpovědi, která patří externímu Telegram dotazu.
- [x] Přidat záložní formát pro Telegram audio odpověď, pokud MP3 syntéza selže.
- [x] Zpřesnit diagnostiku selhání ElevenLabs TTS.
- [x] Ověřit syntaxi a bezpečné smoke testy bez externího API volání.
- [x] Zapsat výsledek do historie.

## FEAT-012 — Windows TTS fallback pro Telegram hlasové odpovědi

Stav: `DONE`

- [x] Přidat lokální Windows SAPI fallback pro Telegram hlasové odpovědi.
- [x] Zachovat ElevenLabs jako primární TTS cestu pro Telegram.
- [x] Zapsat do debug logu důvody selhání jednotlivých TTS cest.
- [x] Aktualizovat dokumentaci Telegram bridge.
- [x] Ověřit syntaxi a bezpečné smoke testy bez externího API volání.
- [x] Zapsat výsledek do historie.

## FEAT-013 — Gemini Live hlas pro Telegram odpovědi

Stav: `DONE`

- [x] Odpojit Windows TTS fallback pro Telegram hlasové odpovědi.
- [x] U Gemini provideru ukládat Live audio odpověď do WAV souboru pro Telegram.
- [x] Zachovat ElevenLabs syntézu pouze při aktivním ElevenLabs provideru.
- [x] Zabránit lokálnímu přehrání audio odpovědi určené pro Telegram.
- [x] Aktualizovat dokumentaci Telegram bridge.
- [x] Ověřit syntaxi a bezpečné smoke testy bez externího API volání.
- [x] Zapsat výsledek do historie.

## SEC-001 — Citlivá konfigurace v `.env`

Stav: `DONE`

- [x] Zmapovat čtení a zápis API klíčů a související konfigurace.
- [x] Přidat kořenový `.env` a bezpečnou šablonu `.env.example`.
- [x] Převést `app_config.py` z JSON na proměnné prostředí.
- [x] Zachovat ukládání nastavení z grafického rozhraní.
- [x] Jednorázově migrovat existující hodnoty a odstranit starý JSON.
- [x] Aktualizovat `.gitignore` a instalační skript.
- [x] Ověřit syntaxi, migraci a načítání bez zveřejnění hodnot.
