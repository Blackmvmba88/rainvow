#!/bin/zsh

# TikTok streaming helper script

# Exit on error and log everything
set -e
exec > >(tee -a ~/live.log) 2>&1

# ------ Dependency check ------

required_formulas=(scrcpy vlc switchaudio-osx adb)
for formula in $required_formulas; do
  if ! command -v $formula >/dev/null 2>&1; then
    echo "Instalando $formula via Homebrew..."
    brew install $formula
  fi
done

# BlackHole is a cask
if ! brew list --cask 2>/dev/null | grep -q '^blackhole-2ch$'; then
  echo "Instalando blackhole-2ch via Homebrew..."
  brew install --cask blackhole-2ch
fi

# ------ Preconditions ------

# Check aggregated audio device
if ! SwitchAudioSource -a -t output | grep -q 'BH+Mic'; then
  echo "El dispositivo de audio 'BH+Mic' no existe. Configura el Dispositivo Agregado en Audio MIDI." >&2
  exit 1
fi

# Check Android device connection
if ! adb devices | grep -w 'device' >/dev/null; then
  echo "No se encontró un dispositivo Android con depuración USB." >&2
  exit 1
fi

# ------ Clone sndcpy if missing ------

SNDCOPY_DIR=~/Apps/sndcpy
if [ ! -x "$SNDCOPY_DIR/sndcpy" ]; then
  echo "Clonando sndcpy desde GitHub..."
  mkdir -p ~/Apps
  git clone https://github.com/rom1v/sndcpy.git "$SNDCOPY_DIR"
fi

# ------ Save current audio output ------

DEFAULT_AUDIO=$(SwitchAudioSource -c -t output)

cleanup() {
  echo "Cerrando procesos y restaurando audio..."
  kill $SCRCPY_PID $SNDCOPY_PID 2>/dev/null || true
  SwitchAudioSource -t output -s "$DEFAULT_AUDIO"
  exit 0
}
trap cleanup INT

# ------ Start sndcpy and scrcpy ------

"$SNDCOPY_DIR/sndcpy" &
SNDCOPY_PID=$!

scrcpy --bit-rate 6M --max-size 1080 &
SCRCPY_PID=$!

# Give sndcpy time to expose the stream and open VLC if not running
sleep 2
if ! pgrep -f VLC >/dev/null; then
  open -g -a VLC
fi

# ------ Route audio to BH+Mic ------

SwitchAudioSource -t output -s 'BH+Mic'

osascript -e 'display notification "✅ Ruteo listo – abre OBS y dale Start Streaming" with title "TikTok Live Setup"'

echo "Presiona CTRL-C para detener."

wait $SCRCPY_PID
cleanup
