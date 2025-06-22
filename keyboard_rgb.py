"""Keyboard RGB control using OpenRGB.

Este script detecta un teclado HID en Windows y controla sus
luces RGB a través de OpenRGB. Asegúrate de tener OpenRGB
corriendo con la opción --server y de haber instalado las
librerías openrgb-python y pywinusb.
"""

import time
import colorsys

from openrgb import OpenRGBClient
from openrgb.utils import RGBColor
import pywinusb.hid as hid


def find_keyboard():
    """Devuelve (vendor_id, product_id) del primer teclado HID."""
    for device in hid.HidDeviceFilter().get_devices():
        try:
            caps = device.hid_caps
            if caps.usage_page == 0x01 and caps.usage == 0x06:
                return device.vendor_id, device.product_id
        except AttributeError:
            continue
    return None, None


def rainbow_cycle(device, steps=360, delay=0.05):
    for i in range(steps):
        hue = i / float(steps)
        r, g, b = [int(255 * x) for x in colorsys.hsv_to_rgb(hue, 1, 1)]
        device.set_color(RGBColor(r, g, b))
        time.sleep(delay)


def main():
    vid, pid = find_keyboard()
    if vid is None:
        print("No se encontró un teclado HID.")
    else:
        print(f"Teclado detectado: VID={vid:04X}, PID={pid:04X}")

    client = OpenRGBClient()
    keyboards = [d for d in client.devices if d.device_type.name == "KEYBOARD"]
    if not keyboards:
        print("No hay teclados compatibles en OpenRGB.")
        return

    keyboard = keyboards[0]
    print(f"Controlando {keyboard.name} con OpenRGB")

    try:
        while True:
            rainbow_cycle(keyboard)
    except KeyboardInterrupt:
        keyboard.set_color(RGBColor(0, 0, 0))
        print("\nTerminando")


if __name__ == "__main__":
    main()
