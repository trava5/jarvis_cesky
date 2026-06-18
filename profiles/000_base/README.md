# 000_base

Výchozí profil pro obecného osobního asistenta.

Tento profil zatím slouží jako dokumentační šablona pro budoucí specializované
kopie. Aktuální aplikace stále používá `core/prompt.txt` a globální katalog
nástrojů.

Zapnuté šablonové features:

- `001_elevenlabs_voice` — hlasový provider ElevenLabs; pro živý hlas se použije
  až po výslovném nastavení `JARVIS_VOICE_PROVIDER="elevenlabs"` a vyplnění API
  klíče a `ELEVENLABS_VOICE_ID` v `.env`.
