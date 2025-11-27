"""Utilidad para capturar capturas de pantalla con logging colorido.

Herramienta simple para tomar screenshots del escritorio completo con
un sistema de tags para organización y mensajes coloridos en terminal.

Requisitos:
    pip install pyautogui colorama

Uso:
    python3 screenshot.py --tag prueba

Las capturas se guardan en el directorio screenshots/
"""

import os
import time
import pyautogui
from colorama import Fore, Style

LOG_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(LOG_DIR, exist_ok=True)

def color(text, hue):
    """Aplica color ANSI al texto.
    
    Args:
        text: Texto a colorear
        hue: Color de colorama (Fore.RED, Fore.BLUE, etc.)
        
    Returns:
        str: Texto con códigos de escape ANSI para color
    """
    return f"{hue}{text}{Style.RESET_ALL}"

def take_screenshot(tag="default"):
    """Captura una captura de pantalla y la guarda con un tag descriptivo.
    
    Args:
        tag: Etiqueta para identificar la captura (default: "default")
        
    Note:
        Las capturas se guardan en el directorio screenshots/ con formato:
        snap_{tag}_{timestamp}.png
        
    Example:
        >>> take_screenshot("test_interface")
        [Hydra] Screenshot saved: screenshots/snap_test_interface_1234567890.png
    """
    filename = os.path.join(LOG_DIR, f"snap_{tag}_{int(time.time())}.png")
    pyautogui.screenshot(filename)
    print(color(f"[Hydra] Screenshot saved: {filename}", Fore.BLUE))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Capture a screenshot with colorful logging")
    parser.add_argument('--tag', default='default', help='Tag for the output filename')
    args = parser.parse_args()
    take_screenshot(args.tag)
