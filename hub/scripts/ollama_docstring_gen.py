#!/usr/bin/env python3
"""
Name: Docstring Generator (Ollama)
Description: Generiert Python Docstrings für Code im Clipboard.
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

def generate_docstring():
    if not shutil.which("ollama"):
        return "Fehler: Ollama nicht gefunden."
    
    code = get_clipboard().strip()
    if not code:
        return "Fehler: Kein Code gefunden."
    
    prompt = f"Generiere einen professionellen Google-Style Docstring für diesen Python Code:\n\n{code}"
    
    try:
        result = subprocess.run(['ollama', 'run', MODEL], input=prompt, capture_output=True, text=True, check=False)
        docstring = result.stdout.strip()
        
        if docstring:
            set_clipboard(docstring)
            return "Docstring generiert."
        return "Fehler."
    except Exception as e:
        return f"Fehler: {e}"

if __name__ == "__main__":
    res = generate_docstring()
    notify("Docstring Gen", res)
    print(res)
