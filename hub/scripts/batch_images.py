#!/usr/bin/env python3
"""
Name: Bild-Batch Konvertierung
Description: Konvertiert Bilder stapelweise in ein Ziel-Format.
Requirements: sips (macOS), optional cwebp fuer WebP-Ausgabe
"""
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import tempfile

# --- Konfiguration ---
INPUT_DIR = Path.home() / "Pictures" / "ToConvert"
OUTPUT_DIR = Path.home() / "Pictures" / "Converted"
OUTPUT_FORMAT = "webp"  # webp, jpeg, png, tiff
QUALITY = 80
RESIZE_MAX = None  # z.B. 1600, oder None

ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".tiff"}


def notify(title: str, message: str) -> None:
    try:
        subprocess.run(
            ["osascript", "-e", f'display notification "{message}" with title "{title}"'],
            check=False,
        )
    except Exception:
        pass


def convert_with_sips(source: Path, dest: Path, fmt: str) -> bool:
    cmd = ["sips", "-s", "format", fmt]
    if fmt == "jpeg":
        cmd += ["-s", "formatOptions", str(QUALITY)]
    if RESIZE_MAX:
        cmd += ["-Z", str(RESIZE_MAX)]
    cmd += [str(source), "--out", str(dest)]

    result = subprocess.run(cmd, check=False, capture_output=True)
    return result.returncode == 0 and dest.exists()


def convert_with_cwebp(source: Path, dest: Path) -> bool:
    cmd = ["cwebp", str(source), "-q", str(QUALITY), "-o", str(dest)]
    result = subprocess.run(cmd, check=False, capture_output=True)
    return result.returncode == 0 and dest.exists()


def main() -> None:
    if not INPUT_DIR.exists():
        notify("Bild-Batch", "Eingabeordner fehlt")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    target_format = OUTPUT_FORMAT.lower()
    use_cwebp = target_format == "webp" and shutil.which("cwebp")
    if target_format == "webp" and not use_cwebp:
        target_format = "jpeg"
        notify("Bild-Batch", "cwebp fehlt, nutze JPEG als Fallback")

    converted = 0
    failed = 0

    for image in INPUT_DIR.iterdir():
        if image.suffix.lower() not in ALLOWED_EXTS:
            continue
        if not image.is_file():
            continue

        out_name = image.stem + f".{target_format}"
        out_path = OUTPUT_DIR / out_name

        try:
            if use_cwebp:
                if RESIZE_MAX:
                    with tempfile.TemporaryDirectory() as tmp:
                        temp_path = Path(tmp) / "temp.png"
                        ok = convert_with_sips(image, temp_path, "png")
                        if not ok:
                            raise RuntimeError("Resize fehlgeschlagen")
                        ok = convert_with_cwebp(temp_path, out_path)
                else:
                    ok = convert_with_cwebp(image, out_path)
            else:
                ok = convert_with_sips(image, out_path, target_format)

            if ok:
                converted += 1
            else:
                failed += 1
        except Exception:
            failed += 1

    notify("Bild-Batch", f"Fertig: {converted}, Fehler: {failed}")


if __name__ == "__main__":
    main()
