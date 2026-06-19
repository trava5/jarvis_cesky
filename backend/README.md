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

## Konfigurace

```env
JARVIS_BACKEND_HOST="127.0.0.1"
JARVIS_BACKEND_PORT="8000"
JARVIS_BACKEND_RELOAD="false"
DATABASE_URL=""
```

`DATABASE_URL` bude smerovat na PostgreSQL, napriklad pres async driver
`postgresql+asyncpg://...`. Skutecny connection string se neverzuje.
