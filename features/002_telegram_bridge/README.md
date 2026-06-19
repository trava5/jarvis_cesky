# 002_telegram_bridge

Feature pro komunikaci s JARVIS přes Telegram bota.

Tato feature není agentní tool a nepatří do `actions/tool_catalog.py`. Slouží jako
runtime komunikační kanál mezi Telegramem a běžící desktopovou relací JARVIS.

## Konfigurace

Skutečné hodnoty patří pouze do lokálního `.env`.

```env
TELEGRAM_BRIDGE_ENABLED="false"
TELEGRAM_BOT_TOKEN=""
TELEGRAM_ALLOWED_CHAT_IDS=""
TELEGRAM_DOWNLOAD_DIR="runtime/telegram"
```

`TELEGRAM_ALLOWED_CHAT_IDS` je čárkou oddělený allowlist chatů, které smějí s
agentem komunikovat. Bez allowlistu se bridge nespustí.

## Stav

První verze podporuje:

- Telegram long polling přes Bot API,
- autorizaci přes `TELEGRAM_ALLOWED_CHAT_IDS`,
- textové zprávy směrované do běžící Gemini Live session,
- přijetí hlasové zprávy a stažení souboru do `runtime/telegram`.

Hlasové zprávy zatím nejsou přepisované do textu. Navazující krok musí doplnit STT
nebo audio převod z Telegram OGG/Opus do formátu, který umí zpracovat zvolený
model.

## Použití

1. V Telegramu vytvoř bota přes BotFather.
2. Token ulož do `TELEGRAM_BOT_TOKEN`.
3. Zjisti `chat_id` povoleného uživatele nebo skupiny.
4. Přidej ho do `TELEGRAM_ALLOWED_CHAT_IDS`.
5. Nastav `TELEGRAM_BRIDGE_ENABLED="true"`.
6. Spusť desktopovou aplikaci JARVIS.

Bridge se spustí jen při vyplněném tokenu, zapnutém `TELEGRAM_BRIDGE_ENABLED` a
nenulovém allowlistu.
