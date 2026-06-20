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

## ADR-007 — Lokální SQLite paměť konverzací

Datum: 2026-06-16
Stav: `ACCEPTED`

### Kontext

Původní paměť asistenta ukládala pouze explicitně vybrané informace do lokálního
JSON souboru. Neuchovávala průběh konverzací, neuměla transakční zápis a při
růstu dat by bylo neefektivní vkládat celou paměť do systémového promptu.

### Rozhodnutí

Paměť se začne ukládat do lokální SQLite databáze v adresáři `memory`. První
krok zachová stávající rozhraní pro dlouhodobé fakty a doplní ukládání
konverzačních turnů. Vektorové embeddingy a sémantické vyhledávání budou
navazující rozšíření nad stejným lokálním úložištěm.

### Důsledky

- Databázový soubor je lokální runtime data a nesmí se verzovat.
- Současné nástroje `save_memory` a `delete_memory` zůstanou kompatibilní.
- Do promptu se zatím stále vkládají dlouhodobé fakty; výběr relevantní paměti
  podle dotazu bude řešen v dalším kroku.
- Budoucí vektorový index musí respektovat lokální charakter dat a nesmí
  vyžadovat externí službu jako povinnou závislost.

## ADR-008 — Oddělení krátkodobé paměti a dlouhodobých rozhodnutí

Datum: 2026-06-17
Stav: `ACCEPTED`

### Kontext

Provozní konverzace a trvalá rozhodnutí mají rozdílnou hodnotu i životnost.
Konverzační záznamy slouží pro krátkodobou návaznost a vyhledávání, zatímco
potvrzená rozhodnutí mají charakter pravidel podobný projektovým ADR a nesmí se
automaticky ztrácet.

### Rozhodnutí

Provozní konverzační turny se ukládají do krátkodobé paměti a mohou být
automaticky mazány po jednom měsíci. Dlouhodobá rozhodnutí se ukládají do
samostatné tabulky až po výslovném návrhu a potvrzení uživatelem. Tato
dlouhodobá rozhodnutí se automaticky nepromazávají.

### Důsledky

- Krátkodobá paměť je vhodná pro běžné konverzační souvislosti, ladicí dohled a
  budoucí sémantické vyhledávání.
- Dlouhodobá paměť rozhodnutí je stabilní kontext a musí být v promptu oddělena
  od běžných faktů.
- Změna nebo zrušení dřívějšího rozhodnutí se má provést novým potvrzeným
  rozhodnutím, nikoli automatickým přepsáním historie.

## ADR-009 — Akční moduly jako místo pro funkce asistenta

Datum: 2026-06-17
Stav: `ACCEPTED`

### Kontext

Asistent bude postupně dostávat další schopnosti, volání funkcí a případně
specializované agentní integrace. Bez jednotného místa by se implementace
rozptýlila mezi `main.py`, prompt, UI a pomocné moduly, což by ztížilo revizi,
testování a zapojování nových nástrojů.

### Rozhodnutí

Všechny nové schopnosti asistenta, které mají být volané jako funkce modelu
nebo jako integrační/agentní akce, se implementují ve složce `actions`.
`main.py` zůstává registr nástrojů, dispatcher a orchestrace běhu; nemá
obsahovat vlastní doménovou logiku nové funkce.

### Důsledky

- Každá nová schopnost má mít samostatný modul nebo jasně související rozšíření
  existujícího modulu v `actions`.
- Nový nástroj musí být zapojen do deklarací nástrojů v `main.py`, dispatcheru a
  podle potřeby do `core/prompt.txt`.
- Nové externí závislosti se zapisují do `requirements.txt` a musí mít
  ověřitelný fallback nebo srozumitelnou chybovou zprávu.
- Akční moduly musí být testovatelné izolovaně bez spuštění celé živé relace.

## ADR-010 — Číslování ověřených akčních modulů

Datum: 2026-06-17
Stav: `ACCEPTED`

### Kontext

Akční moduly budou procházet postupnou revizí. Po ověření má být na první
pohled vidět, které moduly už revizí prošly. Současně musí zůstat zachovaný
standardní Python import v `main.py`.

### Rozhodnutí

Ověřené akční moduly se přejmenovávají do importovatelného tvaru
`_NNN_nazev.py`, například `_001_weather.py`. Čistý tvar `1_weather.py` se
nepoužívá, protože název modulu začínající číslicí nelze běžně importovat
zápisem `from actions.1_weather import ...`.

### Důsledky

- Po přejmenování modulu se vždy aktualizují importy v `main.py` a případné
  další reference.
- Číslo znamená, že modul prošel revizí a základním ověřením.
- Neočíslované moduly zůstávají čekající na revizi.

## ADR-011 — Katalog popisů nástrojů pro agenta

Datum: 2026-06-17
Stav: `ACCEPTED`

### Kontext

Agent potřebuje ke každému nástroji jasný popis, kdy ho má použít, jaké
parametry očekává a jaká má známá omezení. Pokud jsou tyto informace pouze v
`main.py`, promptu nebo komentářích u implementace, snadno se při přidávání
dalších funkcí rozcházejí.

### Rozhodnutí

Popisy nástrojů volaných agentem se ukládají do katalogu `actions/tool_catalog.py`.
Katalog obsahuje strojovou deklaraci pro model i doplňující poznámky pro revizi:
modul, funkci, stav ověření, příklady použití, doporučené situace pro volání a
známá omezení. Při vytvoření nebo zapojení nové akce musí vzniknout odpovídající
záznam v katalogu.

### Důsledky

- `actions` je nejen místo implementace akcí, ale i místo jejich popisu pro agenta.
- Nová akce není považovaná za dokončenou, dokud nemá záznam v
  `actions/tool_catalog.py`.
- `main.py` má používat katalog jako zdroj deklarací nástrojů vždy, když je daná
  akce do katalogu doplněna.
- Prompt může obsahovat stručné shrnutí schopností, ale detailní pravidla pro
  volání konkrétních funkcí se drží v katalogu.
- U ověřených akcí musí katalog uvádět také známá omezení, aby agent nevolal
  funkci pro scénáře, které zatím neumí pokrýt.

## ADR-012 — Oddělení nástrojů a běhových vlastností asistenta

Datum: 2026-06-17
Stav: `ACCEPTED`

### Kontext

Projekt bude kromě nástrojů volaných agentem obsahovat také komunikační kanály,
hlasové moduly a další běhové integrace. Telegram bridge nebo hlasový provider
ElevenLabs nejsou nástroje, které má model volat kvůli splnění uživatelského
úkolu; jsou to způsoby, jak se k agentovi připojit nebo jak agent vstup/výstup
zpracuje.

### Rozhodnutí

Adresář `actions` obsahuje pouze tools, tedy funkce volané agentem přes
tool/function calling. Běhové vlastnosti asistenta, komunikační kanály,
hlasové moduly, bridge adaptéry a poskytovatelé služeb se ukládají do adresáře
`features`.

### Důsledky

- Telegram bridge patří do `features`, ne do `actions`.
- Budoucí hlasový modul ElevenLabs patří do `features`, pokud nebude sám
  vystavený jako nástroj volaný agentem.
- Pokud některá běhová vlastnost zároveň nabídne agentovi nový nástroj, její
  volatelná akce musí být oddělena do `actions` a popsána v
  `actions/tool_catalog.py`.
- `actions/tool_catalog.py` zůstává katalogem pouze pro nástroje dostupné
  agentovi, ne pro všechny interní integrace projektu.

## ADR-013 — Číslované podadresáře pro akce a běhové vlastnosti

Datum: 2026-06-17
Stav: `ACCEPTED`

### Kontext

Některé akce a běhové vlastnosti mohou časem obsahovat více souborů: vlastní
implementaci, testy, dokumentaci, konfigurační šablony, pomocné adaptéry nebo
assets. Jednosouborové ukládání v kořeni `actions` by se u složitějších funkcí
rychle stalo nepřehledné.

### Rozhodnutí

Nové a revidované akce se ukládají do vlastních číslovaných podadresářů ve tvaru
`actions/NNN_name`, například `actions/001_weather`. Nové a revidované běhové
vlastnosti se ukládají stejným způsobem do `features/NNN_name`. Jednotlivé
soubory implementace, dokumentace a podpůrných částí se ukládají až uvnitř
daného podadresáře.

Číslovaný adresář může začínat číslicí, protože se nebude importovat přímým
syntaktickým zápisem `from actions.001_weather ...`. Kód používá import přes
loader nebo `importlib`, například modulovou cestu `actions.001_weather.weather`.

### Důsledky

- ADR-010 o jednosouborovém tvaru `_NNN_name.py` je pro nové změny nahrazeno tímto
  adresářovým pravidlem.
- Ověřená weather akce je uložena v `actions/001_weather`.
- `actions/tool_catalog.py` musí u každého nástroje ukazovat na skutečný modul
  uvnitř číslovaného podadresáře.
- Starší ploché soubory v `actions` jsou legacy stav a budou se přesouvat do
  číslovaných podadresářů postupně při revizi dané akce.
- Každý nový `features/NNN_name` adresář má nést vlastní dokumentaci nebo jasný
  vstupní modul podle povahy feature.

## ADR-014 — Sdílený základ a specializované profily agentů

Datum: 2026-06-17
Stav: `ACCEPTED`

### Kontext

Projekt má nejdříve dozrát do stabilního obecného asistenta s dobře odděleným
jádrem, pamětí, actions a features. Později budou vznikat samostatné kopie
zaměřené na konkrétní účel. Tyto kopie nemají znovu vymýšlet runtime základ; mají
se lišit hlavně promptem, výběrem actions a zapnutými features.

### Rozhodnutí

Společný základ projektu obsahuje runtime jádro, paměť, konfiguraci, sdílené
features, obecný prompt a pravidla pro actions. Specializace agenta se popisuje
profilem v adresáři `profiles/NNN_name`. Profil určuje vlastní `prompt.txt`,
výběr povolených tools z `actions/tool_catalog.py` a výběr zapnutých features.

Samostatné kopie projektu se mají vytvářet až po stabilizaci společného základu.
Kopie má převzít pouze potřebné actions, relevantní features a vlastní prompt
podle zaměření agenta.

### Důsledky

- `features` jsou sdílená runtime vrstva, ne místo pro doménové zaměření agenta.
- Doménové schopnosti, které model přímo volá, zůstávají v `actions`.
- `profiles` popisují kombinaci promptu, povolených tools a zapnutých features.
- Budoucí specializovaná kopie má být odvozená z profilu, ne ručně rozbitá
  úpravami napříč nesouvisejícími soubory.
- Aktuální aplikace zatím používá `core/prompt.txt`; profilový loader bude
  samostatný navazující krok.

## ADR-015 — Komunikační kanály jako klienti nad agentním backendem

Datum: 2026-06-19
Stav: `ACCEPTED`

### Kontext

Telegram má sloužit jako plnohodnotný způsob komunikace s agentem z libovolného
zařízení, ne jako přepisovač textu do dashboardu. Stejný agent má být dostupný
přes desktopové UI, Telegram a později případné další klienty, aniž by každé
rozhraní mělo vlastní kopii rozhodovací logiky, actions, paměti nebo promptu.

### Rozhodnutí

Komunikační kanály se navrhují jako klienti nad sdíleným agentním backendem.
Desktop UI, Telegram bridge a budoucí webové nebo mobilní rozhraní mají posílat
vstupy do stejného agentního runtime a přijímat z něj odpovědi. Telegram bridge
zůstává běhová feature v `features`, protože nejde o tool volaný modelem přes
function calling.

### Důsledky

- Telegram bridge se nesmí navrhovat jako pouhý přepisovač dashboardu.
- Sdílené chování agenta, včetně promptu, actions, paměti a orchestrace odpovědi,
  má být postupně oddělováno od konkrétního UI.
- `main.py` může dočasně obsahovat napojení existujících klientů, ale nová
  architektura má směřovat k explicitnímu agentnímu runtime rozhraní.
- Nový komunikační klient patří do `features/NNN_name` a má používat sdílený
  runtime, ne vlastní paralelní implementaci agenta.
- Pokud klient zároveň zpřístupní modelu nový nástroj, tato volatelná část musí
  být samostatně v `actions` a musí mít záznam v `actions/tool_catalog.py`.

## ADR-016 — Serverový backend pro mobilní a víceklientskou architekturu

Datum: 2026-06-19
Stav: `ACCEPTED`

### Kontext

Současná aplikace vznikla jako desktopový Windows runtime s UI, hlasovým vstupem,
Telegram bridge, actions a pamětí napojenými převážně přes `main.py`. Pro budoucí
mobilní klienty, například Flutter aplikaci, webové rozhraní a více paralelních
komunikačních kanálů je potřeba explicitní serverová vrstva, která nebude závislá
na desktopovém okně.

### Rozhodnutí

Projekt se bude postupně migrovat na architekturu se serverovým backendem nad
FastAPI spuštěným přes Uvicorn. Backend bude poskytovat HTTP/WebSocket API pro
klienty a bude cílovým místem pro sdílený agentní runtime, správu konverzací,
stav klientů a persistenci. PostgreSQL bude cílová relační databáze pro sdílená
runtime data. Stávající lokální SQLite paměť zůstává kompatibilní přechodová
vrstva, dokud nebude bezpečně migrována.

### Důsledky

- Nový serverový kód patří do samostatného balíčku `backend`, ne do `main.py`.
- Desktop UI, Telegram bridge a budoucí Flutter klient mají směřovat k API nad
  backendem, ne k vlastní kopii agentní logiky.
- První migrační kroky nesmí rozbít současný desktopový běh; backend se zavádí
  paralelně a postupně přebírá odpovědnost.
- PostgreSQL konfigurace patří do `.env`; skutečné connection stringy se nesmí
  zapisovat do dokumentace ani verzovaných souborů.
- API endpointy mají používat stabilní verzi v cestě, například `/api/v1/...`,
  aby budoucí mobilní klienti nebyli vázaní na interní refaktoring.
