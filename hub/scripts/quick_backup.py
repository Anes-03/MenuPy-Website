#!/usr/bin/env python3
"""
Name: Backup Schnellschuss
Description: Erstellt ein ZIP-Backup eines Ordners in einem Backup-Verzeichnis.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil
import subprocess

# --- Konfiguration ---
SOURCE_DIR = Path.home() / "Documents"
BACKUP_DIR = Path.home() / "Backups"
ZIP_PREFIX = "Documents"
KEEP_LAST = 10  # aeltere Backups loeschen, None fuer unbegrenzt


def notify(title: str, message: str) -> None:
    try:
        subprocess.run(
            ["osascript", "-e", f'display notification "{message}" with title "{title}"'],
            check=False,
        )
    except Exception:
        pass


def cleanup_old_backups() -> None:
    if KEEP_LAST is None:
        return
    archives = sorted(BACKUP_DIR.glob(f"{ZIP_PREFIX}-*.zip"))
    if len(archives) <= KEEP_LAST:
        return
    for old in archives[: -KEEP_LAST]:
        old.unlink(missing_ok=True)


def main() -> None:
    if not SOURCE_DIR.exists():
        notify("Backup", "Quelle nicht gefunden")
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_name = BACKUP_DIR / f"{ZIP_PREFIX}-{stamp}"

    try:
        archive_path = shutil.make_archive(str(base_name), "zip", str(SOURCE_DIR))
        cleanup_old_backups()
        notify("Backup", f"Fertig: {Path(archive_path).name}")
    except Exception as exc:
        notify("Backup", f"Fehler: {exc}")


if __name__ == "__main__":
    main()
