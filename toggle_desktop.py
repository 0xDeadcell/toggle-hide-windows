import subprocess
import time
from ctypes import windll, Structure, c_long, byref
# Using ctypes because I would rather not have the user install dependencies (besides python)



class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def check_for_scheduled_task(tn):
    subprocess.check_output(f"schtasks.exe /query /tn {tn}", shell=False, universal_newlines=True, stderr=subprocess.STDOUT)


def create_scheduled_task(tn):
    subprocess.call(f"schtasks.exe /create /tn {tn} /tr {__file__} /sc onidle /i 10", shell=False, universal_newlines=True, stderr=subprocess.STDOUT)


def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x, pt.y


def toggle_hide_windows():
    windll.user32.keybd_event(0x5B, 0, 0, 0) # Left Windows Key Down
    windll.user32.keybd_event(0x44, 0, 0, 0) # "D" Key Down
    windll.user32.keybd_event(0x44, 0, 0x0002, 0) # "D" Key Up
    windll.user32.keybd_event(0x5B, 0, 0x0002, 0) # Left Windows Key Up



if __name__ == "__main__":
    TASK_NAME = "toggle_desktop_on_idle"
    
    # Error handling to check if task was already created, if not then create it.
    try:
        check_for_scheduled_task(tn=TASK_NAME)
    except subprocess.CalledProcessError as e:
        print(f"Could not find scheduled task: {TASK_NAME}, creating new one...")
        create_scheduled_task(tn=TASK_NAME)
        exit()
        
    except Exception as oop:
        print(f"{oop}\n\nYou are likely missing schtasks.exe or the permission to schedule a task.")

    time.sleep(0.20)
    toggle_hide_windows() # Hide windows to show background.
    original_pos = queryMousePosition() # Grab mouse position to check if the user has returned later on.

    # Compare current mouse pos with mouse pos at start up.
    while queryMousePosition() == original_pos:
        time.sleep(0.1) # Don't completely hog the CPU (check 10x a second)
    
    toggle_hide_windows() # Out of the loop & the user returned, so bring the windows back up.