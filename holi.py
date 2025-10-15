#!/usr/bin/env python3
"""
holi.py - Saludo colorido en el estilo Rainvow

Un simple script de saludo que muestra "Holi!" con colores del arcoíris.
"""

import time
from rich.console import Console
from rich.text import Text

console = Console()

# Colores del arcoíris (igual que en ondads.py)
RAINBOW_COLORS = [
    "red",
    "orange1",
    "yellow1",
    "green1",
    "cyan",
    "blue",
    "magenta",
]


def show_greeting():
    """Muestra un saludo colorido animado."""
    console.clear()
    
    # Crear el texto "HOLI!" con colores del arcoíris
    mensaje = "HOLI!"
    
    for i in range(len(RAINBOW_COLORS)):
        console.clear()
        text = Text()
        
        for j, letra in enumerate(mensaje):
            color_idx = (j + i) % len(RAINBOW_COLORS)
            text.append(letra, style=RAINBOW_COLORS[color_idx])
        
        console.print(text, justify="center", style="bold")
        console.print("\nGood Vibes! ✨🌈", justify="center", style="italic cyan")
        time.sleep(0.3)
    
    console.clear()
    # Mensaje final
    text = Text()
    for j, letra in enumerate(mensaje):
        text.append(letra, style=RAINBOW_COLORS[j % len(RAINBOW_COLORS)])
    
    console.print(text, justify="center", style="bold")
    console.print("\nGood Vibes! ✨🌈", justify="center", style="italic cyan")
    console.print("\nBienvenido a Rainvow Tools", justify="center", style="dim white")


if __name__ == "__main__":
    try:
        show_greeting()
    except KeyboardInterrupt:
        console.print("\n¡Hasta luego! 👋", style="bold yellow")
