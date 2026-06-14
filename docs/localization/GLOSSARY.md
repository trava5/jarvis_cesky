# Překladový slovník

## Uživatelské termíny

| Původní nebo technický termín | Český text |
|---|---|
| JARVIS ready | JARVIS je připraven |
| Listening | Poslouchám / Naslouchání |
| Thinking | Přemýšlím / Zpracování |
| Speaking | Mluvím / Přehrávání odpovědi |
| Paused | Pozastaveno |
| Settings | Nastavení |
| Debug | Ladění |
| Mute | Ztlumit / Ztlumeno |
| Send | Odeslat |
| Shutdown | Ukončit |
| Resume | Pokračovat |
| Health | Zdraví / Zdravotní souhrn |
| Weather | Počasí |
| System status | Stav systému |
| Conversation | Konverzace |
| Reminder | Připomínka |
| Calendar event | Událost kalendáře |
| Active window | Aktivní okno |
| System information | Systémové informace |
| Network | Síť |
| Battery | Baterie |
| Memory | Paměť |
| Contact | Kontakt |
| Draft | Koncept |

Konkrétní volba mezi variantami závisí na prostoru v UI. V hlasových odpovědích
preferuj přirozenou větu, v krátkých štítcích stručnější variantu.

## Regionální výchozí hodnoty

- Výchozí lokalita počasí: `Praha`.
- Výchozí předvolba devítimístného lokálního čísla: `+420`.
- Datum v UI: `d. MĚSÍCE rrrr`.
- Čas v UI: `HH:MM:SS`.

## Nepřekládané identifikátory

Následující hodnoty jsou součástí interního rozhraní a nesmí se překládat:

- Názvy nástrojů, například `open_app`, `sys_info`, `get_weather`.
- Stavy `LISTENING`, `THINKING`, `SPEAKING`, `PAUSED`, `ERROR`.
- Dotazy `today`, `tomorrow`, `next`, `agenda`, `week`, `upcoming`,
  `overdue`, `all`.
- Systémové dotazy `battery`, `cpu`, `ram`, `disk`, `time`, `date`,
  `network`.
- Akce prohlížeče `open_url`, `search`, `play_youtube`.
- Cíl obrazovky `active_window`.
- Kategorie paměti `identity`, `preferences`, `projects`, `notes`.
- Poskytovatelé `auto`, `youtube`, `spotify`, `apple_music`.
- Pole API jako `start_iso`, `due_iso`, `send_now`, `recipient_name`.

## Chybové markery

Detekce v `main.py` používá české fráze a anglické technické slovo `error`,
které mohou vracet externí služby. Turecké kompatibilní markery byly po
překladu modulů `actions` odstraněny.
