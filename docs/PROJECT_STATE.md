# Stav projektu

Aktualizováno: 2026-06-21

Tento soubor slouží jako rychlý návratový bod po restartu stanice nebo vývojového
prostředí. Neobsahuje žádné hodnoty z `.env`, tokeny ani databázové connection
stringy.

## Aktuální směr

Projekt se postupně migruje z desktopově řízené Windows aplikace na víceklientskou
architekturu:

- backend: FastAPI + Uvicorn,
- cílová databáze: PostgreSQL,
- budoucí klienti: desktop UI, Telegram bridge, web a mobilní frontend, například
  Flutter,
- současný desktopový běh se při migračních krocích nesmí rozbít.

Platná architektonická rozhodnutí jsou hlavně:

- `ADR-015` — komunikační kanály jsou klienti nad agentním backendem,
- `ADR-016` — serverový backend pro mobilní a víceklientskou architekturu.

## Dokončené migrační kroky

- `MIG-001` — agentní runtime kontrakt.
  - `POST /api/v1/messages` přijímá textovou zprávu.
  - Backend vrací stabilní odpověďový model.
  - Stav `runtime_unavailable` je zatím očekávaný, protože živý agent běží v
    desktopové aplikaci.
- `MIG-002` — sdílená konverzační relace.
  - Přidány modely `StoredMessage`, `ConversationSummary`, `ConversationDetail`.
  - Přidány endpointy `GET /api/v1/conversations` a
    `GET /api/v1/conversations/{conversation_id}`.
  - Relace jsou zatím uložené jen v paměti procesu.
- První část `MIG-003` — repository rozhraní.
  - `ConversationRepository` odděluje API od konkrétního úložiště.
  - `InMemoryConversationRepository` je aktuální fallback.
  - `backend/storage.py` obsahuje factory pro volbu repository.
- Druhá část `MIG-003` — SQLAlchemy 2.0 modely.
  - Přidán balíček `backend/db`.
  - Přidány modely `Client`, `Conversation`, `Message`.
  - Modely připravují tabulky `clients`, `conversations`, `messages`.
- Dokončení `MIG-003` — PostgreSQL persistence konverzací.
  - Přidán `PostgresConversationRepository`.
  - Repository factory používá PostgreSQL při nastaveném `DATABASE_URL`.
  - Bez databáze nebo při selhání připojení zůstává bezpečný in-memory fallback.
  - Ověřený zápis a čtení konverzačních dat přes backend API.
- `MIG-004` — backend storage pro krátkodobou paměť a dlouhodobá rozhodnutí.
  - Přidány tabulky `short_term_memory_turns` a `long_term_decisions`.
  - Přidán `MemoryRepository`, in-memory fallback a `PostgresMemoryRepository`.
  - Přidány backend API endpointy pro krátkodobou paměť a dlouhodobá rozhodnutí.
  - Přidán idempotentní SQLite import současných krátkodobých turnů a potvrzených
    dlouhodobých rozhodnutí.

## Aktuálně rozpracováno

`MIG-006` a `MIG-007` mají stav `IN PROGRESS`.

Hotová první část desktopového kanálu:

- Přidán obecný HTTP klient `backend.client` pro `POST /api/v1/messages`.
- Text z dashboardu se posílá nejdřív do backend API s `channel="desktop"` a
  `client_id` ve tvaru `desktop:{session_id}`.
- Desktopová textová relace si ukládá a znovu používá backend `conversation_id`.
- Při vypnutém, nedostupném nebo přechodovém backendu zůstává přímý fallback do
  současné Gemini Live session v `main.py`.
- Desktopový backend požadavek nepotlačuje lokální audio ani ElevenLabs TTS; toto
  potlačení zůstává jen pro externí kanály, jako je Telegram.

Hotová první část realtime kontraktu:

- Přidán backend `RealtimeEventHub` a WebSocket endpoint `/api/v1/realtime`.
- WebSocket po připojení posílá `hello` event se `schema_version="realtime.v1"`.
- `/api/v1/status` vrací počet připojených realtime klientů.
- `AgentRuntime` publikuje `runtime_state` při připojení/odpojení live handleru.
- `POST /api/v1/messages` publikuje realtime `message` eventy pro uživatelský i
  asistentův turn.
- Přidán desktopový realtime klient `backend.realtime_client`, který se spouští z
  `main.py` po startu backendu.
- Dashboard přijímá `hello`, `runtime_state` a `message` eventy a deduplikuje je
  proti současným lokálním logům.
- Desktopové textové user a assistant turny jsou realtime-first: pokud je WebSocket
  handshake aktivní, dashboard čeká na backend `message` event a lokálně zapisuje
  jen fallback.

Známé omezení:

- Audio, mikrofon a přehrávání jsou zatím pořád řízené v `main.py`.
- Embedded live handler pořád volá současnou agentní relaci v desktopovém procesu.
- WebSocket zatím neposílá reálné audio bloky; audio pole jsou jen připravená v
  kontraktu události.
- Lokální logovací cesty v `main.py` zatím zůstávají pro hlas a fallbacky kvůli
  kompatibilitě audio běhu.
- Samostatný backend bez desktop handleru dál vrací `runtime_unavailable`.

## Další krok po restartu

Pokračovat v `MIG-006`:

1. Přesunout další desktopovou konverzační orchestraci z `main.py` za backend
   kontrakt.
2. Navrhnout skutečný audio stream a klientské řídicí příkazy pro `MIG-007`.
3. Převést další hlasové nebo stavové části až po stabilizaci realtime audio kontraktu.

## Důležité soubory

- `docs/MIGRATION_PLAN.md` — hlavní plán migrace.
- `docs/localization/PLAN.md` — evidence dokončených kroků podle pravidel
  repozitáře.
- `docs/localization/HISTORY.md` — append-only historie změn.
- `backend/app.py` — vytvoření FastAPI aplikace.
- `backend/api.py` — HTTP endpointy.
- `backend/config.py` — backend konfigurace z prostředí.
- `backend/database.py` — kontrola dostupnosti databáze.
- `backend/storage.py` — factory pro conversation repository.
- `backend/services/conversations.py` — repository rozhraní a in-memory fallback.
- `backend/services/postgres_conversations.py` — PostgreSQL implementace
  conversation repository.
- `backend/services/memory.py` — repository rozhraní a fallback pro paměť.
- `backend/services/postgres_memory.py` — PostgreSQL implementace paměti.
- `backend/services/memory_migration.py` — import současné SQLite paměti.
- `backend/services/agent_runtime.py` — backend runtime mezivrstva.
- `backend/services/realtime.py` — WebSocket event hub pro realtime klienty.
- `backend/client.py` — obecný HTTP klient pro backend message kontrakt.
- `backend/realtime_client.py` — desktopový WebSocket klient pro realtime eventy.
- `backend/db/base.py` — SQLAlchemy declarative base.
- `backend/db/models.py` — SQLAlchemy ORM modely.
- `backend/db/session.py` — vytvoření async engine, sessionmaker a inicializace
  schématu.

## Poslední ověření

Před uložením stavu byly ověřeny:

- Python syntaxe backend DB a repository modulů přes `py_compile`.
- Testovací připojení k PostgreSQL přes hodnoty z lokálního `.env`.
- Vytvoření tabulek `clients`, `conversations` a `messages` v cílovém schématu.
- Přímý smoke test `PostgresConversationRepository`.
- API smoke test přes `POST /api/v1/messages`,
  `GET /api/v1/conversations/{conversation_id}` a `GET /api/v1/conversations`.
- API smoke test paměti přes endpointy `/api/v1/memory/...`.
- SQLite import do PostgreSQL přenesl 228 krátkodobých turnů a 1 dlouhodobé
  rozhodnutí; opakovaný import přidal 0 duplicit.
- Syntaxe `main.py` a `features/002_telegram_bridge/bridge.py` po změně Telegramu.
- Izolovaný smoke test Telegram bridge bez externího API volání potvrdil, že textový
  i hlasový update odpovídají přes `sendMessage` a nevolají `sendAudio`.
- Syntaxe `features/002_telegram_bridge/backend_client.py` a souvisejících backend
  message modulů.
- Smoke test backend klienta ověřil payload pro `POST /api/v1/messages` a finální
  backend odpověď bez fallbacku.
- Smoke test `main.py` ověřil použití backend odpovědi i desktopový fallback pro
  `runtime_unavailable` u textového i přepsaného hlasového vstupu.
- API smoke test nad in-memory backendem ověřil `conversation_id`, `client_id`
  `telegram:123`, kanál `telegram` a očekávaný stav `runtime_unavailable`.
- `AgentRuntime` smoke test ověřil připojený live handler, stav `ok` a uložení
  uživatelské i asistentovy zprávy.
- FastAPI smoke test ověřil, že `app.state.agent_runtime.connect(...)` přepne
  `/api/v1/messages` na skutečnou odpověď handleru a `/api/v1/status` hlásí
  připojený runtime.
- Syntaxe `backend/client.py` a `main.py` prošla přes `py_compile` po přesměrování
  desktopového textového vstupu přes backend.
- Smoke test `BackendClient` ověřil desktopový payload, URL, `conversation_id` a
  dvojici timeoutů pro `POST /api/v1/messages`.
- Izolovaný smoke test `main.py` ověřil desktopový fallback při
  `runtime_unavailable`, ukládání backend `conversation_id` a rozdíl mezi
  potlačeným Telegram audiem a zachovaným desktopovým audiem.
- Syntaxe realtime backend modulů prošla přes `py_compile`.
- WebSocket smoke test ověřil `hello`, `pong`, realtime status a `message` eventy
  při `POST /api/v1/messages`.
- Smoke test runtime stavu ověřil `runtime_state` event při připojení live handleru.
- Syntaxe `backend/realtime_client.py` a `main.py` prošla přes `py_compile`.
- Smoke test `BackendRealtimeClient` ověřil odvození URL, explicitní realtime URL a
  parsování eventů.
- Smoke test `main.py` ověřil zpracování `hello`, `message`, deduplikaci zpráv a
  filtrování přechodové `runtime_unavailable` odpovědi.
- Smoke test `main.py` ověřil realtime-first desktop logování, vypnutí lokálního
  zápisu při aktivním handshake a zachování lokálního fallback logování.

Známé upozornění:

- `fastapi.testclient.TestClient` vypisuje deprecation warning kvůli `httpx`; není
  to chyba aktuální migrace.
- U více požadavků nad asyncpg repository používej `TestClient` jako context
  manager.
- Běžné dlouhodobé faktické záznamy z `memory_items` zůstávají v kompatibilní
  SQLite vrstvě.
