"""
actions/health.py — načítá exportovaná zdravotní data.

Tok dat:
  export zdravotních dat z iPhonu
  → iCloud Drive/Auto Export/JARVIS/HealthAutoExport-YYYY-MM-DD.json
  → JARVIS
"""

import json
import re
import time
from datetime import date, datetime, timedelta
from pathlib import Path

# Windows: iCloud Drive is typically at %USERPROFILE%\iCloudDrive
_ICLOUD_BASE = Path.home() / "iCloudDrive"
HEALTH_DIR = _ICLOUD_BASE / "iCloud~com~ifunography~HealthExport" / "Documents" / "JARVIS"

# Zpětná kompatibilita se staršími umístěními.
_LEGACY_DIRS = [
    _ICLOUD_BASE / "Auto Export" / "JARVIS",
    _ICLOUD_BASE / "JARVIS",
    Path.home() / "OneDrive" / "JARVIS",
]

# Starší samostatný soubor.
_LEGACY_FILE = _ICLOUD_BASE / "JARVIS" / "health_data.json"

STALE_WARN_MINUTES = 120  # Upozornění na data starší než dvě hodiny.


def _normalize_query(text: str) -> str:
    import unicodedata

    text = (text or "").strip().casefold()
    text = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def _extract_target_date(query: str) -> date | None:
    q = _normalize_query(query)
    today = date.today()

    if any(token in q for token in ("predevcirem", "pred dvema dny")):
        return today - timedelta(days=2)
    if any(token in q for token in ("vcera", "yesterday")):
        return today - timedelta(days=1)
    if any(token in q for token in ("dnes", "today", "nyni", "ted")):
        return today

    iso_match = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", q)
    if iso_match:
        try:
            return datetime.strptime(iso_match.group(1), "%Y-%m-%d").date()
        except ValueError:
            pass

    tr_match = re.search(r"\b(\d{1,2})[./-](\d{1,2})[./-](20\d{2})\b", q)
    if tr_match:
        day_s, month_s, year_s = tr_match.groups()
        try:
            return date(int(year_s), int(month_s), int(day_s))
        except ValueError:
            pass

    return None


def _date_from_file(path: Path | None) -> date | None:
    if not path:
        return None
    match = re.search(r"HealthAutoExport-(\d{4}-\d{2}-\d{2})", path.name)
    if not match:
        return None
    try:
        return datetime.strptime(match.group(1), "%Y-%m-%d").date()
    except ValueError:
        return None


def _find_health_file(target_date: date | None = None) -> Path | None:
    """
    Najde nejnovější soubor HealthAutoExport-*.json.
    Nejprve zkusí hlavní adresář, potom starší umístění.
    """
    search_dirs = [HEALTH_DIR] + _LEGACY_DIRS
    if target_date:
        target_name = f"HealthAutoExport-{target_date.isoformat()}.json"
        for directory in search_dirs:
            candidate = directory / target_name
            if candidate.exists():
                return candidate
    for directory in search_dirs:
        if not directory.exists():
            continue
        candidates = sorted(
            directory.glob("HealthAutoExport-*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if candidates:
            return candidates[0]
    return None


def _resolve_file(target_date: date | None = None) -> Path | None:
    """Vrátí nejnovější zdravotní soubor, přednostně z nového umístění."""
    latest_export = _find_health_file(target_date)
    if latest_export:
        return latest_export
    if _LEGACY_FILE.exists():
        return _LEGACY_FILE
    return None


# ── Pomocné funkce ───────────────────────────────────────────────────────────

def _age_str(ts: float) -> str:
    mins = (time.time() - ts) / 60
    if mins < 2:   return "právě teď"
    if mins < 60:  return f"před {int(mins)} min"
    hrs = mins / 60
    if hrs < 24:   return f"před {hrs:.1f} hod"
    return f"před {hrs/24:.1f} dny"


def _v(d: dict, key: str, unit: str = "", dec: int = 0) -> str:
    val = d.get(key)
    if val is None:
        return "—"
    try:
        f = float(val)
        return f"{f:.{dec}f}{unit}" if dec else f"{int(round(f))}{unit}"
    except (ValueError, TypeError):
        return str(val)


# ── Zpracování formátu zdravotního exportu ───────────────────────────────────

def _parse_hae(raw: dict, target_date: date | None = None) -> dict:
    """
    Převede kombinovaný formát zdravotního exportu na plochý slovník.
    Format: {"data": {"metrics": [{"name": "heart_rate", "data": [{"qty": 72, ...}]}]}}
    """
    out = {}

    metrics_list = (
        raw.get("data", {}).get("metrics")          # combined format
        or raw.get("metrics")                        # alternatif
        or []
    )

    def latest_qty(entries: list) -> float | None:
        """Získá poslední hodnotu qty/value ze seznamu."""
        for entry in reversed(entries):
            for key in ("qty", "value", "Avg", "avg"):
                if key in entry:
                    try:
                        return float(entry[key])
                    except (ValueError, TypeError):
                        pass
        return None

    day_key = target_date.isoformat() if target_date else time.strftime("%Y-%m-%d")

    def today_sum(entries: list) -> float:
        """Sečte všechny záznamy cílového dne."""
        total = 0.0
        for e in entries:
            date_str = str(e.get("date", ""))
            if day_key in date_str:
                for key in ("qty", "value"):
                    if key in e:
                        try:
                            total += float(e[key])
                        except (ValueError, TypeError):
                            pass
        return total

    name_map = {
        # Název pole exportu → interní klíč.
        "heart_rate":                  ("heart_rate",       "latest"),
        "resting_heart_rate":          ("resting_hr",       "latest"),
        "heart_rate_variability":      ("hrv",              "latest"),
        "heart_rate_variability_sdnn": ("hrv",              "latest"),
        "heartratevariabilitysdnn":    ("hrv",              "latest"),
        "blood_oxygen_saturation":     ("blood_oxygen_raw", "latest"),
        "oxygen_saturation":           ("blood_oxygen_raw", "latest"),
        "respiratory_rate":            ("respiratory_rate", "latest"),
        "step_count":                  ("steps",            "today_sum"),
        "steps":                       ("steps",            "today_sum"),
        "active_energy":               ("calories",         "today_sum"),
        "active_energy_burned":        ("calories",         "today_sum"),
        "basal_energy_burned":         ("basal_calories",   "today_sum"),
        "apple_exercise_time":         ("exercise_min",     "today_sum"),
        "exercise_time":               ("exercise_min",     "today_sum"),
        "exercise_minutes":            ("exercise_min",     "today_sum"),
        "apple_stand_hour":            ("stand_hours",      "today_sum"),
        "apple_stand_time":            ("stand_min",        "today_sum"),
        "time_in_daylight":            ("daylight_min",     "today_sum"),
        "flights_climbed":             ("flights_climbed",  "today_sum"),
        "walking_heart_rate_average":  ("walking_hr",       "latest"),
        "walking_speed":               ("walking_speed",    "latest"),
        "walking_asymmetry_percentage": ("walking_asymmetry_pct", "latest"),
        "walking_double_support_percentage": ("walking_double_support_pct", "latest"),
        "walking_step_length":         ("walking_step_length_cm", "latest"),
        "walking_running_distance":    ("walking_distance_km", "today_sum"),
        "environmental_audio_exposure": ("environment_audio_db", "latest"),
        "headphone_audio_exposure":    ("headphone_audio_db", "latest"),
        "physical_effort":             ("physical_effort",   "latest"),
        "sleep_analysis":              ("sleep_hours",      "latest"),
        "sleep_duration":              ("sleep_hours",      "latest"),
    }

    for metric in metrics_list:
        raw_name = metric.get("name", "").lower().replace(" ", "_")
        entries  = metric.get("data", [])
        if not entries:
            continue

        mapping = name_map.get(raw_name)
        if not mapping:
            continue
        our_key, mode = mapping

        if mode == "latest":
            val = latest_qty(entries)
        else:
            val = today_sum(entries)

        if val is not None:
            out[our_key] = val

    # Saturace kyslíku obvykle přichází jako 0,0–1,0; převedeme ji na 0–100.
    if "blood_oxygen_raw" in out:
        raw_o2 = out.pop("blood_oxygen_raw")
        out["blood_oxygen"] = raw_o2 * 100 if raw_o2 <= 1.0 else raw_o2

    return out


def _load(target_date: date | None = None) -> tuple[dict, float, dict, date | None]:
    """Načte JSON a vrátí (data, časové_razítko, původní_json, cílové_datum)."""
    source_file = _resolve_file(target_date)
    if not source_file:
        raise FileNotFoundError("Soubor zdravotních dat nebyl nalezen.")

    raw = json.loads(source_file.read_text(encoding="utf-8"))
    file_mtime = source_file.stat().st_mtime
    source_date = _date_from_file(source_file) or target_date

    # Vlastní jednoduchý formát.
    if "data" in raw and isinstance(raw["data"], dict) and "metrics" not in raw.get("data", {}):
        return raw["data"], raw.get("timestamp", file_mtime), raw, source_date

    # Formát exportu.
    if "data" in raw and "metrics" in raw.get("data", {}):
        return _parse_hae(raw, source_date), file_mtime, raw, source_date

    # Plochý slovník ve starším jednoduchém formátu.
    return raw, file_mtime, raw, source_date


def _metrics_list(raw: dict) -> list:
    return raw.get("data", {}).get("metrics") or raw.get("metrics") or []


def _entry_datetime(entry: dict) -> datetime | None:
    raw_value = str(entry.get("date", "")).strip()
    if not raw_value:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S %z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            return datetime.strptime(raw_value, fmt)
        except ValueError:
            continue
    return None


def _entry_number(entry: dict, keys: tuple[str, ...] = ("qty", "value", "Avg", "avg", "Max", "max")) -> float | None:
    for key in keys:
        if key in entry:
            try:
                return float(entry[key])
            except (ValueError, TypeError):
                continue
    return None


def _entries_for_metric(raw: dict, names: tuple[str, ...], target_date: date | None = None) -> list[dict]:
    wanted = {name.lower().replace(" ", "_") for name in names}
    day_key = target_date.isoformat() if target_date else None
    matched = []
    for metric in _metrics_list(raw):
        raw_name = str(metric.get("name", "")).lower().replace(" ", "_")
        if raw_name not in wanted:
            continue
        for entry in metric.get("data", []) or []:
            if not day_key or day_key in str(entry.get("date", "")):
                matched.append(entry)
    return matched


def _float_or_none(data: dict, key: str) -> float | None:
    value = data.get(key)
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _period_label(target_date: date | None) -> str:
    if not target_date:
        return "Vybraný den"
    if target_date == date.today():
        return "Dnes"
    if target_date == date.today() - timedelta(days=1):
        return "Včera"
    return target_date.strftime("%d.%m.%Y")


def _build_health_analysis(raw: dict, data: dict, query: str, target_date: date | None, age: str) -> str:
    period = _period_label(target_date)
    exercise_min = _float_or_none(data, "exercise_min") or 0.0
    calories = _float_or_none(data, "calories") or 0.0
    steps = _float_or_none(data, "steps") or 0.0
    distance = _float_or_none(data, "walking_distance_km") or 0.0
    walking_speed = _float_or_none(data, "walking_speed")
    hrv = _float_or_none(data, "hrv")
    resting_hr = _float_or_none(data, "resting_hr")
    current_hr = _float_or_none(data, "heart_rate")
    effort = _float_or_none(data, "physical_effort")

    exercise_entries = [
        e for e in _entries_for_metric(raw, ("apple_exercise_time", "exercise_time", "exercise_minutes"), target_date)
        if (_entry_number(e, ("qty", "value")) or 0) > 0
    ]
    heart_entries = _entries_for_metric(raw, ("heart_rate",), target_date)

    exercise_times = [dt for e in exercise_entries if (dt := _entry_datetime(e))]
    workout_window = ""
    if exercise_times:
        workout_window = f"{min(exercise_times).strftime('%H:%M')} - {max(exercise_times).strftime('%H:%M')}"

    peak_hr = None
    avg_hr_values = []
    for entry in heart_entries:
        peak_candidate = _entry_number(entry, ("Max", "qty", "value", "Avg", "avg"))
        avg_candidate = _entry_number(entry, ("Avg", "avg", "qty", "value"))
        if peak_candidate is not None:
            peak_hr = peak_candidate if peak_hr is None else max(peak_hr, peak_candidate)
        if avg_candidate is not None:
            avg_hr_values.append(avg_candidate)
    avg_hr = (sum(avg_hr_values) / len(avg_hr_values)) if avg_hr_values else None

    lines = []
    if any(k in _normalize_query(query) for k in ("trenink", "workout", "cviceni", "sport", "fitness")):
        if exercise_min >= 10:
            lines.append(f"{period}: je zaznamenán výrazný trénink nebo cvičení.")
        elif exercise_min > 0:
            lines.append(f"{period}: je zaznamenán krátký pohyb, ale ne plnohodnotný trénink.")
        else:
            lines.append(f"{period}: není zaznamenán výrazný trénink.")
    else:
        lines.append(f"Zdravotní analýza pro období {period.lower()} je připravena.")

    lines.append(f"Doba cvičení: {int(round(exercise_min))} min.")
    lines.append(f"Aktivní kalorie: {int(round(calories))} kcal, kroky: {int(round(steps))}, vzdálenost: {distance:.2f} km.")
    if workout_window:
        lines.append(f"Nejvýraznější interval aktivity: {workout_window}.")
    if peak_hr is not None:
        hr_text = f"Maximální tep přibližně {int(round(peak_hr))} bpm"
        if avg_hr is not None:
            hr_text += f", denní průměrný tep přibližně {int(round(avg_hr))} bpm"
        lines.append(hr_text + ".")
    if walking_speed is not None:
        lines.append(f"Rychlost chůze přibližně {walking_speed:.1f} km/h.")

    if exercise_min >= 60 or calories >= 600:
        lines.append("Hodnocení: zátěž byla vysoká a den velmi aktivní.")
    elif exercise_min >= 30 or calories >= 300:
        lines.append("Hodnocení: střední zátěž a účelně aktivní den.")
    elif steps >= 7000:
        lines.append("Hodnocení: výrazně aktivní den s chůzí.")
    else:
        lines.append("Hodnocení: lehká zátěž na úrovni běžného denního pohybu.")

    recovery_notes = []
    if hrv is not None:
        if hrv >= 70:
            recovery_notes.append(f"HRV {hrv:.1f} ms vypadá dobře")
        elif hrv >= 40:
            recovery_notes.append(f"HRV {hrv:.1f} ms je ve středním pásmu")
        else:
            recovery_notes.append(f"HRV {hrv:.1f} ms je spíše nízké")
    if resting_hr is not None:
        recovery_notes.append(f"klidový tep {int(round(resting_hr))} bpm")
    elif current_hr is not None:
        recovery_notes.append(f"poslední naměřený tep {int(round(current_hr))} bpm")
    if recovery_notes:
        lines.append("Regenerace: " + ", ".join(recovery_notes) + ".")

    if effort is not None:
        lines.append(f"Skóre fyzické námahy je přibližně {effort:.1f}.")

    lines.append(f"[aktualizace: {age}]")
    return "\n".join(lines)


# ── Formátování ──────────────────────────────────────────────────────────────

def _format(data: dict, query: str, age: str) -> str:
    q = _normalize_query(query)

    if any(k in q for k in ("tep", "srdecni", "srdce", "heart", "bpm", "hrv")):
        return "\n".join([
            f"Aktuální tep : {_v(data, 'heart_rate', ' bpm')}",
            f"Klidový tep  : {_v(data, 'resting_hr', ' bpm')}",
            f"HRV            : {_v(data, 'hrv', ' ms', 1)}",
            f"Tep při chůzi : {_v(data, 'walking_hr', ' bpm')}",
            f"[aktualizace: {age}]",
        ])

    if any(k in q for k in ("krok", "step", "cviceni", "exercise", "kalorie", "aktivita", "activity", "kardio", "stand", "stani", "vzdalenost", "distance", "patro")):
        return "\n".join([
            f"Dnešní kroky   : {_v(data, 'steps')}",
            f"Aktivní kalorie: {_v(data, 'calories', ' kcal')}",
            f"Bazální kalorie: {_v(data, 'basal_calories', ' kcal')}",
            f"Doba cvičení   : {_v(data, 'exercise_min', ' min')}",
            f"Hodiny stání   : {_v(data, 'stand_hours', ' hod')}",
            f"Doba stání     : {_v(data, 'stand_min', ' min')}",
            f"Vzdálenost chůze: {_v(data, 'walking_distance_km', ' km', 2)}",
            f"Vystoupaná patra: {_v(data, 'flights_climbed')}",
            f"[aktualizace: {age}]",
        ])

    if any(k in q for k in ("chuze", "walking", "mobilita", "rovnovaha", "asymetrie", "asymmetry", "rychlost", "delka kroku", "step length", "double support")):
        return "\n".join([
            f"Rychlost chůze : {_v(data, 'walking_speed', ' km/h', 1)}",
            f"Délka kroku    : {_v(data, 'walking_step_length_cm', ' cm')}",
            f"Tep při chůzi  : {_v(data, 'walking_hr', ' bpm')}",
            f"Asymetrie      : {_v(data, 'walking_asymmetry_pct', '%', 1)}",
            f"Dvojitá opora  : {_v(data, 'walking_double_support_pct', '%', 1)}",
            f"Vzdálenost     : {_v(data, 'walking_distance_km', ' km', 2)}",
            f"[aktualizace: {age}]",
        ])

    if any(k in q for k in ("spanek", "sleep", "spal")):
        return "\n".join([
            f"Doba spánku    : {_v(data, 'sleep_hours', ' hod', 1)}",
            f"Hluboký spánek : {_v(data, 'deep_sleep_hours', ' hod', 1)}",
            f"REM spánek     : {_v(data, 'rem_sleep_hours', ' hod', 1)}",
            f"[aktualizace: {age}]",
        ])

    if any(k in q for k in ("kyslik", "spo2", "oxygen", "dychani")):
        return "\n".join([
            f"Kyslík v krvi  : {_v(data, 'blood_oxygen', '%', 1)}",
            f"Dechová frekvence: {_v(data, 'respiratory_rate', ' dechů/min', 1)}",
            f"[aktualizace: {age}]",
        ])

    if any(k in q for k in ("zvuk", "audio", "sluchatka", "hluk", "expozice", "decibel", "db", "headphone", "environmental")):
        return "\n".join([
            f"Hluk prostředí : {_v(data, 'environment_audio_db', ' dB', 1)}",
            f"Zvuk sluchátek : {_v(data, 'headphone_audio_db', ' dB', 1)}",
            f"[aktualizace: {age}]",
        ])

    if any(k in q for k in ("denni svetlo", "daylight", "slunce")):
        return "\n".join([
            f"Denní světlo   : {_v(data, 'daylight_min', ' min', 1)}",
            f"Fyzická námaha : {_v(data, 'physical_effort', '', 1)}",
            f"[aktualizace: {age}]",
        ])

    return "\n".join([
        "── ZDRAVOTNÍ SOUHRN ──────────────",
        f"💓 Tep           : {_v(data, 'heart_rate', ' bpm')}  (klid: {_v(data, 'resting_hr', ' bpm')})",
        f"📊 HRV           : {_v(data, 'hrv', ' ms', 1)}",
        f"🚶 Tep při chůzi : {_v(data, 'walking_hr', ' bpm')}",
        f"🩸 Kyslík v krvi : {_v(data, 'blood_oxygen', '%', 1)}",
        f"🫁 Dechová frekvence: {_v(data, 'respiratory_rate', ' dechů/min', 1)}",
        f"👣 Kroky         : {_v(data, 'steps')}",
        f"🔥 Aktivní kalorie: {_v(data, 'calories', ' kcal')}",
        f"⚡ Bazální kalorie: {_v(data, 'basal_calories', ' kcal')}",
        f"🏃 Cvičení       : {_v(data, 'exercise_min', ' min')}",
        f"🧍 Stání         : {_v(data, 'stand_hours', ' hod')}  ({_v(data, 'stand_min', ' min')})",
        f"🪜 Vystoupaná patra: {_v(data, 'flights_climbed')}",
        f"📏 Vzdálenost    : {_v(data, 'walking_distance_km', ' km', 2)}",
        f"🚀 Rychlost chůze: {_v(data, 'walking_speed', ' km/h', 1)}",
        f"📐 Délka kroku   : {_v(data, 'walking_step_length_cm', ' cm')}",
        f"🎧 Zvuk sluchátek: {_v(data, 'headphone_audio_db', ' dB', 1)}",
        f"🌤 Denní světlo  : {_v(data, 'daylight_min', ' min', 1)}",
        f"💤 Spánek        : {_v(data, 'sleep_hours', ' hod', 1)}",
        f"──────────────────────────────────",
        f"[aktualizace: {age}]",
    ])


# ── Hlavní funkce ────────────────────────────────────────────────────────────

def get_health_data(query: str = "all") -> str:
    target_date = _extract_target_date(query)

    if not _resolve_file(target_date):
        return (
            "Zdravotní data nebyla nalezena. "
            "Na iPhonu nastavte podporovanou aplikaci pro export zdravotních dat "
            "do složky iCloud Drive > Auto Export > JARVIS."
        )

    try:
        data, ts, raw, source_date = _load(target_date)
    except Exception as e:
        return f"Soubor zdravotních dat se nepodařilo načíst: {e}"

    if not data:
        return "Soubor zdravotních dat je prázdný nebo má nerozpoznaný formát."

    age   = _age_str(ts)
    normalized_query = _normalize_query(query)
    if any(token in normalized_query for token in ("analyza", "hodnoceni", "detail", "podrobne", "trenink", "workout", "fitness", "vcera", "yesterday")):
        result = _build_health_analysis(raw, data, query, source_date, age)
    else:
        result = _format(data, query, age)

    mins_old = (time.time() - ts) / 60
    if mins_old > STALE_WARN_MINUTES:
        result += f"\n⚠️  Data byla aktualizována {age}. Zkontrolujte automatický export aplikace."

    return result


def get_welcome_health_summary() -> str:
    if not _resolve_file():
        return "Zdravotní data momentálně nejsou dostupná."

    try:
        data, ts, _, _ = _load()
    except Exception:
        return "Zdravotní data momentálně nejsou dostupná."

    if not data:
        return "Zdravotní data momentálně nejsou dostupná."

    heart_rate = _v(data, "heart_rate", " bpm")
    steps = _v(data, "steps")
    exercise_min = _v(data, "exercise_min", " min")
    distance = _v(data, "walking_distance_km", " km", 2)
    age = _age_str(ts)

    parts = []
    if heart_rate != "—":
        parts.append(f"aktuální tep je {heart_rate}")
    if exercise_min != "—":
        parts.append(f"dnes proběhlo {exercise_min} kardio cvičení")
    if steps != "—":
        parts.append(f"počet kroků je {steps}")
    if distance != "—":
        parts.append(f"ujitá vzdálenost je {distance}")

    if not parts:
        return "Zdravotní data momentálně nejsou dostupná."

    if len(parts) == 1:
        summary = parts[0] + "."
    else:
        summary = ", ".join(parts[:-1]) + f" a {parts[-1]}."

    mins_old = (time.time() - ts) / 60
    if mins_old > STALE_WARN_MINUTES:
        summary += f" Zdravotní data byla aktualizována {age}."

    return summary
