# Rainvow

A colorful terminal visualizer that reacts to your microphone input.

## Requirements
- Python 3
- [NumPy](https://numpy.org/)
- [sounddevice](https://python-sounddevice.readthedocs.io/)

Install the dependencies with:

```bash
pip install numpy sounddevice
```

## Usage
Run the script from your terminal:

```bash
python ondads.py
```

Optional flags let you tune the sensitivity and rainbow speed:

```bash
python ondads.py --sens 0.01 --speed 0.02
```

Press `Ctrl+C` to stop the visualization.

## Example
When audio is detected, the terminal displays a moving rainbow line:

```
----------------------------------------
```
