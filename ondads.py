import numpy as np
import sounddevice as sd
import sys
import time
import colorsys

fs = 44100
frame_length = 1024
hop_length = frame_length // 4
audio_buffer = np.zeros(fs)

max_line_length = 200  # Doble de largo
min_line_length = 40   # También el doble

def audio_callback(indata, frames, time, status):
    global audio_buffer
    audio_buffer = np.roll(audio_buffer, -len(indata[:, 0]))
    audio_buffer[-len(indata[:, 0]):] = indata[:, 0]

def rainbow_line(length, t):
    line = ""
    for i in range(length):
        hue = ((i / length) + t) % 1.0
        r, g, b = [int(255*x) for x in colorsys.hsv_to_rgb(hue, 1, 1)]
        line += f"\033[38;2;{r};{g};{b}m─"
    line += "\033[0m"
    return line

stream = sd.InputStream(channels=1, samplerate=fs, callback=audio_callback, blocksize=hop_length)
stream.start()

try:
    t = 0.0
    while True:
        frame = audio_buffer[-frame_length:]
        rms = np.sqrt(np.mean(frame**2))
        # Más sensible: divisor más pequeño (ajusta si quieres aún más sensibilidad)
        norm_rms = min(rms / 0.02, 1.0)
        line_length = int(min_line_length + (max_line_length - min_line_length) * norm_rms)
        pad = (max_line_length - line_length) // 2
        line = " " * pad + rainbow_line(line_length, t) + " " * (max_line_length - line_length - pad)
        sys.stdout.write("\r" + line)
        sys.stdout.flush()
        t = (t + 0.01) % 1.0
        time.sleep(hop_length / fs)
except KeyboardInterrupt:
    pass
finally:
    stream.stop()
    stream.close()
    print("\nListo.")