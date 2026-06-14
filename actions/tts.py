"""
TTS (Text-to-Speech) - uses PowerShell SAPI on Windows.
Requires no extra setup and supports built-in Windows voices.
"""

import subprocess
import threading


def speak_text(text: str, on_done=None, blocking: bool = False):
    """
    Reads text aloud with Windows SAPI.
    on_done: optional callback called when speech finishes.
    blocking: wait until speech finishes when True.
    """
    if not text or not text.strip():
        if on_done:
            on_done()
        return

    max_len = 500
    if len(text) > max_len:
        text = text[:max_len] + "..."

    safe_text = text.replace("'", "''").replace('"', '`"')
    script = (
        "Add-Type -AssemblyName System.Speech; "
        f"$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$s.Speak('{safe_text}')"
    )

    def _run():
        try:
            subprocess.run(
                ["powershell", "-WindowStyle", "Hidden", "-Command", script],
                check=False,
                timeout=60,
            )
        except Exception:
            pass
        if on_done:
            on_done()

    if blocking:
        _run()
    else:
        threading.Thread(target=_run, daemon=True).start()


def get_available_voices() -> list[str]:
    """List the available SAPI voices on Windows."""
    try:
        script = (
            "Add-Type -AssemblyName System.Speech; "
            "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            "$s.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name }"
        )
        result = subprocess.run(
            ["powershell", "-Command", script],
            capture_output=True, text=True, timeout=10,
        )
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except Exception:
        return []
