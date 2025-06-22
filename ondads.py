#!/usr/bin/env python3
"""Terminal-based rainbow audio visualizer."""

import argparse
import colorsys
import numpy as np
import sounddevice as sd
import shutil
import sys
import time

# Audio settings
FS = 44100
FRAME_LENGTH = 1024
HOP_LENGTH = FRAME_LENGTH // 4

# Ring buffer for recent audio
audio_buffer = np.zeros(FS)


def audio_callback(indata, frames, time_info, status):
    """Store microphone data in the global buffer."""
    global audio_buffer
    audio_buffer = np.roll(audio_buffer, -frames)
    audio_buffer[-frames:] = indata[:, 0]


def rainbow_line(length: int, offset: float) -> str:
    """Return a string with a rainbow gradient of the given length."""
    line = ""
    for i in range(length):
        hue = ((i / length) + offset) % 1.0
        r, g, b = [int(255 * x) for x in colorsys.hsv_to_rgb(hue, 1, 1)]
        line += f"\033[38;2;{r};{g};{b}m─"
    return line + "\033[0m"


def main() -> None:
    parser = argparse.ArgumentParser(description="Colorful terminal audio visualizer")
    parser.add_argument(
        "--sens",
        type=float,
        default=0.02,
        help="amplitude normalization; lower is more sensitive",
    )
    parser.add_argument(
        "--speed", type=float, default=0.01, help="rainbow scroll speed"
    )
    args = parser.parse_args()

    # Determine terminal dimensions
    term_width = shutil.get_terminal_size().columns
    max_line_length = term_width - 2
    min_line_length = max(10, term_width // 5)

    stream = sd.InputStream(
        channels=1, samplerate=FS, callback=audio_callback, blocksize=HOP_LENGTH
    )
    stream.start()

    try:
        offset = 0.0
        while True:
            frame = audio_buffer[-FRAME_LENGTH:]
            rms = np.sqrt(np.mean(frame ** 2))
            level = min(rms / args.sens, 1.0)
            length = int(min_line_length + (max_line_length - min_line_length) * level)
            pad = (max_line_length - length) // 2
            line = " " * pad + rainbow_line(length, offset) + " " * (
                max_line_length - length - pad
            )
            sys.stdout.write("\r" + line)
            sys.stdout.flush()
            offset = (offset + args.speed) % 1.0
            time.sleep(HOP_LENGTH / FS)
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop()
        stream.close()
        print("\nDone.")


if __name__ == "__main__":
    main()
