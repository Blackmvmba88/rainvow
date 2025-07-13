import os
import time
import pyautogui
from colorama import Fore, Style

LOG_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(LOG_DIR, exist_ok=True)

def color(text, hue):
    return f"{hue}{text}{Style.RESET_ALL}"

def take_screenshot(tag="default"):
    filename = os.path.join(LOG_DIR, f"snap_{tag}_{int(time.time())}.png")
    pyautogui.screenshot(filename)
    print(color(f"[Hydra] Screenshot saved: {filename}", Fore.BLUE))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Capture a screenshot with colorful logging")
    parser.add_argument('--tag', default='default', help='Tag for the output filename')
    args = parser.parse_args()
    take_screenshot(args.tag)
