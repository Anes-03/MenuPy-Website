#!/usr/bin/env python3
"""
Name: Datei Zusammenfassung (Ollama)
Description: Fasst die neueste Textdatei in einem Ordner zusammen.
Requirements: ollama (https://ollama.com)
"""
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess

# --- Konfiguration ---
MODEL = "llama3.1"
WATCH_DIR = Path.home() / "Downloads"
EXTENSIONS = {".txt", ".md", ".log"}
RECURSIVE = False
MAX_CHARS = 16000
OUTPUT_DIR = Path.home() / "Documents" / "Summaries"


def notify(title: str, message: str) -> None:
    try:
        subprocess.run(
            ["osascript", "-e", f'display notification "{message}" with title "{title}"'],
            check=False,
        )
    except Exception:
        pass


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


def pick_latest_file() -> Path | None:
    if not WATCH_DIR.exists():
        return None

    if RECURSIVE:
        candidates = [p for p in WATCH_DIR.rglob("*") if p.suffix.lower() in EXTENSIONS]
    else:
        candidates = [p for p in WATCH_DIR.iterdir() if p.suffix.lower() in EXTENSIONS]

    candidates = [p for p in candidates if p.is_file()]
    if not candidates:
        return None

    return max(candidates, key=lambda p: p.stat().st_mtime)


def main() -> None:
    target = pick_latest_file()
    if not target:
        notify("Ollama", "Keine passende Datei gefunden")
        return

    text = target.read_text(encoding="utf-8", errors="ignore").strip()
    if not text:
        notify("Ollama", "Datei ist leer")
        return

    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]

    prompt = (
        "Fasse den folgenden Text in 5-8 Stichpunkten zusammen. "
        "Erwaehne Schluesselthemen und Ergebnisse.\n\nText:\n"
        f"{text}"
    )

    summary = run_ollama(prompt)
    if not summary:
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{target.stem}.summary.txt"
    out_path.write_text(summary, encoding="utf-8")
    notify("Ollama", f"Summary erstellt: {out_path.name}")


if __name__ == "__main__":
    main()
