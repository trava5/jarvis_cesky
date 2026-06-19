"""ElevenLabs text-to-speech provider."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

from app_config import get_app_config_value


ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


class ElevenLabsVoiceError(RuntimeError):
    """Chyba hlasového provideru ElevenLabs."""


class ElevenLabsPaymentRequiredError(ElevenLabsVoiceError):
    """ElevenLabs účet nemá dostupný kredit nebo vyžaduje platbu."""


@dataclass(frozen=True)
class ElevenLabsVoiceConfig:
    api_key: str
    voice_id: str
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"
    stability: float | None = None
    similarity_boost: float | None = None
    style: float | None = None
    use_speaker_boost: bool | None = None


def _clean_text(text: str, max_chars: int = 2500) -> str:
    cleaned = " ".join(str(text or "").split())
    if len(cleaned) > max_chars:
        return cleaned[:max_chars].rstrip() + "..."
    return cleaned


def _accept_header_for_output(output_format: str) -> str:
    if str(output_format or "").startswith("pcm_"):
        return "application/octet-stream"
    return "audio/mpeg"


def load_config() -> ElevenLabsVoiceConfig:
    api_key = str(
        get_app_config_value("elevenlabs_api_key", "")
        or get_app_config_value("eleven_labs_api_key", "")
        or ""
    ).strip()
    voice_id = str(get_app_config_value("elevenlabs_voice_id", "") or "").strip()
    model_id = str(
        get_app_config_value("elevenlabs_model_id", "eleven_multilingual_v2")
        or "eleven_multilingual_v2"
    ).strip()
    output_format = str(
        get_app_config_value("elevenlabs_output_format", "mp3_44100_128")
        or "mp3_44100_128"
    ).strip()
    return ElevenLabsVoiceConfig(
        api_key=api_key,
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format,
    )


def is_configured(config: ElevenLabsVoiceConfig | None = None) -> bool:
    selected = config or load_config()
    return bool(selected.api_key and selected.voice_id)


def build_text_to_speech_request(
    text: str,
    config: ElevenLabsVoiceConfig | None = None,
) -> tuple[str, dict[str, str], dict[str, Any], dict[str, str]]:
    selected = config or load_config()
    cleaned = _clean_text(text)
    if not cleaned:
        raise ElevenLabsVoiceError("Text pro hlasový výstup je prázdný.")
    if not selected.api_key:
        raise ElevenLabsVoiceError("Chybí ELEVENLABS_API_KEY nebo ELEVEN_LABS_API_KEY.")
    if not selected.voice_id:
        raise ElevenLabsVoiceError("Chybí ELEVENLABS_VOICE_ID.")

    payload: dict[str, Any] = {
        "text": cleaned,
        "model_id": selected.model_id,
    }

    voice_settings: dict[str, Any] = {}
    if selected.stability is not None:
        voice_settings["stability"] = selected.stability
    if selected.similarity_boost is not None:
        voice_settings["similarity_boost"] = selected.similarity_boost
    if selected.style is not None:
        voice_settings["style"] = selected.style
    if selected.use_speaker_boost is not None:
        voice_settings["use_speaker_boost"] = selected.use_speaker_boost
    if voice_settings:
        payload["voice_settings"] = voice_settings

    url = ELEVENLABS_TTS_URL.format(voice_id=selected.voice_id)
    headers = {
        "xi-api-key": selected.api_key,
        "Content-Type": "application/json",
        "Accept": _accept_header_for_output(selected.output_format),
    }
    params = {"output_format": selected.output_format}
    return url, headers, payload, params


def _raise_for_tts_status(response: requests.Response) -> None:
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        status_code = getattr(response, "status_code", None)
        detail = str(getattr(response, "text", "") or "").strip()
        detail_suffix = f" Detail: {detail[:300]}" if detail else ""
        if status_code == 402:
            raise ElevenLabsPaymentRequiredError(
                "ElevenLabs účet nemá dostupný kredit nebo vyžaduje platbu."
            ) from exc
        if status_code:
            raise ElevenLabsVoiceError(
                f"ElevenLabs TTS selhalo: HTTP {status_code}.{detail_suffix}"
            ) from exc
        raise ElevenLabsVoiceError(f"ElevenLabs TTS selhalo.{detail_suffix}") from exc


def synthesize_to_file(
    text: str,
    output_path: str | Path,
    config: ElevenLabsVoiceConfig | None = None,
    timeout: int = 60,
) -> Path:
    url, headers, payload, params = build_text_to_speech_request(text, config)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            params=params,
            timeout=timeout,
        )
        _raise_for_tts_status(response)
    except requests.RequestException as exc:
        raise ElevenLabsVoiceError(
            "ElevenLabs TTS selhalo: síťová chyba nebo nedostupné API."
        ) from exc

    target.write_bytes(response.content)
    return target


def synthesize_to_bytes(
    text: str,
    config: ElevenLabsVoiceConfig | None = None,
    timeout: int = 60,
) -> bytes:
    url, headers, payload, params = build_text_to_speech_request(text, config)
    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            params=params,
            timeout=timeout,
        )
        _raise_for_tts_status(response)
    except requests.RequestException as exc:
        raise ElevenLabsVoiceError(
            "ElevenLabs TTS selhalo: síťová chyba nebo nedostupné API."
        ) from exc
    return response.content
