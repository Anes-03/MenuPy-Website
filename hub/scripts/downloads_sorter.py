#!/usr/bin/env python3
"""
Name: Downloads aufraeumen
Description: Sortiert alte Dateien in ~/Downloads nach Typ und optional nach Monat.
Note: Passe die Konfiguration unten an deine Beduerfnisse an.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import os
import shutil
import subprocess
import time

# --- Konfiguration ---
DOWNLOADS_DIR = Path.home() / "Downloads"
MAX_AGE_DAYS = 14  # None, um alles zu bewegen
MOVE_BY_DATE = True
DATE_FOLDER_FORMAT = "%Y-%m"
DRY_RUN = False

EXTENSION_MAP = {
    "pdf": "PDF",
    "zip": "Archive",
    "rar": "Archive",
    "7z": "Archive",
    "dmg": "Installer",
    "pkg": "Installer",
    "jpg": "Bilder",
    "jpeg": "Bilder",
    "png": "Bilder",
    "heic": "Bilder",
    "gif": "Bilder",
    "mp4": "Videos",
    "mov": "Videos",
    "mp3": "Audio",
    "wav": "Audio",
    "csv": "Daten",
    "xlsx": "Daten",
    "xls": "Daten",
    "doc": "Dokumente",
    "docx": "Dokumente",
}
DEFAULT_FOLDER = "Sonstiges"


def notify(title: str, message: str) -> None:
    try:
        subprocess.run(
            ["osascript", "-e", f'display notification "{message}" with title "{title}"'],
            check=False,
        )
    except Exception:
        pass


def is_old_enough(path: Path) -> bool:
    if MAX_AGE_DAYS is None:
        return True
    cutoff = time.time() - (MAX_AGE_DAYS * 86400)
    return path.stat().st_mtime < cutoff


def target_folder(path: Path) -> Path:
    ext = path.suffix.lower().lstrip(".")
    folder = EXTENSION_MAP.get(ext, DEFAULT_FOLDER)
    base = DOWNLOADS_DIR / folder
    if MOVE_BY_DATE:
        stamp = datetime.fromtimestamp(path.stat().st_mtime).strftime(DATE_FOLDER_FORMAT)
        return base / stamp
    return base


def main() -> None:
    if not DOWNLOADS_DIR.exists():
        notify("Downloads", "Ordner nicht gefunden")
        return

    moved = 0
    skipped = 0

    for item in DOWNLOADS_DIR.iterdir():
        if item.is_dir():
            continue
        if item.name.startswith("."):
            continue
        if not is_old_enough(item):
            skipped += 1
            continue

        dest_dir = target_folder(item)
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / item.name

        if DRY_RUN:
            print(f"DRY_RUN: {item} -> {dest_path}")
            moved += 1
            continue

        try:
            shutil.move(str(item), str(dest_path))
            moved += 1
        except Exception as exc:
            print(f"Fehler beim Verschieben von {item}: {exc}")

    notify("Downloads aufgeraeumt", f"Verschoben: {moved}, Uebersprungen: {skipped}")


if __name__ == "__main__":
    main()
