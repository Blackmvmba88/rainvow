import os
import time
from colorama import init, Fore, Style

init()

QUARK_COLORS = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN]
ANTI_COLOR = Fore.MAGENTA

ANTIQ = f"{ANTI_COLOR}Q̄{Style.RESET_ALL}"

ASCII_LINES = [
    "  {q0}   {q1}",
    " {q2} {aq} {q3}"
]

def show_pentaquark(colors):
    os.system('clear')
    q0, q1, q2, q3 = [c + 'Q' + Style.RESET_ALL for c in colors]
    print("Pentaquark:\n")
    print(ASCII_LINES[0].format(q0=q0, q1=q1))
    print(ASCII_LINES[1].format(q2=q2, aq=ANTIQ, q3=q3))
    print("\nCuatro quarks y un antiquark en una partícula.")
    print("Presiona Ctrl+C para salir.")

if __name__ == '__main__':
    i = 0
    try:
        while True:
            color_order = QUARK_COLORS[i:] + QUARK_COLORS[:i]
            show_pentaquark(color_order)
            time.sleep(0.7)
            i = (i + 1) % len(QUARK_COLORS)
    except KeyboardInterrupt:
        os.system('clear')
        print('Hasta luego!')

