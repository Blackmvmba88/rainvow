"""Dashboard unificado para Rainvow - WebUI para monitorear todos los componentes.

Esta aplicación Flask proporciona una interfaz web unificada que permite
visualizar y monitorear todos los componentes del proyecto Rainvow:
- Sistema (CPU, memoria, ventana activa)
- Audio (visualización en tiempo real)
- Spotify (canción actual)
- RGB Keyboard (estado)
- Enlaces a demos AR y otras utilidades

Características:
    - Dashboard centralizado con diseño de tarjetas
    - Actualizaciones en tiempo real con WebSocket
    - API REST para cada componente
    - Tema oscuro consistente con el proyecto
    - Integración con componentes existentes

Variables de entorno opcionales:
    DASHBOARD_PORT: Puerto del servidor (default: 5000)
    SPOTIPY_CLIENT_ID: Para integración con Spotify
    SPOTIPY_CLIENT_SECRET: Para integración con Spotify

Uso:
    python3 dashboard.py

El servidor escucha en http://0.0.0.0:5000
"""

import os
import time
import threading
import psutil
import numpy as np
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit

# Importar componentes existentes
try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except (ImportError, OSError):
    AUDIO_AVAILABLE = False

try:
    import pygetwindow as gw
    WINDOW_TRACKING = True
except (ImportError, ModuleNotFoundError):
    WINDOW_TRACKING = False

try:
    from openrgb import OpenRGBClient
    RGB_AVAILABLE = True
except ImportError:
    RGB_AVAILABLE = False

try:
    import spotipy  # noqa: F401
    from spotipy.oauth2 import SpotifyOAuth  # noqa: F401
    SPOTIFY_AVAILABLE = True
except ImportError:
    SPOTIFY_AVAILABLE = False

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'rainvow-dashboard-secret')
socketio = SocketIO(app, cors_allowed_origins="*")

# Estado global del sistema
system_state = {
    'cpu': 0,
    'memory': 0,
    'active_window': 'N/A',
    'audio_bands': [0] * 7,
    'spotify': None,
    'rgb_status': 'disconnected',
    'uptime': time.time()
}

state_lock = threading.Lock()

# Configuración de audio
FS = 44100
DURATION = 0.1
BLOCKSIZE = int(FS * DURATION)
N_BANDS = 7


def get_band_amps(audio_block: np.ndarray, fs: int, n_bands: int) -> list:
    """Calcula amplitudes por banda de frecuencia (adaptado de ondads.py).

    Args:
        audio_block: Array de audio
        fs: Frecuencia de muestreo
        n_bands: Número de bandas

    Returns:
        Lista de amplitudes normalizadas [0-1]
    """
    if len(audio_block.shape) == 1:
        audio_data = audio_block
    else:
        audio_data = audio_block[:, 0]

    fft = np.fft.rfft(audio_data * np.hanning(len(audio_data)))
    mag = np.abs(fft)
    freqs = np.fft.rfftfreq(len(audio_data), 1 / fs)
    max_freq = fs // 2
    band_edges = np.linspace(0, max_freq, n_bands + 1)

    amps = []
    for i in range(n_bands):
        idx = np.where((freqs >= band_edges[i]) & (freqs < band_edges[i + 1]))[0]
        if len(idx) > 0:
            amps.append(float(mag[idx].max()))
        else:
            amps.append(0.0)

    # Normalizar logarítmicamente
    amps = np.log1p(amps)
    max_amp = max(amps) if max(amps) > 0 else 1
    return [float(a / max_amp) for a in amps]


def audio_monitor_thread():
    """Thread que monitorea audio continuamente y actualiza el estado."""
    if not AUDIO_AVAILABLE:
        return

    try:
        with sd.InputStream(channels=1, samplerate=FS, blocksize=BLOCKSIZE) as stream:
            while True:
                audio_block, _ = stream.read(BLOCKSIZE)
                bands = get_band_amps(audio_block, FS, N_BANDS)

                with state_lock:
                    system_state['audio_bands'] = bands

                socketio.emit('audio_update', {'bands': bands})
                time.sleep(0.05)
    except Exception as e:
        print(f"Error en monitoreo de audio: {e}")
        # Fallback a datos de prueba
        while True:
            bands = [float(np.random.random() * 0.5) for _ in range(N_BANDS)]
            with state_lock:
                system_state['audio_bands'] = bands
            socketio.emit('audio_update', {'bands': bands})
            time.sleep(0.1)


def system_monitor_thread():
    """Thread que monitorea métricas del sistema continuamente."""
    while True:
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory().percent

        # Obtener ventana activa si está disponible
        active_window = 'N/A'
        if WINDOW_TRACKING:
            try:
                win = gw.getActiveWindow()
                if win:
                    active_window = win.title[:50]  # Limitar longitud
            except Exception:
                pass

        with state_lock:
            system_state['cpu'] = cpu
            system_state['memory'] = mem
            system_state['active_window'] = active_window

        socketio.emit('system_update', {
            'cpu': cpu,
            'memory': mem,
            'active_window': active_window
        })

        time.sleep(2)


def check_rgb_status():
    """Verifica si el servidor OpenRGB está disponible."""
    if not RGB_AVAILABLE:
        return 'no_disponible'

    try:
        client = OpenRGBClient(host='localhost', port=6742)
        keyboards = [d for d in client.devices if d.device_type.name == "KEYBOARD"]
        if keyboards:
            return 'conectado'
        return 'sin_teclado'
    except Exception:
        return 'desconectado'


def check_spotify_status():
    """Verifica si hay una sesión activa de Spotify."""
    if not SPOTIFY_AVAILABLE:
        return None

    # Aquí se podría integrar con la sesión de spotify_live
    # Por ahora retornamos un mensaje indicando que está disponible
    return {'status': 'disponible', 'message': 'Usar Spotify Live app'}


@app.route('/')
def index():
    """Página principal del dashboard."""
    return render_template('dashboard.html',
                           audio_available=AUDIO_AVAILABLE,
                           spotify_available=SPOTIFY_AVAILABLE,
                           rgb_available=RGB_AVAILABLE,
                           window_tracking=WINDOW_TRACKING)


@app.route('/api/status')
def api_status():
    """API endpoint que retorna el estado completo del sistema."""
    with state_lock:
        state_copy = system_state.copy()

    # Agregar información adicional
    state_copy['uptime_seconds'] = int(time.time() - system_state['uptime'])
    state_copy['rgb_status'] = check_rgb_status()
    state_copy['spotify'] = check_spotify_status()

    return jsonify(state_copy)


@app.route('/api/system')
def api_system():
    """API endpoint para métricas del sistema."""
    with state_lock:
        return jsonify({
            'cpu': system_state['cpu'],
            'memory': system_state['memory'],
            'active_window': system_state['active_window']
        })


@app.route('/api/audio')
def api_audio():
    """API endpoint para datos de audio."""
    with state_lock:
        return jsonify({
            'bands': system_state['audio_bands'],
            'available': AUDIO_AVAILABLE
        })


@app.route('/api/capabilities')
def api_capabilities():
    """API endpoint que retorna las capacidades disponibles."""
    return jsonify({
        'audio': AUDIO_AVAILABLE,
        'spotify': SPOTIFY_AVAILABLE,
        'rgb': RGB_AVAILABLE,
        'window_tracking': WINDOW_TRACKING
    })


@socketio.on('connect')
def handle_connect():
    """Maneja nuevas conexiones WebSocket."""
    emit('connected', {'message': 'Conectado al dashboard de Rainvow'})


@socketio.on('request_update')
def handle_request_update():
    """Envía actualización inmediata del estado al cliente."""
    with state_lock:
        emit('system_update', {
            'cpu': system_state['cpu'],
            'memory': system_state['memory'],
            'active_window': system_state['active_window']
        })
        emit('audio_update', {'bands': system_state['audio_bands']})


def start_background_threads():
    """Inicia los threads de monitoreo en background."""
    system_thread = threading.Thread(target=system_monitor_thread, daemon=True)
    system_thread.start()

    if AUDIO_AVAILABLE:
        audio_thread = threading.Thread(target=audio_monitor_thread, daemon=True)
        audio_thread.start()


if __name__ == '__main__':
    print("=" * 60)
    print("🌈 Dashboard Unificado de Rainvow")
    print("=" * 60)
    print(f"Audio disponible: {'✓' if AUDIO_AVAILABLE else '✗'}")
    print(f"Spotify disponible: {'✓' if SPOTIFY_AVAILABLE else '✗'}")
    print(f"RGB disponible: {'✓' if RGB_AVAILABLE else '✗'}")
    print(f"Seguimiento de ventanas: {'✓' if WINDOW_TRACKING else '✗'}")
    print("=" * 60)
    print("\nIniciando threads de monitoreo...")

    start_background_threads()

    port = int(os.environ.get('DASHBOARD_PORT', 5000))
    print(f"\n🚀 Dashboard disponible en http://0.0.0.0:{port}")
    print("Presiona Ctrl+C para detener\n")

    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
