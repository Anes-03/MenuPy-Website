#!/usr/bin/env python3
"""
Name: Git Commit Generator (Ollama)
Description: Generiert eine Commit-Message aus einem git diff im Clipboard.
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

def generate_commit():
    if not shutil.which("ollama"):
        return "Fehler: Ollama nicht gefunden."
    
    diff = get_clipboard().strip()
    if not diff:
        return "Fehler: Kein Git Diff in der Zwischenablage."
    
    prompt = f"Erzeuge eine professionelle, kurze Git Commit Message (Conventional Commits) basierend auf diesem Diff:\n\n{diff}"
    
    try:
        result = subprocess.run(['ollama', 'run', MODEL], input=prompt, capture_output=True, text=True, check=False)
        msg = result.stdout.strip()
        
        if msg:
            set_clipboard(msg)
            return "Commit Message generiert und kopiert."
        return "Keine Antwort erhalten."
    except Exception as e:
        return f"Fehler: {e}"

if __name__ == "__main__":
    res = generate_commit()
    notify("Git Commit", res)
    print(res)
