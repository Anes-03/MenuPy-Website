#!/usr/bin/env python3
"""
Name: Battery Health
Description: Zeigt Batteriestatus, Ladezyklen und Temperatur an.
"""
import subprocess
import re

def notify(title, message):
    try:
        subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'], check=False)
    except:
        pass

def get_battery_info():
    try:
        cmd = ['pmset', '-g', 'batt']
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        output = result.stdout
        
        # Power source and percentage
        pct_match = re.search(r'(\d+)%', output)
        percent = pct_match.group(1) if pct_match else "N/A"
        
        # Cycles and Health via system_profiler
        cmd_prof = ['system_profiler', 'SPPowerDataType']
        res_prof = subprocess.run(cmd_prof, capture_output=True, text=True, check=False)
        prof_out = res_prof.stdout
        
        cycles = re.search(r'Cycle Count: (\d+)', prof_out)
        condition = re.search(r'Condition: (.*)', prof_out)
        
        c_count = cycles.group(1) if cycles else "N/A"
        cond = condition.group(1).strip() if condition else "N/A"
        
        return f"Ladestand: {percent}% | Zyklen: {c_count} | Zustand: {cond}"
    except Exception as e:
        return f"Fehler: {e}"

if __name__ == "__main__":
    info = get_battery_info()
    notify("Batterie Info", info)
    print(info)
