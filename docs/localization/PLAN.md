# Plán české lokalizace

Aktualizováno: 2026-06-14

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
- [x] Přeložit `actions/weather.py`.
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

## SEC-001 — Citlivá konfigurace v `.env`

Stav: `DONE`

- [x] Zmapovat čtení a zápis API klíčů a související konfigurace.
- [x] Přidat kořenový `.env` a bezpečnou šablonu `.env.example`.
- [x] Převést `app_config.py` z JSON na proměnné prostředí.
- [x] Zachovat ukládání nastavení z grafického rozhraní.
- [x] Jednorázově migrovat existující hodnoty a odstranit starý JSON.
- [x] Aktualizovat `.gitignore` a instalační skript.
- [x] Ověřit syntaxi, migraci a načítání bez zveřejnění hodnot.
