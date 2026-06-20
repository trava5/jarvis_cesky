# Stav projektu

Aktualizováno: 2026-06-20

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

`MIG-005` má stav `IN PROGRESS`.

Hotová je přípravná část Telegram kanálu:

- Telegram dál přijímá textové zprávy.
- Telegram dál přijímá hlasové zprávy a přepisuje je přes Gemini do textu.
- Telegram už neodesílá hlasové ani audio odpovědi; textový i hlasový vstup vrací
  jen textovou zprávu.

Zbývající část `MIG-005` je přesměrování Telegram bridge přes backend API.

## Další krok po restartu

Pokračovat další částí `MIG-005`:

1. Přidat backend klienta nebo adapter pro volání `POST /api/v1/messages`.
2. Přesměrovat Telegram textový vstup přes backend při zachování bezpečného
   desktopového fallbacku.
3. Přesměrovat přepsaný Telegram hlasový vstup přes stejnou backend cestu.
4. Ověřit `conversation_id`, `client_id`, kanál `telegram` a chování při
   nedostupném backendu.

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

Známé upozornění:

- `fastapi.testclient.TestClient` vypisuje deprecation warning kvůli `httpx`; není
  to chyba aktuální migrace.
- U více požadavků nad asyncpg repository používej `TestClient` jako context
  manager.
- Běžné dlouhodobé faktické záznamy z `memory_items` zůstávají v kompatibilní
  SQLite vrstvě.
