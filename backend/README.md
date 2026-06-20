# Backend

Serverova vrstva pro budouci viceklientskou architekturu JARVIS.

Backend je zatim zavedena paralelni kostra. Soucasna desktop aplikace zustava
funkcni a agentni runtime jeste bezi v `main.py`. Dalsi migracni kroky budou
postupne presouvat sdilenou agentni logiku za API, aby ji mohly pouzivat Desktop
UI, Telegram bridge a budouci mobilni frontend, napriklad Flutter.

## Spusteni

Skutecne hodnoty patri do lokalniho `.env`.

```powershell
.\.venv\Scripts\python.exe -m backend
```

Vychozi adresa je `http://127.0.0.1:8000`.

## Endpointy

- `GET /api/v1/health` vraci zakladni stav backendu.
- `GET /api/v1/status` vraci stav backendu a PostgreSQL konfigurace.
- `POST /api/v1/messages` prijima prvni stabilni agentni message kontrakt. Zatim
  vraci `runtime_unavailable`, protoze zivy agentni runtime jeste bezi v desktopove
  aplikaci.
- `GET /api/v1/conversations` vraci seznam konverzacnich relaci z aktivniho
  repository.
- `GET /api/v1/conversations/{conversation_id}` vraci detail relace vcetne zprav.
- `POST /api/v1/memory/short-term` ulozi kratkodoby pametovy turn.
- `GET /api/v1/memory/short-term` vraci posledni kratkodobe turny.
- `GET /api/v1/memory/short-term/search` vyhleda text v kratkodobe pameti.
- `DELETE /api/v1/memory/short-term` smaze kratkodobe turny starsi nez zadany
  pocet dni.
- `POST /api/v1/memory/decisions` ulozi potvrzene dlouhodobe rozhodnuti.
- `GET /api/v1/memory/decisions` vraci potvrzena dlouhodoba rozhodnuti.
- `POST /api/v1/memory/import/sqlite` importuje soucasne lokalni SQLite zaznamy
  kratkodobe pameti a dlouhodobych rozhodnuti do aktivni backend storage vrstvy.

Priklad zpravy:

```json
{
  "text": "Ahoj, jaky je dnes plan?",
  "channel": "mobile",
  "client_id": "flutter-dev",
  "conversation_id": null,
  "want_audio": false
}
```

API uz nepouziva konkretni in-memory uloziste primo. Konverzace jdou pres
`ConversationRepository` a factory `create_conversation_repository`. Bez
`DATABASE_URL` factory vraci in-memory fallback. Pri nastavene databazi pouzije
PostgreSQL repository nad SQLAlchemy modely; pokud pripojeni k databazi selze,
backend zustane funkcni nad in-memory fallbackem.

Databazove schéma pro PostgreSQL uz ma SQLAlchemy 2.0 modely v `backend/db`.
Modely `Client`, `Conversation` a `Message` pripravuji tabulky `clients`,
`conversations` a `messages`, vcetne zakladnich vazeb, indexu a timestampu.
Repository pri prvnim pouziti provede vyvojovou inicializaci schematu pres
`Base.metadata.create_all`.

Backend storage vrstva pro pamet pridava tabulky `short_term_memory_turns` a
`long_term_decisions`. Import ze SQLite je idempotentni: opakovane spusteni
importu nepridava duplicitni zaznamy se stejnou identitou.

## Konfigurace

```env
JARVIS_BACKEND_HOST="127.0.0.1"
JARVIS_BACKEND_PORT="8000"
JARVIS_BACKEND_RELOAD="false"
DATABASE_URL=""
DATABASE_NAME="postgres"
DATABASE_USER=""
DATABASE_PASS=""
DATABASE_SCHEMA=""
```

`DATABASE_URL` bude smerovat na PostgreSQL, napriklad pres async driver
`postgresql+asyncpg://...`. Pokud URL neobsahuje prihlaseni, backend doplni
`DATABASE_USER` a `DATABASE_PASS`. Pokud URL neobsahuje nazev databaze, pouzije
se `DATABASE_NAME`. `DATABASE_SCHEMA` je volitelne databazove schema, napriklad
pro oddeleni vyvojovych tabulek. Skutecny connection string se neverzuje.
