#!/usr/bin/env python3
"""
Name: Passwort Generator
Description: Erzeugt ein sicheres Passwort und kopiert es in die Zwischenablage.
"""
import secrets
import string
import subprocess

def notify(title, message):
    try:
        subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'], check=False)
    except:
        pass

def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    
    # Copy to clipboard
    subprocess.run(['pbcopy'], input=password.encode('utf-8'), check=False)
    return "Sicheres Passwort generiert und kopiert."

if __name__ == "__main__":
    msg = generate_password()
    notify("Passwort", msg)
    print(msg)
