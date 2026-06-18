# Pokyny pro práci v repozitáři

Tyto pokyny platí pro celý projekt.

## Povinná dokumentace změn

Při každé změně zdrojového kódu, konfigurace nebo lokalizace:

1. Před úpravou zkontroluj platná rozhodnutí v `DECISIONS.md`.
2. Zkontroluj aktuální plán v `docs/localization/PLAN.md`.
3. Označ právě řešený krok stavem `IN PROGRESS`.
4. Po dokončení aktualizuj stav kroku a jeho kontrolní body.
5. Přidej záznam do `docs/localization/HISTORY.md`.
6. Pokud vznikne nový překladový termín, doplň `docs/localization/GLOSSARY.md`.
7. Pokud změna ovlivňuje celý projekt, přidej nebo aktualizuj ADR v
   `DECISIONS.md`.
8. Před uzavřením změny projdi `docs/localization/CHECKLIST.md`.

Historie je append-only. Starší záznamy nemaž ani nepřepisuj, pouze oprav
prokazatelnou faktickou chybu.

Projektová rozhodnutí jsou rovněž append-only. Přijaté rozhodnutí nahrazuj
novým ADR, nepřepisuj jeho původní obsah.

## Stavové hodnoty plánu

- `TODO` — práce ještě nezačala.
- `IN PROGRESS` — právě probíhá.
- `BLOCKED` — nelze pokračovat bez rozhodnutí nebo externí závislosti.
- `DONE` — implementace i předepsaná kontrola jsou dokončené.

## Pravidla lokalizace

- Uživatelské texty mají být v češtině.
- Technické identifikátory API, názvy funkcí a strojové hodnoty se nepřekládají.
- Zachovej význam návratových hodnot, podle kterých aplikace rozpoznává chyby
  nebo úspěšné akce.
- Nové české termíny sjednocuj podle `docs/localization/GLOSSARY.md`.
- Po úpravě Pythonu proveď alespoň syntaktickou kontrolu přes projektové `venv`.

## Pravidla akčních modulů

- Nové nástroje volané agentem přes tool/function calling patří do složky
  `actions`.
- Nové nebo revidované akce ukládej do vlastních číslovaných podadresářů ve tvaru
  `actions/NNN_name`, například `actions/001_weather`.
- Při vytvoření nebo zapojení nové akce vždy přidej odpovídající záznam do
  `actions/tool_catalog.py`.
- Akce bez záznamu v katalogu nástrojů není považovaná za dokončenou.
- Pokud název číslovaného adresáře začíná číslicí, načítej implementaci přes
  `actions/action_loader.py` nebo `importlib`, ne přímým `from actions.NNN_name`.

## Pravidla běhových vlastností

- Komunikační kanály, bridge adaptéry, hlasové moduly a poskytovatelé služeb
  patří do složky `features`.
- Nové nebo revidované features ukládej do vlastních číslovaných podadresářů ve
  tvaru `features/NNN_name`.
- Telegram bridge, mobilní vstupní kanál nebo budoucí hlasový modul ElevenLabs
  nejsou `actions`, pokud je agent přímo nevolá jako nástroj.
- Pokud běhová vlastnost zároveň zpřístupní nový agentní nástroj, volatelná část
  patří do `actions` a musí mít záznam v `actions/tool_catalog.py`.

## Pravidla profilů agentů

- Budoucí specializované varianty agenta popisuj v adresáři `profiles`.
- Profil určuje vlastní prompt, povolené actions a zapnuté features.
- Specializace agenta se nemá řešit přidáváním doménových pravidel do sdílených
  features.
- Samostatnou kopii projektu vytvářej až ze stabilního základu a podle profilu,
  který jasně uvádí zaměření, prompt a sadu povolených nástrojů.
