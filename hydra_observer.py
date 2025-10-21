import json
import os
import time
import datetime
import threading
import subprocess
import psutil
from pynput import keyboard, mouse
import numpy as np
import sounddevice as sd
try:
    import pygetwindow as gw
except (ImportError, ModuleNotFoundError):
    gw = None

try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init()
    COLOR_ENABLED = True
except (ImportError, ModuleNotFoundError):
    COLOR_ENABLED = False

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(LOG_DIR, f"session_{session_id}.json")
logs = []
log_lock = threading.Lock()

HYDRA_CLI = os.environ.get("HYDRA_CLI", "hydra")
USER_CONSENT = False  # Will be set at runtime after user confirmation
SLEEP_DURATION = 2  # Seconds between system checks


def color(text, c):
    if not COLOR_ENABLED:
        return text
    return f"{c}{text}{Style.RESET_ALL}"


def log_event(event_type, info):
    entry = {
        "time": time.time(),
        "event": event_type,
        "info": info,
    }
    with log_lock:
        logs.append(entry)


def display_metrics(cpu, mem):
    bar_len = 20
    cpu_bar = "█" * int(cpu / 100 * bar_len)
    mem_bar = "█" * int(mem / 100 * bar_len)
    print(color(f"CPU [{cpu:5.1f}%] {cpu_bar:<20} MEM [{mem:5.1f}%] {mem_bar:<20}", Fore.BLUE))


def record_audio(duration=5, samplerate=44100):
    print(color("[Hydra] Capturing audio loop...", Fore.MAGENTA))
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2)
    sd.wait()
    path = os.path.join(LOG_DIR, f"audio_{int(time.time())}.npy")
    np.save(path, audio)
    print(color(f"[Hydra] Audio saved to {path}", Fore.YELLOW))
    log_event("audio", {"file": path})


def active_window_title():
    if gw is None:
        return None
    try:
        win = gw.getActiveWindow()
        if win:
            return win.title
    except (AttributeError, OSError):
        pass
    return None


def on_key_press(key):
    if not USER_CONSENT:
        return
    window_title = active_window_title()
    if window_title and ("password" in window_title.lower() or "login" in window_title.lower()):
        return
    try:
        k = key.char
    except AttributeError:
        k = str(key)
    log_event("key", k)


def on_click(x, y, button, pressed):
    if pressed:
        log_event("click", {"button": str(button), "pos": [x, y]})


shutdown_flag = False

def monitor_system():
    global shutdown_flag
    while not shutdown_flag:
        window = active_window_title()
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        log_event("system", {"window": window, "cpu": cpu, "mem": mem})
        display_metrics(cpu, mem)
        if window and "zip" in window.lower():
            print(color("[Hydra] Detected ZIP context - launching HUD...", Fore.CYAN))
            send_to_hydra("zip_hud")
        elif window and "music" in window.lower():
            print(color("[Hydra] Detected music context - listening for loops...", Fore.MAGENTA))
            send_to_hydra("music_mode")
            record_audio(5)
        time.sleep(SLEEP_DURATION)


def send_to_hydra(message):
    try:
        subprocess.Popen([HYDRA_CLI, message])
        log_event("hydra", message)
    except FileNotFoundError:
        print(color("Hydra CLI not found", Fore.RED))


if __name__ == "__main__":
    print(color("Hydra Observer starting...", Fore.GREEN))
    print(color("⚠️  This tool monitors keyboard and mouse activity.", Fore.YELLOW))
    print(color("Sensitive windows (password/login) are automatically excluded.", Fore.YELLOW))
    
    consent = input(color("Do you consent to keyboard/mouse monitoring? (y/N): ", Fore.CYAN))
    if consent.lower() == 'y':
        USER_CONSENT = True
        print(color("✓ User consent granted. Starting monitoring...", Fore.GREEN))
    else:
        USER_CONSENT = False
        print(color("⚠️  Monitoring disabled. Only system metrics will be logged.", Fore.YELLOW))
    
    key_listener = keyboard.Listener(on_press=on_key_press)
    mouse_listener = mouse.Listener(on_click=on_click)
    key_listener.start()
    mouse_listener.start()

    try:
        monitor_system()
    except KeyboardInterrupt:
        pass
    finally:
        key_listener.stop()
        mouse_listener.stop()
        with open(log_file, "w") as f:
            json.dump(logs, f, indent=2)
        print(color(f"Logs saved to {log_file}", Fore.YELLOW))

