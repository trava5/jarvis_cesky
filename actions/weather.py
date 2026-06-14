"""
Jednoduchý souhrn počasí z externí služby.
Vytvořil Alp Unlu - @alppunlu

Výchozí lokalita:
- použije se JARVIS_WEATHER_LOCATION, pokud je nastavena,
- jinak se použije Praha.
"""

from __future__ import annotations

import os

import requests

WEATHER_TRANSLATIONS = {
    "sunny": "slunečno",
    "clear": "jasno",
    "partly cloudy": "polojasno",
    "cloudy": "oblačno",
    "overcast": "zataženo",
    "mist": "opar",
    "fog": "mlha",
    "light rain": "slabý déšť",
    "rain": "déšť",
    "heavy rain": "silný déšť",
    "light snow": "slabé sněžení",
    "snow": "sněžení",
    "thunderstorm": "bouřka",
}


def _translate_weather_description(description: str) -> str:
    normalized = str(description or "").strip().lower()
    return WEATHER_TRANSLATIONS.get(normalized, normalized)


def get_weather_summary(location: str | None = None) -> str:
    target = (location or os.environ.get("JARVIS_WEATHER_LOCATION") or "Praha").strip()
    try:
        response = requests.get(
            f"https://wttr.in/{target}",
            params={"format": "j1"},
            timeout=10,
            headers={"User-Agent": "JARVIS Windows"},
        )
        response.raise_for_status()
        payload = response.json()
        current = (payload.get("current_condition") or [{}])[0]
        temp_c = current.get("temp_C")
        feels_like = current.get("FeelsLikeC")
        weather_desc = ((current.get("weatherDesc") or [{}])[0]).get("value", "")
        humidity = current.get("humidity")

        parts = []
        if temp_c:
            parts.append(f"{temp_c} °C")
        if weather_desc:
            parts.append(_translate_weather_description(weather_desc))
        if feels_like and feels_like != temp_c:
            parts.append(f"pocitově {feels_like} °C")
        if humidity:
            parts.append(f"vlhkost {humidity}%")

        if not parts:
            return "Informace o počasí momentálně nejsou dostupné."

        return f"Počasí pro {target}: " + ", ".join(parts) + "."
    except Exception:
        return "Informace o počasí momentálně nejsou dostupné."
