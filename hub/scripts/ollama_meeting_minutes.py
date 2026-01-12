#!/usr/bin/env python3
"""
Name: Meeting Minutes (Ollama)
Description: Erstellt strukturierte Protokolle aus Notizen im Clipboard.
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

def generate_minutes():
    if not shutil.which("ollama"):
        return "Fehler: Ollama nicht gefunden."
    
    notes = get_clipboard().strip()
    if not notes:
        return "Fehler: Keine Notizen gefunden."
    
    prompt = f"Erstelle ein strukturiertes Meeting-Protokoll aus diesen Notizen (Zusammenfassung, Entscheidungen, Action Items):\n\n{notes}"
    
    try:
        result = subprocess.run(['ollama', 'run', MODEL], input=prompt, capture_output=True, text=True, check=False)
        minutes = result.stdout.strip()
        
        if minutes:
            set_clipboard(minutes)
            return "Protokoll generiert."
        return "Fehler beim Generieren."
    except Exception as e:
        return f"Fehler: {e}"

if __name__ == "__main__":
    res = generate_minutes()
    notify("Meeting Minutes", res)
    print(res)
