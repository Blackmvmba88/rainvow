"""Control de iluminación RGB del teclado con OpenRGB.

Se conecta a un servidor OpenRGB (local o remoto) y cambia los colores
de un teclado en un ciclo de arcoíris. Puede mostrarse una pequeña
representación del color actual en la terminal.
"""

import argparse
import colorsys
import time

from openrgb import OpenRGBClient
from openrgb.utils import RGBColor


def rainbow_cycle(device, steps=360, delay=0.05, show=False):
    """Recorre los colores del arcoíris en el dispositivo."""
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
        keyboard.set_color(RGBColor(0, 0, 0))
        print("\nTerminando")


if __name__ == "__main__":
    main()
