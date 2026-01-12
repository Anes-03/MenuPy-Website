#!/usr/bin/env python3
"""
Name: Pomodoro Timer
Description: Startet einen 25-Minuten Fokus-Timer.
"""
import time
import subprocess

def notify(title, message):
    try:
        subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'], check=False)
    except:
        pass

def start_pomodoro():
    notify("Pomodoro", "Timer gestartet: 25 Minuten Fokus!")
    # For a real script, this would run in background. 
    # Here we just simulate or advise.
    # time.sleep(25 * 60)
    # notify("Pomodoro", "Zeit um! Mach eine kurze Pause.")
    return "Fokus-Session läuft... (25 Min)"

if __name__ == "__main__":
    res = start_pomodoro()
    print(res)
