# Profily agentů

Adresář `profiles` popisuje budoucí specializované varianty agenta.

Základní projekt drží společné runtime jádro:

- spuštění živé relace,
- paměť,
- správu konfigurace,
- společné `features`,
- obecné načítání promptu a katalogu nástrojů,
- společná pravidla pro bezpečnost a lokalizaci.

Konkrétní specializovaný agent se bude lišit hlavně profilem:

- vlastním systémovým promptem,
- výběrem povolených actions,
- výběrem zapnutých features,
- případnou vlastní konfigurací,
- dokumentací zaměření agenta.

## Doporučená struktura profilu

```text
profiles/NNN_name/
  README.md
  prompt.txt
  actions.json
  features.json
```

`prompt.txt` obsahuje specializovaný systémový prompt.

`actions.json` určuje, které nástroje z `actions/tool_catalog.py` má daný agent
k dispozici.

`features.json` určuje, které běhové vlastnosti z `features` se mají v dané
variantě zapnout.

## Pravidlo kopírování

Samostatné kopie projektu se mají vytvářet až ve chvíli, kdy je společný základ
stabilní. Kopie má převzít jádro, sdílené features a jen takové actions, které
odpovídají zaměření daného agenta. Prompt a katalog povolených actions se pak
upravují podle účelu konkrétní kopie.
