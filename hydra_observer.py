"""Sistema de monitoreo del sistema con detección de contexto inteligente.

Este módulo monitorea continuamente el uso de recursos del sistema (CPU, memoria),
registra eventos de teclado y mouse, y detecta contextos relevantes basados en
la ventana activa (ZIP, música, etc.) para activar acciones automáticas.

Características:
    - Monitoreo de CPU y memoria en tiempo real
    - Registro de eventos de teclado y mouse (respetando privacidad)
    - Detección de ventana activa
    - Contextos inteligentes que activan acciones (grabación de audio, HUD)
    - Logs JSON estructurados por sesión

Uso:
    python3 hydra_observer.py

Variables de entorno:
    HYDRA_CLI: Path al CLI de Hydra para enviar comandos (opcional)

El programa se ejecuta hasta recibir Ctrl+C. Todos los eventos se guardan
en logs/session_{timestamp}.json
"""

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
USER_CONSENT = False  # Se establecerá en tiempo de ejecución después de la confirmación del usuario
SLEEP_DURATION = 2  # Segundos entre comprobaciones del sistema


def color(text, c):
    """Aplica color al texto usando colorama si está disponible.

    Args:
        text: Texto a colorear
        c: Color de colorama (Fore.RED, Fore.BLUE, etc.)

    Returns:
        str: Texto con códigos de color ANSI o texto sin modificar
    """
    if not COLOR_ENABLED:
        return text
    return f"{c}{text}{Style.RESET_ALL}"


def log_event(event_type, info):
    """Registra un evento en el log de la sesión de forma thread-safe.

    Args:
        event_type: Tipo de evento ('key', 'click', 'system', 'audio', 'hydra')
        info: Información adicional del evento (dict, str, o cualquier JSON serializable)
    """
    entry = {
        "time": time.time(),
        "event": event_type,
        "info": info,
    }
    with log_lock:
        logs.append(entry)


def display_metrics(cpu, mem):
    """Muestra métricas del sistema con barras visuales en la terminal.

    Args:
        cpu: Porcentaje de uso de CPU (0-100)
        mem: Porcentaje de uso de memoria (0-100)
    """
    bar_len = 20
    cpu_bar = "█" * int(cpu / 100 * bar_len)
    mem_bar = "█" * int(mem / 100 * bar_len)
    print(color(f"CPU [{cpu:5.1f}%] {cpu_bar:<20} MEM [{mem:5.1f}%] {mem_bar:<20}", Fore.BLUE))


def record_audio(duration=5, samplerate=44100):
    """Graba un clip de audio y lo guarda en el directorio de logs.

    Útil para capturar loops musicales cuando se detecta contexto de música.

    Args:
        duration: Duración de la grabación en segundos (default: 5)
        samplerate: Frecuencia de muestreo en Hz (default: 44100)

    Note:
        Guarda el archivo como numpy array (.npy) para facilitar procesamiento
    """
    print(color("[Hydra] Capturing audio loop...", Fore.MAGENTA))
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2)
    sd.wait()
    path = os.path.join(LOG_DIR, f"audio_{int(time.time())}.npy")
    np.save(path, audio)
    print(color(f"[Hydra] Audio saved to {path}", Fore.YELLOW))
    log_event("audio", {"file": path})


def active_window_title():
    """Obtiene el título de la ventana activa del sistema.

    Returns:
        str or None: Título de la ventana activa, o None si no se puede obtener

    Note:
        Requiere pygetwindow instalado. Retorna None si no está disponible
        o si ocurre un error al consultar ventanas del sistema.
    """
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
    """Monitorea el sistema continuamente y detecta contextos relevantes.

    Ejecuta un loop que:
    - Revisa uso de CPU y memoria cada SLEEP_DURATION segundos
    - Detecta la ventana activa
    - Identifica contextos especiales (ZIP, music) en títulos de ventanas
    - Activa acciones automáticas según el contexto detectado

    El monitoreo continúa hasta que shutdown_flag se establece a True
    o se recibe KeyboardInterrupt.
    """
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
    """Envía un mensaje al CLI de Hydra si está configurado.

    Args:
        message: Comando o mensaje a enviar a Hydra CLI

    Note:
        El path del CLI se configura con la variable de entorno HYDRA_CLI.
        Si el CLI no se encuentra, se imprime un error pero no se interrumpe la ejecución.
    """
    try:
        subprocess.Popen([HYDRA_CLI, message])
        log_event("hydra", message)
    except FileNotFoundError:
        print(color("Hydra CLI not found", Fore.RED))


if __name__ == "__main__":
    print(color("Hydra Observer iniciando...", Fore.GREEN))
    print(color("⚠️  Esta herramienta monitorea la actividad del teclado y el ratón.", Fore.YELLOW))
    print(color("Las ventanas sensibles (contraseñas/inicio de sesión) se excluyen automáticamente.", Fore.YELLOW))

    consent = input(color("¿Consientes el monitoreo del teclado/ratón? (s/N): ", Fore.CYAN))
    if consent.lower() == 's':
        USER_CONSENT = True
        print(color("✓ Consentimiento del usuario otorgado. Iniciando monitoreo...", Fore.GREEN))
    else:
        USER_CONSENT = False
        print(color("⚠️  Monitoreo deshabilitado. Solo se registrarán métricas del sistema.", Fore.YELLOW))

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
