#!/usr/bin/env python3
"""
Name: Screenshot OCR
Description: Nimmt einen Screenshot, extrahiert Text via Tesseract und kopiert ihn.
Requirements: tesseract (Homebrew: brew install tesseract)
"""
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import tempfile

# --- Konfiguration ---
OCR_LANG = "deu+eng"
SAVE_TEXT_FILE = False
TEXT_OUTPUT_DIR = Path.home() / "Documents" / "OCR"


def notify(title: str, message: str) -> None:
    try:
        subprocess.run(
            ["osascript", "-e", f'display notification "{message}" with title "{title}"'],
            check=False,
        )
    except Exception:
        pass


def set_clipboard(text: str) -> None:
    subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=False)


def main() -> None:
    if shutil.which("tesseract") is None:
        notify("OCR", "tesseract fehlt. Installiere es via Homebrew.")
        return

    with tempfile.TemporaryDirectory() as tmp:
        img_path = Path(tmp) / "capture.png"
        result_base = Path(tmp) / "ocr"

        capture = subprocess.run(["screencapture", "-i", str(img_path)], check=False)
        if capture.returncode != 0 or not img_path.exists():
            notify("OCR", "Screenshot abgebrochen")
            return

        ocr = subprocess.run(
            ["tesseract", str(img_path), str(result_base), "-l", OCR_LANG],
            capture_output=True,
            check=False,
        )
        if ocr.returncode != 0:
            notify("OCR", "Tesseract Fehler")
            return

        text_path = Path(f"{result_base}.txt")
        if not text_path.exists():
            notify("OCR", "Kein Text erkannt")
            return

        text = text_path.read_text(encoding="utf-8", errors="ignore").strip()
        if not text:
            notify("OCR", "Kein Text erkannt")
            return

        set_clipboard(text)

        if SAVE_TEXT_FILE:
            TEXT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            out_path = TEXT_OUTPUT_DIR / "ocr_result.txt"
            out_path.write_text(text, encoding="utf-8")

        notify("OCR", "Text ins Clipboard kopiert")


if __name__ == "__main__":
    main()
