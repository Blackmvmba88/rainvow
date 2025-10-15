"""Visualizador de audio en tiempo real con barras de colores del arcoíris.

Este módulo captura audio del micrófono del sistema, analiza las frecuencias
usando FFT (Fast Fourier Transform), y las visualiza como barras de colores
del arcoíris en la terminal. Incluye sistema de ganancia adaptativa automática
para mantener visualización óptima independientemente del volumen de entrada.

Componentes principales:
    - get_band_amps(): Análisis de frecuencias modulares
    - audio_source(): Fuente de audio configurable con fallback
    - run_visualizer(): Loop principal de visualización

Uso:
    python3 ondads.py

El programa se ejecuta hasta recibir Ctrl+C.
"""

import numpy as np
import sounddevice as sd
from rich.console import Console
from rich.style import Style

console = Console()

# Colores base del arcoíris
RAINBOW_BASE = [
    "red",
    "orange1",
    "yellow1",
    "green1",
    "cyan",
    "blue",
    "magenta",
]

N_BANDS = len(RAINBOW_BASE)
BAR_HEIGHT = 12

FS = 44100
DURATION = 0.05  # segundos por bloque
BLOCKSIZE = int(FS * DURATION)

# Ganancias adaptativas por banda
gains = np.ones(N_BANDS)
MIN_GAIN = 0.5
MAX_GAIN = 10.0
ADAPT_SPEED = 0.1


def get_band_amps(audio_block: np.ndarray, fs: int, n_bands: int) -> np.ndarray:
    """Calcula la amplitud para cada banda de frecuencia del audio.
    
    Aplica FFT (Fast Fourier Transform) al bloque de audio y divide el espectro
    de frecuencias en bandas equiespaciadas, calculando la amplitud máxima
    de cada banda.
    
    Args:
        audio_block: Array de audio con shape (n_samples, n_channels)
        fs: Frecuencia de muestreo en Hz (sample rate)
        n_bands: Número de bandas de frecuencia a generar
        
    Returns:
        Array con las amplitudes logarítmicas de cada banda (log1p aplicado)
        
    Example:
        >>> audio = np.random.randn(2205, 1)
        >>> amps = get_band_amps(audio, 44100, 7)
        >>> len(amps)
        7
    """
    fft = np.fft.rfft(audio_block[:, 0] * np.hanning(len(audio_block)))
    mag = np.abs(fft)
    freqs = np.fft.rfftfreq(len(audio_block), 1 / fs)
    max_freq = fs // 2
    band_edges = np.linspace(0, max_freq, n_bands + 1)
    amps = []
    for i in range(n_bands):
        idx = np.where((freqs >= band_edges[i]) & (freqs < band_edges[i + 1]))[0]
        if len(idx) > 0:
            amps.append(mag[idx].max())
        else:
            amps.append(0)
    return np.log1p(amps)


shift = 0


def audio_source():
    """Generador que produce bloques de audio del micrófono o ruido de prueba.
    
    Intenta capturar audio del micrófono del sistema. Si falla (por falta de
    hardware, permisos, o errores), automáticamente usa ruido aleatorio como
    fuente alternativa para permitir pruebas sin hardware de audio.
    
    Yields:
        np.ndarray: Bloques de audio con shape (BLOCKSIZE, 1)
        
    Note:
        Esta función es un generador infinito. Debe interrumpirse con Ctrl+C
        o mediante una excepción externa.
        
    Example:
        >>> for block in audio_source():
        ...     # Procesar block de audio
        ...     break  # Terminar después del primer bloque
    """
    try:
        with sd.InputStream(channels=1, samplerate=FS, blocksize=BLOCKSIZE) as stream:
            console.print("Presiona Ctrl+C para detener", style="bold white")
            while True:
                yield stream.read(BLOCKSIZE)[0]
    except Exception as exc:
        console.print(
            f"No se pudo iniciar la entrada de audio ({exc}). Se usará ruido de prueba.",
            style="bold yellow",
        )
        while True:
            yield np.random.uniform(-1, 1, size=(BLOCKSIZE, 1))


def run_visualizer():
    """Ejecuta el visualizador de audio en tiempo real con barras de colores.
    
    Loop principal que captura audio, analiza frecuencias, aplica ganancia
    adaptativa y renderiza barras de colores del arcoíris que representan
    la amplitud de cada banda de frecuencia.
    
    El visualizador usa un sistema de ganancia adaptativa que ajusta
    automáticamente los niveles para evitar saturación y mantener la
    visualización óptima independientemente del volumen de entrada.
    
    Note:
        Ejecuta indefinidamente hasta recibir KeyboardInterrupt (Ctrl+C)
    """
    global shift
    for audio_block in audio_source():
        amps = get_band_amps(audio_block, FS, N_BANDS)
        for i in range(N_BANDS):
            target = 0.7
            if amps[i] * gains[i] > 0.95:
                gains[i] = max(gains[i] * (1 - ADAPT_SPEED), MIN_GAIN)
            elif amps[i] * gains[i] < target:
                gains[i] = min(gains[i] * (1 + ADAPT_SPEED), MAX_GAIN)
        amps = amps * gains
        if amps.max() > 0:
            amps = amps / amps.max()
        barra_str = ""
        for i, amp in enumerate(amps):
            barras = int(amp * BAR_HEIGHT)
            color_idx = (i + shift) % N_BANDS
            color = Style(color=RAINBOW_BASE[color_idx])
            barra_str += f"[{color}]" + "█" * barras + " " * (BAR_HEIGHT - barras) + "[/]"
        shift = (shift + 1) % N_BANDS
        console.print(barra_str, end="\r", highlight=False, soft_wrap=True)


if __name__ == "__main__":
    try:
        run_visualizer()
    except KeyboardInterrupt:
        console.print("\nDetenido por el usuario", style="bold white")
