#!/usr/bin/env python3
"""
Name: Emoji Enhancer (Ollama)
Description: Fügt passende Emojis in den Clipboard-Text ein.
"""
import subprocess
import shutil

MODEL = "llama3.1"

def notify(title, message):
    try:
        subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'], check=False)
    except:
        pass

def get_clipboard():
    return subprocess.check_output(['pbpaste'], text=True)

def set_clipboard(text):
    process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    process.communicate(text.encode('utf-8'))

def emojify():
    if not shutil.which("ollama"):
        return "Fehler: Ollama nicht gefunden."
    
    text = get_clipboard().strip()
    if not text:
        return "Fehler: Zwischenablage leer."
    
    prompt = f"Füge passende Emojis in diesen Text ein, um ihn lebendiger zu machen. Behalte den Originaltext bei:\n\n{text}"
    
    try:
        result = subprocess.run(['ollama', 'run', MODEL], input=prompt, capture_output=True, text=True, check=False)
        new_text = result.stdout.strip()
        
        if new_text:
            set_clipboard(new_text)
            return "Emojis hinzugefügt."
        return "Keine Änderung vorgenommen."
    except Exception as e:
        return f"Fehler: {e}"

if __name__ == "__main__":
    res = emojify()
    notify("Emojify", res)
    print(res)
