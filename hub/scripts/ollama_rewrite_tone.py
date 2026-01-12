#!/usr/bin/env python3
"""
Name: Text umschreiben (Ollama)
Description: Schreibt Clipboard-Text in einer gewuenschten Tonalitaet um.
Requirements: ollama (https://ollama.com)
"""
from __future__ import annotations

import shutil
import subprocess

# --- Konfiguration ---
MODEL = "llama3.1"
TONE = "freundlich und klar"
MAX_CHARS = 12000


def notify(title: str, message: str) -> None:
    try:
        subprocess.run(
            ["osascript", "-e", f'display notification "{message}" with title "{title}"'],
            check=False,
        )
    except Exception:
        pass


def get_clipboard() -> str:
    result = subprocess.run(["pbpaste"], capture_output=True, check=False)
    return result.stdout.decode("utf-8", errors="ignore")


def set_clipboard(text: str) -> None:
    subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=False)


def run_ollama(prompt: str) -> str | None:
    if shutil.which("ollama") is None:
        notify("Ollama", "ollama ist nicht installiert")
        return None

    result = subprocess.run(
        ["ollama", "run", MODEL],
        input=prompt.encode("utf-8"),
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        notify("Ollama", "Fehler beim Modell")
        return None
    return result.stdout.decode("utf-8", errors="ignore").strip()


def main() -> None:
    text = get_clipboard().strip()
    if not text:
        notify("Clipboard", "Kein Text im Clipboard")
        return

    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]

    prompt = (
        "Schreibe den folgenden Text um. "
        f"Tonalitaet: {TONE}. "
        "Behalte die Bedeutung, aber optimiere Lesbarkeit.\n\nText:\n"
        f"{text}"
    )

    rewritten = run_ollama(prompt)
    if not rewritten:
        return

    set_clipboard(rewritten)
    notify("Ollama", "Umschrift kopiert")


if __name__ == "__main__":
    main()
