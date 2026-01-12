#!/usr/bin/env python3
"""
Name: Code Reviewer (Ollama)
Description: Analysiert Code in der Zwischenablage auf Fehler und Verbesserungen.
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

def review_code():
    if not shutil.which("ollama"):
        return "Fehler: Ollama ist nicht installiert."
    
    code = get_clipboard().strip()
    if not code:
        return "Fehler: Keine Daten in der Zwischenablage."
    
    prompt = f"Reviewe diesen Code auf Fehler, Best Practices und Sicherheit. Gib konstruktive Vorschläge:\n\n{code}"
    
    try:
        result = subprocess.run(['ollama', 'run', MODEL], input=prompt, capture_output=True, text=True, check=False)
        review = result.stdout.strip()
        
        if review:
            set_clipboard(review)
            return "Review abgeschlossen und in Zwischenablage kopiert."
        return "Keine Antwort vom Modell erhalten."
    except Exception as e:
        return f"Fehler: {e}"

if __name__ == "__main__":
    status = review_code()
    notify("Ollama Reviewer", status)
    print(status)
