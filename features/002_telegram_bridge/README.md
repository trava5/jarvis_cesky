# 002_telegram_bridge

Feature pro komunikaci s JARVIS přes Telegram bota.

Tato feature není agentní tool a nepatří do `actions/tool_catalog.py`. Slouží jako
runtime komunikační kanál mezi Telegramem a běžící desktopovou relací JARVIS.
Telegram bridge není dashboardový přepisovač. Je to klientský kanál, který má
posílat vstupy do sdíleného agentního backendu a vracet uživateli odpovědi ze
stejného runtime jako desktopové UI.

## Konfigurace

Skutečné hodnoty patří pouze do lokálního `.env`.

```env
TELEGRAM_BRIDGE_ENABLED="false"
TELEGRAM_BOT_TOKEN=""
TELEGRAM_ALLOWED_CHAT_IDS=""
TELEGRAM_DOWNLOAD_DIR="runtime/telegram"
TELEGRAM_TRANSCRIPTION_MODEL="models/gemini-2.5-flash"
```

`TELEGRAM_ALLOWED_CHAT_IDS` je čárkou oddělený allowlist chatů, které smějí s
agentem komunikovat. Bez allowlistu se bridge nespustí.
`TELEGRAM_TRANSCRIPTION_MODEL` určuje model pro přepis hlasových zpráv do textu.

## Stav

Aktuální verze podporuje:

- Telegram long polling přes Bot API,
- autorizaci přes `TELEGRAM_ALLOWED_CHAT_IDS`,
- textové zprávy směrované do běžící Gemini Live session,
- servisní příkazy `/start`, `/help` a `/id`,
- přijetí hlasové zprávy, stažení souboru do `runtime/telegram`,
- přepis Telegram OGG/Opus audia přes Gemini a předání textu do stejného
  agentního runtime jako běžnou textovou zprávu,
- textovou odpověď pro textové i hlasové Telegram dotazy.

Telegram bridge neodesílá hlasové ani audio odpovědi. Aktivní hlasový provider
desktopové aplikace neovlivňuje Telegram výstup; hlasová zpráva z Telegramu se
jen přepíše do textu a odpověď agenta se odešle jako běžná textová zpráva.

Další architektonický krok má oddělit explicitní agentní runtime rozhraní, které
budou sdílet Desktop UI, Telegram a případní další klienti.

## Použití

1. V Telegramu vytvoř bota přes BotFather.
2. Token ulož do `TELEGRAM_BOT_TOKEN`.
3. Zjisti `chat_id` povoleného uživatele nebo skupiny.
4. Přidej ho do `TELEGRAM_ALLOWED_CHAT_IDS`.
5. Nastav `TELEGRAM_BRIDGE_ENABLED="true"`.
6. Spusť desktopovou aplikaci JARVIS.

Bridge se spustí jen při vyplněném tokenu, zapnutém `TELEGRAM_BRIDGE_ENABLED` a
nenulovém allowlistu.

Pro zjištění `chat_id` pošli botovi zprávu `/id`. Pokud chat ještě není v
allowlistu, bridge z bezpečnostních důvodů odpoví jen informací, že chat nemá
povolený přístup.
