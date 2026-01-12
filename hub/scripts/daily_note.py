#!/usr/bin/env python3
"""
Name: Tagesnotiz erstellen
Description: Legt eine neue Markdown-Notiz mit Datum an und oeffnet sie.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import subprocess

# --- Konfiguration ---
NOTES_DIR = Path.home() / "Documents" / "Notes"
OPEN_AFTER_CREATE = True

TEMPLATE = """# {date}

## Aufgaben
- 

## Notizen
- 
"""


def notify(title: str, message: str) -> None:
    try:
        subprocess.run(
            ["osascript", "-e", f'display notification "{message}" with title "{title}"'],
            check=False,
        )
    except Exception:
        pass


def main() -> None:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    note_path = NOTES_DIR / f"{today}.md"

    if not note_path.exists():
        note_path.write_text(TEMPLATE.format(date=today), encoding="utf-8")
        notify("Tagesnotiz", "Neue Notiz erstellt")
    else:
        notify("Tagesnotiz", "Notiz existiert bereits")

    if OPEN_AFTER_CREATE:
        subprocess.run(["open", str(note_path)], check=False)


if __name__ == "__main__":
    main()
