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
| MIG-005 | Telegram přes backend | IN PROGRESS | Příprava: Telegram přijímá text i hlas, ale odpovídá už jen textem; backend napojení zůstává navazující část. |
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

Stav: `IN PROGRESS`

Tento krok postupně převádí Telegram bridge z přímého napojení na desktopový
runtime na klienta backendového API. První přípravná část sjednocuje výstup
Telegramu: bridge dál přijímá textové zprávy i hlasové zprávy přepsané přes Gemini,
ale odpověď do Telegramu je vždy textová.

Kontrolní body:

- [x] Zachovat příjem textových Telegram zpráv.
- [x] Zachovat příjem hlasových Telegram zpráv a jejich přepis do textu.
- [x] Odstranit odesílání hlasových/audio odpovědí přes Telegram.
- [ ] Přidat backend klienta nebo adapter pro volání `/api/v1/messages`.
- [ ] Přesměrovat Telegram textový vstup přes backend při zachování bezpečného
  desktopového fallbacku.
- [ ] Přesměrovat přepsaný Telegram hlasový vstup přes stejnou backend cestu.
- [ ] Ověřit konverzační relace, klientské ID a chování při nedostupném backendu.

Známé omezení:

- Telegram bridge po této přípravné části stále volá živý desktopový runtime přes
  `main.py`. Přímé backend napojení zůstává další část `MIG-005`.
