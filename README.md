# Rainvow Tools

Este repositorio contiene utilidades de Python para efectos visuales.

## `ondads.py`
Visualiza un arcoíris animado en la terminal sincronizado con el audio
capturado por el micrófono.

## `keyboard_rgb.py`
Controla las luces de un teclado a través de
[OpenRGB](https://openrgb.org/). El script se conecta a un servidor
OpenRGB local o remoto y recorre los colores del arcoíris.

OpenRGB no tiene soporte nativo para macOS, por lo que puedes
ejecutarlo en otra máquina (Windows o Linux) o en una máquina virtual y
usar la opción `--host` para indicar su dirección.

### Requisitos
- Python 3
- `pip install openrgb-python`
- Un servidor OpenRGB ejecutándose con la opción `--server`.

### Uso
```bash
python keyboard_rgb.py --show --host 127.0.0.1
```
Interrumpe con `Ctrl+C` para apagar las luces.
