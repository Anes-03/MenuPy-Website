#!/usr/bin/env python3
"""
Name: URL Shortener
Description: Verkürzt eine URL aus der Zwischenablage via TinyURL API.
"""
import subprocess
import urllib.request
import urllib.parse

def notify(title, message):
    try:
        subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'], check=False)
    except:
        pass

def shorten_url():
    try:
        url = subprocess.check_output(['pbpaste'], text=True).strip()
        if not url.startswith('http'):
            return "Fehler: Ungültige URL in der Zwischenablage."
        
        api_url = "http://tinyurl.com/api-create.php?url=" + urllib.parse.quote(url)
        with urllib.request.urlopen(api_url) as response:
            short_url = response.read().decode('utf-8')
            
        subprocess.run(['pbcopy'], input=short_url.encode('utf-8'), check=False)
        return f"Verkürzt: {short_url} (in Zwischenablage)"
    except Exception as e:
        return f"Fehler: {e}"

if __name__ == "__main__":
    res = shorten_url()
    notify("URL Shortener", res)
    print(res)
