#!/usr/bin/env python3
"""
Name: Public IP Checker
Description: Ruft die aktuelle öffentliche IP-Adresse ab.
"""
import urllib.request
import subprocess

def notify(title, message):
    try:
        subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'], check=False)
    except:
        pass

def get_public_ip():
    try:
        with urllib.request.urlopen('https://api.ipify.org') as response:
            public_ip = response.read().decode('utf-8')
        return f"Deine öffentliche IP: {public_ip}"
    except Exception as e:
        return f"Fehler beim Abrufen der IP: {e}"

if __name__ == "__main__":
    ip = get_public_ip()
    notify("Netzwerk", ip)
    print(ip)
