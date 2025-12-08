"""Control de iluminación RGB del teclado con OpenRGB.

Se conecta a un servidor OpenRGB (local o remoto) y cambia los colores
de un teclado en un ciclo de arcoíris. Puede mostrarse una pequeña
representación del color actual en la terminal.

Requisitos:
    - Python 3
    - pip install openrgb-python
    - Un servidor OpenRGB ejecutándose con la opción --server

Uso:
    python keyboard_rgb.py --show --host 127.0.0.1

El programa se ejecuta hasta recibir Ctrl+C, momento en el cual
apaga las luces del teclado.
"""

import argparse
import colorsys
import time

from openrgb import OpenRGBClient
from openrgb.utils import RGBColor


def rainbow_cycle(device, steps=360, delay=0.05, show=False):
    """Recorre los colores del arcoíris en el dispositivo RGB.

    Convierte valores HSV a RGB para crear una transición suave de colores
    a través del espectro del arcoíris completo.

    Args:
        device: Dispositivo OpenRGB a controlar
        steps: Número de pasos en el ciclo de colores (default: 360 para 1 grado por paso)
        delay: Pausa en segundos entre cambios de color (default: 0.05)
        show: Si True, muestra el color actual en la terminal (default: False)

    Example:
        >>> client = OpenRGBClient()
        >>> keyboard = client.devices[0]
        >>> rainbow_cycle(keyboard, steps=180, delay=0.1, show=True)
    """
    for i in range(steps):
        hue = i / float(steps)
        r, g, b = [int(255 * x) for x in colorsys.hsv_to_rgb(hue, 1, 1)]
        device.set_color(RGBColor(r, g, b))
        if show:
            print(f"\r\033[38;2;{r};{g};{b}m█\033[0m", end='', flush=True)
        time.sleep(delay)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Control de luces RGB del teclado via OpenRGB"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Direcci\u00f3n del servidor OpenRGB",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=6742,
        help="Puerto del servidor OpenRGB",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Mostrar el color aplicado en la terminal",
    )
    args = parser.parse_args()

    client = OpenRGBClient(host=args.host, port=args.port)
    keyboards = [d for d in client.devices if d.device_type.name == "KEYBOARD"]
    if not keyboards:
        print("No hay teclados compatibles en OpenRGB.")
        return

    keyboard = keyboards[0]
    print(
        f"Controlando {keyboard.name} a trav\u00e9s de OpenRGB en {args.host}:{args.port}"
    )

    try:
        while True:
            rainbow_cycle(keyboard, show=args.show)
    except KeyboardInterrupt:
        try:
            keyboard.set_color(RGBColor(0, 0, 0))
        except Exception as e:
            print(f"\nError al apagar el teclado: {e}")
        print("\nTerminando")


if __name__ == "__main__":
    main()
