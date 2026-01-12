#!/usr/bin/env python3
"""
Name: Speicherplatz prüfen
Description: Überprüft den freien Speicherplatz auf der Festplatte.
"""
import shutil
import subprocess

def notify(title, message):
    try:
        subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'], check=False)
    except:
        pass

def check_disk_usage():
    total, used, free = shutil.disk_usage("/")
    
    # Convert to GB
    free_gb = free // (2**30)
    percent_free = (free / total) * 100
    
    msg = f"Frei: {free_gb} GB ({percent_free:.1f}% verfügbar)"
    return msg

if __name__ == "__main__":
    result = check_disk_usage()
    notify("Festplatte", result)
    print(result)
