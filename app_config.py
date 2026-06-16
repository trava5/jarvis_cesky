# Created by Alp Unlu - @alppunlu
from __future__ import annotations

import json
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
LEGACY_CONFIG_PATH = BASE_DIR / "config" / "api_keys.json"


DEFAULT_CONFIG = {
    "gemini_api_key": "",
    "voice": "Charon",
    "youtube_api_key": "",
    "youtube_channel_handle": "",
}

ENV_KEY_MAP = {
    "gemini_api_key": "GEMINI_API_KEY",
    "voice": "JARVIS_VOICE",
    "youtube_api_key": "YOUTUBE_API_KEY",
    "youtube_channel_handle": "YOUTUBE_CHANNEL_HANDLE",
}


def _decode_env_value(raw_value: str) -> str:
    value = raw_value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            decoded = json.loads(value)
            return decoded if isinstance(decoded, str) else str(decoded)
        except (TypeError, ValueError, json.JSONDecodeError):
            return value[1:-1]
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1]
    return value


def _parse_env_assignment(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    if stripped.startswith("export "):
        stripped = stripped[7:].lstrip()
    key, separator, raw_value = stripped.partition("=")
    key = key.strip()
    if not separator or not key or not key.replace("_", "").isalnum():
        return None
    return key, _decode_env_value(raw_value)


def _read_env_values() -> dict[str, str]:
    values: dict[str, str] = {}
    try:
        lines = ENV_PATH.read_text(encoding="utf-8").splitlines()
    except (FileNotFoundError, OSError, UnicodeError):
        return values

    for line in lines:
        assignment = _parse_env_assignment(line)
        if assignment is not None:
            key, value = assignment
            values[key] = value
    return values


def _encode_env_value(value: object) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def _write_env_updates(updates: dict[str, object]) -> None:
    try:
        lines = ENV_PATH.read_text(encoding="utf-8").splitlines()
    except (FileNotFoundError, OSError, UnicodeError):
        lines = []

    pending = {key: str(value) for key, value in updates.items()}
    output: list[str] = []
    for line in lines:
        assignment = _parse_env_assignment(line)
        if assignment is None:
            output.append(line)
            continue
        key, _ = assignment
        if key in pending:
            output.append(f"{key}={_encode_env_value(pending.pop(key))}")
        else:
            output.append(line)

    if output and output[-1]:
        output.append("")
    output.extend(f"{key}={_encode_env_value(value)}" for key, value in pending.items())

    temp_path = ENV_PATH.with_name(f"{ENV_PATH.name}.tmp")
    temp_path.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")
    temp_path.replace(ENV_PATH)


def _load_env_into_process() -> None:
    for key, value in _read_env_values().items():
        os.environ.setdefault(key, value)


def migrate_legacy_config_to_env() -> bool:
    if not LEGACY_CONFIG_PATH.exists():
        return False

    try:
        legacy = json.loads(LEGACY_CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return False
    if not isinstance(legacy, dict):
        return False

    env_values = _read_env_values()
    updates: dict[str, object] = {}
    for config_key, env_key in ENV_KEY_MAP.items():
        current_value = env_values.get(env_key, "")
        if current_value:
            continue
        legacy_value = legacy.get(config_key, DEFAULT_CONFIG[config_key])
        if legacy_value is not None:
            updates[env_key] = legacy_value

    try:
        if updates:
            _write_env_updates(updates)
        LEGACY_CONFIG_PATH.unlink()
    except OSError:
        return False

    for key, value in updates.items():
        os.environ.setdefault(key, str(value))
    return True


def load_app_config() -> dict:
    migrate_legacy_config_to_env()
    _load_env_into_process()

    config = dict(DEFAULT_CONFIG)
    env_values = _read_env_values()
    for config_key, env_key in ENV_KEY_MAP.items():
        if env_key in os.environ:
            config[config_key] = os.environ[env_key]
        elif env_key in env_values:
            config[config_key] = env_values[env_key]
    return config


def save_app_config(updates: dict) -> dict:
    migrate_legacy_config_to_env()

    env_updates: dict[str, object] = {}
    for config_key, value in (updates or {}).items():
        env_key = ENV_KEY_MAP.get(config_key)
        if env_key is None or value is None:
            continue
        env_updates[env_key] = value

    if env_updates:
        _write_env_updates(env_updates)
        for key, value in env_updates.items():
            os.environ[key] = str(value)
    return load_app_config()


def get_app_config_value(key: str, default=None):
    return load_app_config().get(key, default)


def has_gemini_api_key() -> bool:
    value = str(get_app_config_value("gemini_api_key", "") or "").strip()
    return bool(value)


migrate_legacy_config_to_env()
_load_env_into_process()
