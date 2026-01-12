#!/usr/bin/env python3
"""
Name: Projekt Starter
Description: Oeffnet definierte Ordner, Apps und URLs mit einem Klick.
"""
from __future__ import annotations

from pathlib import Path
import subprocess
import time

# --- Konfiguration ---
FOLDERS = [
    Path.home() / "Projects",
]

APPS = [
    "Visual Studio Code",
    "Safari",
]

URLS = [
    "https://github.com",
]

DELAY_SECONDS = 0.2


def notify(title: str, message: str) -> None:
    try:
        subprocess.run(
            ["osascript", "-e", f'display notification "{message}" with title "{title}"'],
            check=False,
        )
    except Exception:
        pass


def main() -> None:
    for folder in FOLDERS:
        if folder.exists():
            subprocess.run(["open", str(folder)], check=False)
            time.sleep(DELAY_SECONDS)

    for app in APPS:
        subprocess.run(["open", "-a", app], check=False)
        time.sleep(DELAY_SECONDS)

    for url in URLS:
        subprocess.run(["open", url], check=False)
        time.sleep(DELAY_SECONDS)

    notify("Projekt Starter", "Alles geoeffnet")


if __name__ == "__main__":
    main()
