# Rainvow Tools

Este repositorio contiene utilidades de Python para efectos visuales.

## `ondads.py`
Visualiza un arcoíris animado en la terminal sincronizado con el audio
capturado por el micrófono.

## `keyboard_rgb.py`
Activa la iluminación RGB de un teclado compatible mediante
[OpenRGB](https://openrgb.org/). El script detecta un teclado HID en
Windows usando `pywinusb` y cambia su color en un ciclo de arcoíris.

### Requisitos
- Python 3
- `pip install openrgb-python pywinusb`
- Ejecutar OpenRGB con `--server` antes de lanzar el script.

### Uso
```bash
python keyboard_rgb.py
```
Interrumpe con `Ctrl+C` para apagar las luces.
