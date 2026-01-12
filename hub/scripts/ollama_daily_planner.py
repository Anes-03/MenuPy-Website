#!/usr/bin/env python3
"""
Name: Tagesplanung (Ollama)
Description: Erstellt eine priorisierte Tagesplanung aus Clipboard-Tasks.
Requirements: ollama (https://ollama.com)
"""
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess

# --- Konfiguration ---
MODEL = "llama3.1"
MAX_CHARS = 12000
OUTPUT_DIR = Path.home() / "Documents" / "Planning"
SAVE_TO_FILE = True


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
    tasks = get_clipboard().strip()
    if not tasks:
        notify("Clipboard", "Kein Text im Clipboard")
        return

    if len(tasks) > MAX_CHARS:
        tasks = tasks[:MAX_CHARS]

    prompt = (
        "Du bist ein Planungsassistent. Erstelle eine Tagesplanung mit Prioritaeten "
        "und Zeitbloecken. Gib eine klare Reihenfolge und realistische Dauer an.\n\n"
        "Aufgaben:\n"
        f"{tasks}"
    )

    plan = run_ollama(prompt)
    if not plan:
        return

    set_clipboard(plan)

    if SAVE_TO_FILE:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = OUTPUT_DIR / "day-plan.txt"
        out_path.write_text(plan, encoding="utf-8")

    notify("Ollama", "Tagesplan erstellt")


if __name__ == "__main__":
    main()
