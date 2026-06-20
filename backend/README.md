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
- `GET /api/v1/conversations` vraci seznam konverzacnich relaci v pameti procesu.
- `GET /api/v1/conversations/{conversation_id}` vraci detail relace vcetne zprav.

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

Konverzacni relace jsou v tomto kroku pouze docasne in-memory uloziste. Po
restartu backendu se ztrati. Trvale ulozeni do PostgreSQL je dalsi migracni krok.

API uz nepouziva konkretni in-memory uloziste primo. Konverzace jdou pres
`ConversationRepository` a factory `create_conversation_repository`. PostgreSQL
implementace se doplni jako dalsi cast `MIG-003`; do te doby factory vraci
in-memory fallback.

Databazove schéma pro PostgreSQL uz ma SQLAlchemy 2.0 modely v `backend/db`.
Modely `Client`, `Conversation` a `Message` pripravuji tabulky `clients`,
`conversations` a `messages`, vcetne zakladnich vazeb, indexu a timestampu.
Repository je zatim na tyto modely jeste nepripojena.

## Konfigurace

```env
JARVIS_BACKEND_HOST="127.0.0.1"
JARVIS_BACKEND_PORT="8000"
JARVIS_BACKEND_RELOAD="false"
DATABASE_URL=""
```

`DATABASE_URL` bude smerovat na PostgreSQL, napriklad pres async driver
`postgresql+asyncpg://...`. Skutecny connection string se neverzuje.
