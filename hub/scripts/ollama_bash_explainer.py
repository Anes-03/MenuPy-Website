#!/usr/bin/env python3
"""
Name: Bash Explainer (Ollama)
Description: Erklärt komplexe Terminal-Befehle aus dem Clipboard.
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

def explain_bash():
    if not shutil.which("ollama"):
        return "Fehler: Ollama nicht gefunden."
    
    cmd = get_clipboard().strip()
    if not cmd:
        return "Fehler: Kein Befehl gefunden."
    
    prompt = f"Erkläre kurz und verständlich, was dieser Bash-Befehl macht:\n\n{cmd}"
    
    try:
        result = subprocess.run(['ollama', 'run', MODEL], input=prompt, capture_output=True, text=True, check=False)
        explanation = result.stdout.strip()
        
        if explanation:
            set_clipboard(explanation)
            return "Erklärung kopiert."
        return "Fehler."
    except Exception as e:
        return f"Fehler: {e}"

if __name__ == "__main__":
    res = explain_bash()
    notify("Bash Explainer", res)
    print(res)
