#!/usr/bin/env python3
"""
Name: WiFi Info
Description: Zeigt das aktuelle WiFi-Netzwerk (SSID) und die Signalstärke (RSSI) an.
"""
import subprocess
import re

def notify(title, message):
    try:
        subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'], check=False)
    except:
        pass

def get_wifi_info():
    try:
        # macOS specific command for airport utility
        cmd = ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I']
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        output = result.stdout
        
        ssid = re.search(r' SSID: (.*)', output)
        rssi = re.search(r' agrCtlRSSI: (.*)', output)
        
        if ssid:
            name = ssid.group(1).strip()
            signal = rssi.group(1).strip() if rssi else "N/A"
            return f"Verbunden mit: {name} (Signal: {signal} dBm)"
        return "Nicht mit einem WiFi-Netzwerk verbunden."
    except Exception as e:
        return f"Fehler beim Abrufen der WiFi-Info: {e}"

if __name__ == "__main__":
    info = get_wifi_info()
    notify("WiFi Status", info)
    print(info)
