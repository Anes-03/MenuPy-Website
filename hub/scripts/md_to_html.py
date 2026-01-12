#!/usr/bin/env python3
"""
Name: Markdown zu HTML
Description: Konvertiert Markdown aus der Zwischenablage in HTML.
"""
import subprocess
import re

def notify(title, message):
    try:
        subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'], check=False)
    except:
        pass

def md_converter():
    try:
        md_text = subprocess.check_output(['pbpaste'], text=True).strip()
        if not md_text:
            return "Fehler: Zwischenablage ist leer."
        
        # Very simple conversion rules for basic MD
        html = md_text
        html = re.sub(r'^# (.*)', r'<h1>\1</h1>', html, flags=re.M)
        html = re.sub(r'^## (.*)', r'<h2>\1</h2>', html, flags=re.M)
        html = re.sub(r'\*\*(.*)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*)\*', r'<em>\1</em>', html)
        
        subprocess.run(['pbcopy'], input=html.encode('utf-8'), check=False)
        return "Konvertiert und in Zwischenablage kopiert."
    except Exception as e:
        return f"Fehler: {e}"

if __name__ == "__main__":
    res = md_converter()
    notify("MD to HTML", res)
    print(res)
