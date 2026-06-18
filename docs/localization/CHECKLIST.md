# Kontrolní seznam lokalizační změny

Tento seznam projdi před označením kroku jako `DONE`.

## Před úpravou

- [ ] Byla zkontrolována platná rozhodnutí v `DECISIONS.md`.
- [ ] Je změna uvedena v `PLAN.md`.
- [ ] Aktivní krok je označen `IN PROGRESS`.
- [ ] Je jasné, které technické identifikátory se nesmí překládat.
- [ ] Byly zkontrolovány související moduly a návratové hodnoty.

## Během úpravy

- [ ] Uživatelské texty jsou přeloženy přirozenou češtinou.
- [ ] Terminologie odpovídá `GLOSSARY.md`.
- [ ] Názvy funkcí, API polí a strojové hodnoty zůstaly zachované.
- [ ] České texty používají UTF-8.
- [ ] Nové texty neobsahují zbytečné anglicismy nebo turecké výrazy.
- [ ] Detekce chyb a úspěchu stále rozpoznává návraty závislých modulů.
- [ ] Pokud vznikla nebo byla zapojena nová akce, má záznam v `actions/tool_catalog.py`.
- [ ] Pokud vznikl komunikační kanál, bridge nebo hlasový provider, je umístěný ve `features`.
- [ ] Nová nebo revidovaná akce je uložená v `actions/NNN_name`.
- [ ] Nová nebo revidovaná feature je uložená v `features/NNN_name`.
- [ ] Pokud změna souvisí se specializací agenta, je popsaná v `profiles`, ne ve sdílené feature.

## Ověření

- [ ] Upravené Python soubory prošly `py_compile` nebo `compileall`.
- [ ] Bylo provedeno cílené hledání zbývajících tureckých textů.
- [ ] U změn UI bylo zkontrolováno rozložení a délka textů.
- [ ] U změn chování byl proveden odpovídající funkční test.
- [ ] Nebyly změněny nesouvisející soubory.

## Dokumentace

- [ ] Stav a kontrolní body byly aktualizovány v `PLAN.md`.
- [ ] Projektové rozhodnutí bylo podle potřeby zapsáno do `DECISIONS.md`.
- [ ] Nové termíny byly doplněny do `GLOSSARY.md`.
- [ ] Na konec `HISTORY.md` byl přidán záznam.
- [ ] Záznam historie uvádí provedené kontroly a známá omezení.
