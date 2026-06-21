# Stav konverzace

Aktualizováno: 2026-06-21

Tento soubor ukládá pracovní kontext aktuální vývojové konverzace před restartem
stanice.

## Poslední uživatelský záměr

Uživatel chce pokračovat podle migračního plánu na nové architektuře:

- backend: FastAPI,
- běh: Uvicorn,
- databáze: PostgreSQL,
- cílem je budoucí napojení mobilního frontendu, například Flutteru.

Bezprostřední aktuální požadavek:

- pokračovat v `MIG-006`,
- připravit realtime WebSocket kontrakt pro `MIG-007`,
- napojit desktop UI jako realtime klienta,
- zatím zachovat současné audio, mikrofon a živou Gemini session v `main.py`.

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

Následně byl dokončen mezikrok `ARCH-012`:

- přidán `features/002_telegram_bridge/backend_client.py`,
- Telegram textové vstupy se posílají nejdřív na backend API,
- přepsané hlasové vstupy z Telegramu používají stejnou backend cestu,
- při nedostupném backendu nebo stavech `runtime_unavailable` / `not_implemented`
  se použije desktopový fallback přes současnou živou relaci v `main.py`,
- backend konverzační ID se ukládá per Telegram chat.

Poté byl dokončen `ARCH-013` a tím i `MIG-005`:

- backend `AgentRuntime` umí přijmout volitelný live handler,
- FastAPI aplikace ukládá instanci runtime do `app.state.agent_runtime`,
- desktop aplikace spouští embedded backend při
  `JARVIS_EMBEDDED_BACKEND_ENABLED="true"`,
- při navázání Gemini Live relace se handler z `main.py` připojí k backendu,
- `/api/v1/messages` v embedded režimu vrací skutečnou odpověď agenta se stavem
  `ok`,
- samostatný backend bez embedded handleru dál bezpečně vrací `runtime_unavailable`.

Následně byla zahájena první část `MIG-006`:

- přidán obecný HTTP klient `backend.client` pro `POST /api/v1/messages`,
- desktopový textový vstup z dashboardu volá backend API s `channel="desktop"`,
- desktopová textová relace si ukládá backend `conversation_id`,
- při nedostupném nebo přechodovém backendu zůstává přímý fallback do současné
  Gemini Live session,
- desktopový backend požadavek zachovává lokální audio/TTS, zatímco Telegram
  požadavky lokální audio dál potlačují.

Poté byla zahájena první část `MIG-007`:

- přidán backend `RealtimeEventHub` v `backend/services/realtime.py`,
- přidán WebSocket endpoint `/api/v1/realtime`,
- realtime kontrakt používá `schema_version="realtime.v1"`,
- `/api/v1/status` vrací počet připojených realtime klientů,
- `AgentRuntime` publikuje `runtime_state` při připojení live handleru,
- `POST /api/v1/messages` publikuje `message` eventy pro uživatele i asistenta,
- typ `audio` je zatím připravený v modelu, ale reálné audio bloky se ještě
  neposílají.

Následně byl přidán desktopový realtime klient:

- přidán modul `backend/realtime_client.py`,
- přidána explicitní závislost `websockets` do `requirements.txt`,
- `main.py` spouští realtime klienta po startu embedded backendu,
- desktop klient zpracovává `hello`, `runtime_state` a `message` eventy,
- konverzační logy se deduplikují proti lokálnímu logování v `main.py`, aby dashboard
  nezobrazoval stejné zprávy dvakrát,
- přechodové assistant eventy se stavem `runtime_unavailable`, `not_implemented` a
  `runtime_error` se nelogují jako běžná odpověď, protože je řeší fallback.

Poté bylo zapnuté realtime-first logování pro desktopové textové turny:

- při aktivním WebSocket handshake se desktopový user turn nezapisuje okamžitě
  lokálně, ale přes backend `message` event,
- desktopová assistant odpověď se při aktivním realtime spojení také zobrazuje přes
  backend `message` event,
- při nedostupném backendu, chybě HTTP klienta nebo reconnectu realtime klienta
  zůstává lokální fallback logování,
- hlasové turny zůstávají lokální, dokud nebude připravený realtime audio/text
  kontrakt pro mikrofonní cestu.

## Stav plánu

`docs/MIGRATION_PLAN.md`:

- `MIG-001` je `DONE`.
- `MIG-002` je `DONE`.
- `MIG-003` je `DONE`.
- `MIG-004` je `DONE`.
- `MIG-005` je `DONE`.
- `MIG-006` je `IN PROGRESS`.
- `MIG-007` je `IN PROGRESS`.

Hotová část `MIG-007`:

- Realtime event model pro stav, text a budoucí audio.
- WebSocket endpoint `/api/v1/realtime`.
- `hello`, `pong`, `runtime_state` a `message` eventy.
- WebSocket smoke testy pro message i runtime state eventy.
- Desktop realtime klient nad `/api/v1/realtime`.
- Realtime-first logování desktopových textových turnů s lokálním fallbackem.

Další krok:

- Navrhnout skutečný audio stream a klientské řídicí příkazy pro `MIG-007`.
- Převést další hlasové nebo stavové části až po stabilizaci realtime audio kontraktu.

## Doporučený další prompt po restartu

Pokračuj v `MIG-007`: desktop text je realtime-first, navazuj návrhem skutečného
audio streamu a klientských řídicích příkazů.

## Důležité technické rozhodnutí

PostgreSQL implementace nesmí rozbít současný desktopový běh. Pokud databáze není
nastavená nebo dostupná, backend má dál fungovat nad in-memory fallbackem.

Skutečné hodnoty `.env`, tokeny a connection stringy se nesmí zapisovat do
dokumentace.
