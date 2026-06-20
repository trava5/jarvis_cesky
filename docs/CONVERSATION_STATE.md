# Stav konverzace

Aktualizováno: 2026-06-20

Tento soubor ukládá pracovní kontext aktuální vývojové konverzace před restartem
stanice.

## Poslední uživatelský záměr

Uživatel chce pokračovat podle migračního plánu na nové architektuře:

- backend: FastAPI,
- běh: Uvicorn,
- databáze: PostgreSQL,
- cílem je budoucí napojení mobilního frontendu, například Flutteru.

Bezprostřední aktuální požadavek:

- upravit Telegram tak, aby vždy odpovídal jen textem,
- zachovat příjem textových i hlasových zpráv,
- hlasové odpovědi z Telegram kódu úplně vypustit.

## Poslední dokončená práce

Bylo dokončeno `MIG-003` pro PostgreSQL persistenci konverzačních dat:

- `backend/db/session.py`,
- `backend/services/postgres_conversations.py`,
- úpravy `backend/config.py`, `backend/database.py`, `backend/storage.py`,
  `backend/api.py`, `backend/services/conversations.py` a
  `backend/services/agent_runtime.py`.

Implementováno:

- async `ConversationRepository` kontrakt,
- in-memory fallback bez databáze,
- PostgreSQL repository pro tabulky `clients`, `conversations` a `messages`,
- vývojová inicializace databázového schématu a tabulek,
- konfigurace přes `DATABASE_URL`, `DATABASE_NAME`, `DATABASE_USER`,
  `DATABASE_PASS` a `DATABASE_SCHEMA`.

Ověřeno:

- připojení k PostgreSQL přes lokální `.env`,
- vytvoření tabulek v cílovém schématu,
- přímý smoke test `PostgresConversationRepository`,
- backend API smoke test pro zápis a čtení konverzace.

Následně bylo dokončeno `MIG-004` pro krátkodobou paměť a dlouhodobá potvrzená
rozhodnutí:

- přidány SQLAlchemy modely `ShortTermMemoryTurn` a `LongTermDecision`,
- přidán `MemoryRepository`, `InMemoryMemoryRepository`,
  `FallbackMemoryRepository` a `PostgresMemoryRepository`,
- přidány endpointy `/api/v1/memory/short-term`,
  `/api/v1/memory/short-term/search`, `/api/v1/memory/decisions` a
  `/api/v1/memory/import/sqlite`,
- import ze SQLite je idempotentní a při ověření přenesl 228 krátkodobých turnů a
  1 dlouhodobé rozhodnutí.

V rámci rozpracovaného `MIG-005` byla dokončena přípravná změna `FEAT-014`:

- `features/002_telegram_bridge` dál přijímá textové a hlasové zprávy.
- Hlasové zprávy se dál stahují a přepisují do textu přes Gemini.
- Telegram bridge už neposílá audio odpovědi a nepoužívá `sendAudio`.
- `main.py` už pro Telegram nevytváří Gemini Live WAV ani ElevenLabs audio odpovědi.
- Telegram výstup je po textovém i hlasovém vstupu vždy textová zpráva.

## Stav plánu

`docs/MIGRATION_PLAN.md`:

- `MIG-001` je `DONE`.
- `MIG-002` je `DONE`.
- `MIG-003` je `DONE`.
- `MIG-004` je `DONE`.
- `MIG-005` je `IN PROGRESS`.

Hotová část `MIG-005`:

- Telegram text-only output po textovém i hlasovém vstupu.

Zbývající část `MIG-005`:

- Telegram bridge přes backend API,
- zachování současného desktopového fallbacku,
- příprava na sdílený agentní runtime pro více klientů.

## Doporučený další prompt po restartu

Pokračuj v `MIG-005`: přidej backend klienta nebo adapter pro `POST /api/v1/messages`
a začni přes něj směrovat Telegram textové vstupy se zachováním desktopového
fallbacku.

## Důležité technické rozhodnutí

PostgreSQL implementace nesmí rozbít současný desktopový běh. Pokud databáze není
nastavená nebo dostupná, backend má dál fungovat nad in-memory fallbackem.

Skutečné hodnoty `.env`, tokeny a connection stringy se nesmí zapisovat do
dokumentace.
