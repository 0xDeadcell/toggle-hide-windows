import time
import os
from ctypes import windll, Structure, c_uint, sizeof, byref
# Using ctypes because I would rather not have the user install dependencies (besides python of course)


class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]


def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0


def toggle_hide_windows():
    windll.user32.keybd_event(0x5B, 0, 0, 0) # Left Windows Key Down
    windll.user32.keybd_event(0x44, 0, 0, 0) # "D" Key Down
    time.sleep(0.05)
    windll.user32.keybd_event(0x5B, 0, 0x0002, 0) # Left Windows Key Up
    windll.user32.keybd_event(0x44, 0, 0x0002, 0) # "D" Key Up


if __name__ == "__main__":
    IDLE_MINUTES = 15 # (15 minutes)
    # Create the start up file
    appdata = os.getenv('APPDATA')
    
    # If the startup file doesn't exist, then create it
    if not os.path.exists(f"{appdata}\Microsoft\Windows\Start Menu\Programs\Startup\hide_windows.bat"):
        try:
            with open(f"{appdata}\Microsoft\Windows\Start Menu\Programs\Startup\hide_windows.bat", 'w') as f:
                f.write(f'@echo off\n\npythonw "{__file__}"')
            print(f"[+] Set [{__file__}] to run on startup at:\n{appdata}\Microsoft\Windows\Start Menu\Programs\Startup\hide_windows.bat\n\n")
        except Exception as e:
            input(str(e) + "\n\nPress any key to continue...")
            exit()
        
    while True:
        print("[*] Waiting for idle...\n")
        while True:
            time.sleep(0.1)
            if get_idle_duration() < float(IDLE_MINUTES):
                # We sleep until we have waited the requested duration and are deemed 'idle'
                continue
            elif get_idle_duration() > float(IDLE_MINUTES):
                break

        print("[*] IDLE - Hiding windows")
        toggle_hide_windows() # Hide windows to show background (also resets the idle duration back to 0)

        # Wait for the idle duration to increase back to 0.15
        time.sleep(0.15)
        while True:
            if get_idle_duration() < 0.05:
                break
        
        time.sleep(0.15)
        toggle_hide_windows() # Out of the loop & the user returned, so bring the windows back up.
