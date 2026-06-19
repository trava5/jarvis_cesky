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
| MIG-002 | Sdílená konverzační relace | TODO | Zavedení `conversation_id`, `client_id`, `channel` a jednotného modelu zpráv. |
| MIG-003 | PostgreSQL persistence | TODO | Tabulky pro klienty, konverzace, zprávy, krátkodobou paměť a dlouhodobá rozhodnutí. |
| MIG-004 | Migrace paměti | TODO | Přesun současné paměti z lokální SQLite vrstvy do backend storage vrstvy. |
| MIG-005 | Telegram přes backend | TODO | Telegram bridge přestane volat desktopový runtime přímo a použije backend službu. |
| MIG-006 | Desktop přes backend | TODO | Dashboard se stane klientem backendu a `main.py` se ztenčí na UI/audio bootstrap. |
| MIG-007 | Realtime WebSocket API | TODO | Stream stavu, textu, audia a událostí pro desktop, Telegram a mobilní klienty. |
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
