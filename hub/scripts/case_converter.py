#!/usr/bin/env python3
"""
Name: Text Case Converter
Description: Ändert Groß-/Kleinschreibung des Textes in der Zwischenablage.
"""
import subprocess

def get_clipboard():
    return subprocess.check_output(['pbpaste'], text=True)

def set_clipboard(text):
    process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    process.communicate(text.encode('utf-8'))

def cycle_case():
    text = get_clipboard().strip()
    if not text:
        return "Zwischenablage leer."
    
    if text.isupper():
        new_text = text.lower()
    elif text.islower():
        new_text = text.title()
    else:
        new_text = text.upper()
        
    set_clipboard(new_text)
    return f"Geändert zu: {new_text[:20]}..."

if __name__ == "__main__":
    res = cycle_case()
    print(res)
