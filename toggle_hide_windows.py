import time
import argparse
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
    return millis / 1000.0 # returns time in seconds


def toggle_hide_windows():
    windll.user32.keybd_event(0x5B, 0, 0, 0) # Left Windows Key Down
    windll.user32.keybd_event(0x44, 0, 0, 0) # "D" Key Down
    time.sleep(0.05)
    windll.user32.keybd_event(0x5B, 0, 0x0002, 0) # Left Windows Key Up
    windll.user32.keybd_event(0x44, 0, 0x0002, 0) # "D" Key Up
    

def lock_screen():
    windll.user32.LockWorkStation()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Hide all windows after a certain period of inactivity. Then bring them back after mouse or keyboard interaction.')
    parser.add_argument("idle_time", help="Trigger after x minutes of being idle (defaults to an idle_time of 15 minutes).", nargs='?', default=15, type=float)
    parser.add_argument("-r", "--create_startup", help="Set script to run upon logon of the current user", action="store_true")
    parser.add_argument("-l", "--lockscreen", help="Lock screen after period of inactivity.", action="store_true")
    args = parser.parse_args()

    if args.idle_time < 0.1:
        parser.error("Minimum idle time is 0.1 minutes (10 seconds).")
    else:
        idle_minutes = args.idle_time * 60
    if args.lockscreen:
        print("[!] Screen will lock upon return from idle\n")
    print(f"[+] Idle time set to {idle_minutes/60} minutes")
        

    # If the user specified -r, then add the script to their startup folder and use idle_time when running it.
    if args.create_startup:
        appdata = os.getenv('APPDATA')
        lock_arg = ''
        
        # If user ALSO specified -l then add the argument when script is run on logon.
        if args.lockscreen:
            lock_arg = "-l"
        try:
            with open(f"{appdata}\Microsoft\Windows\Start Menu\Programs\Startup\hide_windows.bat", 'w') as f:
                f.write(f'@echo off\n\npythonw "{__file__}" {lock_arg} {args.idle_time}')
            print(f"[+] Set [{__file__}] to run on startup at:\n%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\hide_windows.bat\n\n")
        except Exception as e:
            input(str(e) + "\n\nPress any key to continue...")
            exit()
        
    while True:
        print("[*] Waiting for idle...\n")
        while True:
            time.sleep(0.1)
            if get_idle_duration() < float(idle_minutes):
                # We sleep until we have waited the requested duration and are deemed 'idle'
                continue
            elif get_idle_duration() > float(idle_minutes):
                break

        print(f"[*] Idle for >{idle_minutes/60} minutes - Hiding windows")
        toggle_hide_windows() # Hide windows to show background (also resets the idle duration back to 0)


        # Wait for the idle duration to increase back to 0.15
        time.sleep(0.15)
        while True:
            if get_idle_duration() < 0.05:
                break
        
        if args.lockscreen:
            toggle_hide_windows() # First show their windows to them
            time.sleep(0.05)
            lock_screen() # If the user specified -l, then lock the screen when they return from inactivity
        else:
            time.sleep(0.025)
            toggle_hide_windows() # Out of the loop & the user returned, so bring the windows back up.