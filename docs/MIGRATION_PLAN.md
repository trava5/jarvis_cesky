# Migrační plán backendové architektury

Tento plán popisuje postupnou migraci projektu JARVIS z desktopově řízené
aplikace na víceklientskou architekturu s backendem FastAPI, Uvicorn a
PostgreSQL. Cílem je zachovat funkční desktopovou aplikaci a postupně umožnit
napojení Telegramu, webu a mobilního frontendu, například Flutter aplikace.

## Principy migrace

- Současný desktopový běh se nesmí rozbít kvůli backendovým krokům.
- Nový serverový kód patří do balíčku `backend`.
- Desktop UI, Telegram a mobilní klient mají postupně používat stejný agentní
  runtime kontrakt.
- PostgreSQL je cílová databáze pro sdílená runtime data; současná SQLite paměť
  zůstává přechodová vrstva.
- API pro klienty používá verzovaný prefix `/api/v1`.
- Skutečné klíče, tokeny a databázové connection stringy zůstávají pouze v
  lokálním `.env`.

## Fáze migrace

| ID | Název | Stav | Výsledek |
|---|---|---|---|
| MIG-001 | Agentní runtime kontrakt | DONE | Backend přijímá textovou zprávu přes `/api/v1/messages` a vrací stabilní odpověďový model. |
| MIG-002 | Sdílená konverzační relace | DONE | Zavedení `conversation_id`, `client_id`, `channel` a jednotného modelu zpráv. |
| MIG-003 | PostgreSQL persistence | DONE | PostgreSQL repository a tabulky pro klienty, konverzace a zprávy. |
| MIG-004 | Migrace paměti | DONE | Krátkodobá paměť a dlouhodobá rozhodnutí jsou dostupná v backend storage vrstvě. |
| MIG-005 | Telegram přes backend | DONE | Telegram volá backend API jako první cestu; embedded backend s live handlerem vrací skutečnou odpověď agenta a fallback zůstává bezpečnostní záloha. |
| MIG-006 | Desktop přes backend | IN PROGRESS | Desktopový textový vstup volá backend API jako první cestu; audio/mikrofon zatím zůstává v `main.py`. |
| MIG-007 | Realtime WebSocket API | IN PROGRESS | Desktop text je realtime-first přes WebSocket eventy; audio stream je připravený jen v modelu události. |
| MIG-008 | Mobilní API kontrakt | TODO | Stabilní OpenAPI kontrakt pro Flutter klienta. |
| MIG-009 | Autentizace klientů | TODO | API tokeny nebo přihlášení klientů, oddělené od Telegram allowlistu. |

## MIG-001 — Agentní runtime kontrakt

Stav: `DONE`

První krok nezavádí plný přesun živé Gemini session z `main.py`. Cílem je vytvořit
serverový kontrakt, na který půjde bezpečně napojovat klienty a který později
dostane skutečnou agentní implementaci.

Kontrolní body:

- [x] Definovat request model pro textovou zprávu klienta.
- [x] Definovat response model pro odpověď agenta.
- [x] Přidat službu `AgentRuntime` jako mezivrstvu mezi API a budoucím agentem.
- [x] Napojit `POST /api/v1/messages` na `AgentRuntime`.
- [x] Vrátit řízený stav, pokud živý runtime ještě není připojený k backendu.
- [x] Ověřit API smoke testem.

## Očekávaný kontrakt zprávy

Klient pošle:

```json
{
  "text": "Ahoj, jaký je dnes plán?",
  "channel": "mobile",
  "client_id": "flutter-dev",
  "conversation_id": null,
  "want_audio": false
}
```

Backend vrátí:

```json
{
  "status": "runtime_unavailable",
  "message_id": "...",
  "conversation_id": "...",
  "text": "...",
  "audio_url": null,
  "detail": "..."
}
```

Stav `runtime_unavailable` je přechodový. Znamená, že API kontrakt funguje, ale
živý agentní runtime zatím běží v desktopové aplikaci a není připojený k backendu.

## MIG-002 — Sdílená konverzační relace

Stav: `DONE`

Tento krok zavádí jednotný model konverzační relace pro backend klienty. Relace je
zatím uložená pouze v paměti procesu, protože trvalá PostgreSQL persistence patří
do navazujícího kroku `MIG-003`.

Kontrolní body:

- [x] Přidat `ConversationSummary`, `ConversationDetail` a `StoredMessage`.
- [x] Přidat dočasné in-memory úložiště `ConversationStore`.
- [x] Při `POST /api/v1/messages` založit nebo najít relaci podle
  `conversation_id`.
- [x] Ukládat uživatelský turn a přechodovou odpověď asistenta do relace.
- [x] Přidat `GET /api/v1/conversations`.
- [x] Přidat `GET /api/v1/conversations/{conversation_id}`.
- [x] Ověřit API smoke testem.

Známé omezení:

- Relace se po restartu backendu ztratí. Trvalé uložení do PostgreSQL bude řešit
  `MIG-003`.

## MIG-003 — PostgreSQL persistence

Stav: `DONE`

Tento krok nahrazuje přímou závislost API na in-memory úložišti repository
rozhraním a následně přidá PostgreSQL implementaci. První podkrok je hotový:
endpointy už používají `ConversationRepository`, takže databázovou implementaci
půjde zapojit bez změny API kontraktu.

Kontrolní body:

- [x] Oddělit `ConversationRepository` rozhraní od in-memory implementace.
- [x] Přejmenovat dočasné úložiště na `InMemoryConversationRepository`.
- [x] Přidat factory pro volbu conversation repository.
- [x] Zachovat funkční API endpointy nad in-memory fallbackem.
- [x] Přidat SQLAlchemy modely pro `clients`, `conversations` a `messages`.
- [x] Přidat PostgreSQL implementaci repository.
- [x] Přidat inicializaci databázového schématu.
- [x] Přepnout repository factory na PostgreSQL při nastaveném `DATABASE_URL`.
- [x] Ověřit fallback bez databáze a PostgreSQL režim s databází.

Poznámka k ověření:

- Fallback bez databáze je ověřený.
- Režim s nastaveným `DATABASE_URL` zatím bezpečně přechází na in-memory fallback,
  pokud PostgreSQL připojení selže.
- Testovací připojení k lokální PostgreSQL databázi je funkční přes hodnoty z
  `.env`.
- Plný PostgreSQL smoke test ověřil vytvoření tabulek, zápis konverzace, zápis
  zpráv a čtení detailu relace přes backend API.

## MIG-004 — Migrace paměti

Stav: `DONE`

Tento krok přesouvá krátkodobou provozní paměť a dlouhodobá potvrzená rozhodnutí
do backend storage vrstvy. Současné veřejné funkce desktopové aplikace zůstávají
kompatibilní a lokální SQLite soubor zůstává přechodová vrstva pro starší běh.

Kontrolní body:

- [x] Přidat PostgreSQL modely pro krátkodobé turny a dlouhodobá rozhodnutí.
- [x] Přidat repository rozhraní pro paměť.
- [x] Přidat in-memory fallback bez databáze.
- [x] Přidat PostgreSQL implementaci repository.
- [x] Přidat backend API endpointy pro zápis, čtení, vyhledávání a promazání
  krátkodobé paměti.
- [x] Přidat backend API endpointy pro zápis a čtení dlouhodobých rozhodnutí.
- [x] Přidat idempotentní import současných SQLite záznamů.
- [x] Ověřit PostgreSQL zápis, čtení, vyhledávání a opakovaný import.

Poznámka:

- Běžné dlouhodobé faktické záznamy z `memory_items` zůstávají v kompatibilní
  lokální vrstvě a mohou být přesunuty v samostatném navazujícím kroku, pokud se
  rozhodne, že mají být sdílené mezi klienty stejně jako krátkodobé turny a
  potvrzená rozhodnutí.

## MIG-005 — Telegram přes backend

Stav: `DONE`

Tento krok postupně převádí Telegram bridge z přímého napojení na desktopový
runtime na klienta backendového API. První přípravná část sjednocuje výstup
Telegramu: bridge dál přijímá textové zprávy i hlasové zprávy přepsané přes Gemini,
ale odpověď do Telegramu je vždy textová.

Kontrolní body:

- [x] Zachovat příjem textových Telegram zpráv.
- [x] Zachovat příjem hlasových Telegram zpráv a jejich přepis do textu.
- [x] Odstranit odesílání hlasových/audio odpovědí přes Telegram.
- [x] Přidat backend klienta nebo adapter pro volání `/api/v1/messages`.
- [x] Přesměrovat Telegram textový vstup přes backend při zachování bezpečného
  desktopového fallbacku.
- [x] Přesměrovat přepsaný Telegram hlasový vstup přes stejnou backend cestu.
- [x] Ověřit konverzační relace, klientské ID a chování při nedostupném backendu.
- [x] Připojit živý agentní runtime přímo k backendu, aby desktopový fallback už
  nebyl potřeba.

Známé omezení:

- Samostatný backend spuštěný přes `python -m backend` bez embedded desktop handleru
  dál vrací `runtime_unavailable`. Skutečná odpověď agenta přes backend je dostupná,
  pokud běží desktopová aplikace s embedded backendem.
- Agentní orchestrace pořád fyzicky běží v desktopovém procesu. Další migrační
  kroky mají postupně přesunout desktop UI na backend a ztenčit `main.py`.

## MIG-006 — Desktop přes backend

Stav: `IN PROGRESS`

Tento krok převádí desktopové UI na klienta backendu po menších částech. První
hotová část přesměrovává textový vstup z dashboardu přes `POST /api/v1/messages`.
Současné audio, mikrofon, přehrávání a živá Gemini session zatím zůstávají v
`main.py`, protože realtime stream pro klienty bude samostatný krok `MIG-007`.

Kontrolní body:

- [x] Přidat obecného backend klienta pro `POST /api/v1/messages`.
- [x] Přesměrovat desktopový textový vstup přes backend s `channel="desktop"` a
  `client_id` ve tvaru `desktop:{session_id}`.
- [x] Ukládat a znovu používat backend `conversation_id` pro desktopovou textovou
  relaci.
- [x] Zachovat přímý fallback do současné Gemini Live session při vypnutém,
  nedostupném nebo přechodovém backendu.
- [x] Zachovat lokální audio/TTS pro desktopové backend požadavky a dál potlačovat
  lokální audio u Telegram požadavků.
- [ ] Přesunout další desktopové orchestrace z `main.py` za backend kontrakt.
- [x] Připravit realtime WebSocket kontrakt pro stav, text a audio.

Známá omezení:

- Desktopový text používá backend jako první cestu, ale embedded live handler pořád
  volá současnou agentní relaci v desktopovém procesu.
- Audio a mikrofonní smyčky ještě nejsou backend klienti. Jejich přesun bude záviset
  na `MIG-007`.

## MIG-007 — Realtime WebSocket API

Stav: `IN PROGRESS`

Tento krok zavádí realtime kontrakt pro klienty, které potřebují sledovat stav,
text a později audio bez dotazování HTTP endpointů. První hotová část přidává
WebSocket endpoint `GET/WS /api/v1/realtime` a backend event hub. Klient po
připojení dostane `hello` událost se `schema_version="realtime.v1"`.

Základní realtime událost má pole:

- `event_id`, `event_type`, `timestamp`,
- `channel`, `client_id`, `conversation_id`,
- `role`, `text`,
- `audio_mime_type`, `audio_base64`,
- `payload`.

Aktuálně používané typy událostí:

- `hello` — úvodní handshake po WebSocket připojení.
- `pong` — odpověď na klientský text `ping`.
- `runtime_state` — změna připojení živého agentního runtime.
- `message` — uložený uživatelský nebo asistentův textový turn.
- `audio` — rezervovaný typ pro navazující streamování audia.

Kontrolní body:

- [x] Definovat realtime event model pro stav, text a budoucí audio.
- [x] Přidat backend `RealtimeEventHub` pro připojené WebSocket klienty.
- [x] Přidat WebSocket endpoint `/api/v1/realtime`.
- [x] Doplnit realtime stav do `/api/v1/status`.
- [x] Publikovat `runtime_state` při připojení a odpojení live handleru.
- [x] Publikovat `message` eventy při zpracování `POST /api/v1/messages`.
- [x] Napojit desktop UI jako realtime klienta s deduplikací lokálních logů.
- [x] Postupně vypnout lokální logovací cesty tam, kde realtime eventy už pokrývají
  stejné chování.
- [ ] Přidat skutečné audio eventy nebo binární audio stream.
- [ ] Navrhnout klientské příkazy pro přerušení, mute/pause a stav přehrávání.

Známá omezení:

- WebSocket zatím pouze vysílá serverové události. Klientské řídicí příkazy kromě
  jednoduchého `ping` nejsou součástí kontraktu.
- Audio pole jsou připravená v modelu, ale backend zatím neposílá reálné audio
  bloky.
- Desktopový klient realtime eventy čte jako primární zdroj pro desktopové textové
  turny. Lokální logovací cesty v `main.py` zatím zůstávají pro hlas a fallbacky
  kvůli kompatibilitě audio běhu.
