# Projektová rozhodnutí

Tento soubor eviduje důležitá rozhodnutí s dopadem na celý projekt. Používá
zjednodušený formát ADR (Architecture Decision Record).

## Pravidla vedení

- Každé rozhodnutí má stabilní identifikátor ve formátu `ADR-NNN`.
- Přijatá rozhodnutí se zpětně nemažou.
- Změnu rozhodnutí popiš novým ADR, které původní záznam označí jako
  `SUPERSEDED`.
- Menší implementační detaily patří do plánu nebo historie, nikoli sem.
- Nové rozhodnutí přidej na konec souboru.

## Stavové hodnoty

- `PROPOSED` — návrh čeká na schválení.
- `ACCEPTED` — rozhodnutí je platné.
- `DEPRECATED` — rozhodnutí se již nedoporučuje, ale může být stále použité.
- `SUPERSEDED` — rozhodnutí bylo nahrazeno novějším ADR.
- `REJECTED` — návrh nebyl přijat.

## Šablona

```markdown
## ADR-NNN — Název

Datum: RRRR-MM-DD
Stav: `PROPOSED`

### Kontext

Problém, omezení a důvod rozhodnutí.

### Rozhodnutí

Jednoznačný popis zvoleného řešení.

### Důsledky

Pozitivní i negativní dopady a následná práce.
```

## ADR-001 — Čeština jako výchozí jazyk aplikace

Datum: 2026-06-14
Stav: `ACCEPTED`

### Kontext

Původní aplikace používá turecké uživatelské texty a turecký systémový prompt.
Cílovým prostředím této varianty je český uživatel ve Windows.

### Rozhodnutí

Výchozím jazykem uživatelského rozhraní, systémového promptu, hlasových
odpovědí a provozních hlášek je čeština. Pokud uživatel komunikuje jiným
jazykem, asistent může odpovědět v tomto jazyce.

### Důsledky

- Všechny nové uživatelské texty musí být primárně české.
- Existující turecké texty budou postupně přeloženy podle lokalizačního plánu.
- Přirozenost českého textu má přednost před doslovným překladem.

## ADR-002 — Technické identifikátory se nelokalizují

Datum: 2026-06-14
Stav: `ACCEPTED`

### Kontext

Nástroje Gemini a integrační moduly používají pevné názvy funkcí, polí, stavů
a strojových hodnot. Jejich překlad by porušil smlouvy mezi moduly.

### Rozhodnutí

Názvy funkcí, nástrojů, API polí, interních stavů a strojových hodnot zůstávají
beze změny. Lokalizují se pouze texty určené uživateli a popisy předávané
modelu, pokud nejsou součástí strojového rozhraní.

### Důsledky

- Hodnoty jako `today`, `battery`, `active_window` nebo `LISTENING` zůstávají
  v původní podobě.
- České pokyny se mapují na existující technické hodnoty.
- Překlad musí být ověřen proti volajícím a návratovým hodnotám.

## ADR-003 — Povinná průběžná dokumentace změn

Datum: 2026-06-14
Stav: `ACCEPTED`

### Kontext

Lokalizace zasahuje více modulů a návratové texty mohou ovlivňovat chování
aplikace. Bez průběžného záznamu by nebylo možné spolehlivě kontrolovat rozsah,
stav a důvody změn.

### Rozhodnutí

Každá změna zdrojového kódu, konfigurace nebo lokalizace musí aktualizovat
příslušný plán a historii. Rozhodnutí s dopadem na celý projekt se zapisují do
tohoto souboru.

### Důsledky

- Nezdokumentovaná změna se nepovažuje za dokončenou.
- Historie a přijatá ADR jsou append-only.
- Před implementací je nutné zkontrolovat platná projektová rozhodnutí.

## ADR-004 — Oddělení textové lokalizace a hlasových výstupů

Datum: 2026-06-14
Stav: `ACCEPTED`

### Kontext

Texty rozhraní, návratové zprávy nástrojů a hlasové výstupy mají rozdílné
způsoby ověření. Současná změna má odstranit turecké texty z aplikace, zatímco
volba hlasu, výslovnost a TTS budou řešeny samostatně.

### Rozhodnutí

Nejprve se přeloží všechny textové výstupy, UI a návratové zprávy do češtiny.
Konfigurace hlasu, TTS moduly a ověření české výslovnosti se provedou v
samostatném následném kroku.

### Důsledky

- `actions/tts.py` a nastavení hlasu se v textové fázi funkčně nemění.
- Textový obsah systémového promptu zůstává český.
- Regresní test hlasové odpovědi se uzavře až po dokončení hlasového kroku.

## ADR-005 — České regionální výchozí hodnoty

Datum: 2026-06-14
Stav: `ACCEPTED`

### Kontext

Původní projekt používal jako výchozí lokalitu počasí Istanbul a lokální
telefonní čísla automaticky převáděl na tureckou předvolbu `+90`. To je v české
variantě matoucí a u WhatsApp kontaktů také funkčně chybné.

### Rozhodnutí

Výchozí lokalitou počasí je Praha. Devítimístná lokální telefonní čísla se
normalizují s českou předvolbou `+420`.

### Důsledky

- Lokalitu počasí lze nadále přepsat argumentem nebo proměnnou
  `JARVIS_WEATHER_LOCATION`.
- Mezinárodní telefonní čísla zadaná s předvolbou zůstávají beze změny.
- Ukázkové texty a výchozí karty UI používají Prahu.

## ADR-006 — Citlivá konfigurace pouze v lokálním `.env`

Datum: 2026-06-14
Stav: `ACCEPTED`

### Kontext

API klíče byly ukládány v `config/api_keys.json`. Přestože byl soubor ignorován
Gitem, samostatný JSON s tajnými hodnotami zvyšoval riziko nechtěného zveřejnění
a neodpovídal běžnému způsobu předávání tajné konfigurace aplikaci.

### Rozhodnutí

API klíče a lokální konfigurační hodnoty aplikace se ukládají do kořenového
souboru `.env`, který nesmí být verzován. Repozitář obsahuje pouze
`.env.example` bez tajných hodnot. Proměnné nastavené operačním systémem mají
při spuštění přednost před hodnotami v souboru.

### Důsledky

- `config/api_keys.json` se po úspěšné migraci odstraní.
- Nastavení v grafickém rozhraní zapisuje spravované hodnoty do `.env`.
- Instalační skript vytváří `.env` z bezpečné šablony.
- Skutečné klíče se nesmí zapisovat do dokumentace, logů ani ukázkových souborů.
