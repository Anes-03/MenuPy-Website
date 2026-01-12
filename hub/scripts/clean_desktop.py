#!/usr/bin/env python3
"""
Name: Schreibtisch aufräumen
Description: Verschiebt alle Dateien vom Schreibtisch in einen Archiv-Ordner.
"""
import os
import shutil
from pathlib import Path
from datetime import datetime
import subprocess

DESKTOP = Path.home() / "Desktop"
ARCHIVE = Path.home() / "Documents" / "Desktop Architecture" / datetime.now().strftime("%Y-%m-%d")

def notify(title, message):
    try:
        subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'], check=False)
    except:
        pass

def clean_desktop():
    if not DESKTOP.exists():
        return "Desktop-Ordner nicht gefunden."
    
    files = [f for f in DESKTOP.iterdir() if f.is_file() and not f.name.startswith('.')]
    
    if not files:
        return "Der Schreibtisch ist bereits sauber!"
    
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    count = 0
    
    for f in files:
        try:
            shutil.move(str(f), str(ARCHIVE / f.name))
            count += 1
        except Exception as e:
            print(f"Fehler bei {f.name}: {e}")
            
    return f"{count} Dateien nach {ARCHIVE.relative_to(Path.home())} verschoben."

if __name__ == "__main__":
    result = clean_desktop()
    notify("Desktop Cleanup", result)
    print(result)
