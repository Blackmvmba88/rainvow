# 📡 Documentación de API - Rainvow

Esta documentación describe las APIs y componentes reutilizables del proyecto Rainvow.

---

## 📖 Tabla de Contenidos

1. [API REST - Spotify Live](#api-rest---spotify-live)
2. [API Python - Visualizador de Audio](#api-python---visualizador-de-audio)
3. [API Python - Monitor de Sistema](#api-python---monitor-de-sistema)
4. [API Python - Control RGB](#api-python---control-rgb)
5. [Ejemplos de Integración](#ejemplos-de-integración)

---

## 🎵 API REST - Spotify Live

Base URL: `http://localhost:8888`

### Autenticación

Todos los endpoints protegidos requieren autenticación previa mediante OAuth.

### Endpoints

#### `GET /`

Página principal de la aplicación.

**Respuesta**: HTML

**Ejemplo**:
```bash
curl http://localhost:8888/
```

---

#### `GET /login`

Inicia el flujo de autenticación OAuth con Spotify.

**Respuesta**: Redirect a Spotify OAuth

**Ejemplo**:
```bash
curl -L http://localhost:8888/login
```

---

#### `GET /callback`

Endpoint de callback para OAuth. No debe ser llamado manualmente.

**Parámetros**:
- `code` (query string): Código de autorización de Spotify

**Respuesta**: Redirect a `/`

---

#### `GET /current`

Obtiene información de la canción actualmente en reproducción.

**Autenticación**: Requerida

**Respuesta exitosa (200)**:
```json
{
  "name": "Bohemian Rhapsody",
  "artists": "Queen",
  "album": "A Night at the Opera",
  "image": "https://i.scdn.co/image/...",
  "preview": "https://p.scdn.co/mp3-preview/..."
}
```

**Error - No autenticado (401)**:
```json
{
  "error": "not_authenticated"
}
```

**Error - No hay reproducción (200)**:
```json
{
  "error": "no_track"
}
```

**Ejemplo**:
```bash
# Con sesión activa
curl -b cookies.txt http://localhost:8888/current
```

**Ejemplo JavaScript**:
```javascript
fetch('/current')
  .then(response => response.json())
  .then(data => {
    if (data.error) {
      console.log('No track playing');
    } else {
      console.log(`Now playing: ${data.name} by ${data.artists}`);
    }
  });
```

---

#### `GET /search`

Busca canciones en el catálogo de Spotify.

**Autenticación**: Requerida

**Parámetros**:
- `q` (query string, requerido): Término de búsqueda

**Respuesta exitosa (200)**:
```json
{
  "results": [
    {
      "name": "Stairway to Heaven",
      "artists": "Led Zeppelin",
      "image": "https://i.scdn.co/image/...",
      "preview": "https://p.scdn.co/mp3-preview/..."
    },
    ...
  ]
}
```

**Error - No autenticado (401)**:
```json
{
  "error": "not_authenticated"
}
```

**Sin resultados (200)**:
```json
{
  "results": []
}
```

**Ejemplo**:
```bash
# Con sesión activa
curl -b cookies.txt "http://localhost:8888/search?q=pink+floyd"
```

**Ejemplo JavaScript**:
```javascript
const query = 'pink floyd';
fetch(`/search?q=${encodeURIComponent(query)}`)
  .then(response => response.json())
  .then(data => {
    data.results.forEach(track => {
      console.log(`${track.name} - ${track.artists}`);
    });
  });
```

**Ejemplo Python**:
```python
import requests

session = requests.Session()
# ... realizar login ...

# Buscar canciones
response = session.get('http://localhost:8888/search', params={'q': 'beatles'})
tracks = response.json()['results']

for track in tracks:
    print(f"{track['name']} - {track['artists']}")
```

---

## 🌈 API Python - Visualizador de Audio

Módulo: `ondads.py`

### Funciones Exportables

#### `get_band_amps(audio_block, fs, n_bands) -> np.ndarray`

Analiza un bloque de audio y retorna las amplitudes por banda de frecuencia.

**Parámetros**:
- `audio_block` (np.ndarray): Array de audio con shape `(n_samples, 1)`
- `fs` (int): Frecuencia de muestreo (sample rate) en Hz
- `n_bands` (int): Número de bandas de frecuencia a generar

**Retorna**:
- `np.ndarray`: Array de amplitudes normalizadas (logarítmicas) con shape `(n_bands,)`

**Ejemplo**:
```python
import numpy as np
from ondads import get_band_amps

# Generar audio de prueba (440 Hz - nota A)
fs = 44100
duration = 0.05
t = np.linspace(0, duration, int(fs * duration))
audio = np.sin(2 * np.pi * 440 * t).reshape(-1, 1)

# Analizar frecuencias en 7 bandas
amps = get_band_amps(audio, fs, 7)
print(f"Amplitudes: {amps}")
# Output: [0.123, 2.456, 0.789, ...]
```

**Uso avanzado**:
```python
# Crear visualizador personalizado
def my_custom_visualizer():
    import sounddevice as sd
    
    fs = 44100
    blocksize = int(fs * 0.05)
    
    with sd.InputStream(channels=1, samplerate=fs, blocksize=blocksize) as stream:
        while True:
            audio_block = stream.read(blocksize)[0]
            amps = get_band_amps(audio_block, fs, 10)  # 10 bandas
            
            # Tu lógica de visualización aquí
            for i, amp in enumerate(amps):
                print(f"Banda {i}: {'█' * int(amp * 20)}")
```

---

#### `audio_source() -> Generator`

Generador que produce bloques de audio desde el micrófono o ruido de prueba.

**Yields**:
- `np.ndarray`: Bloques de audio con shape `(BLOCKSIZE, 1)`

**Ejemplo**:
```python
from ondads import audio_source, get_band_amps

# Procesar audio en tiempo real
for audio_block in audio_source():
    amps = get_band_amps(audio_block, 44100, 7)
    print(f"Amplitudes: {amps}")
    # Presiona Ctrl+C para detener
```

---

#### `run_visualizer()`

Ejecuta el visualizador completo con renderizado de consola.

**Ejemplo**:
```python
from ondads import run_visualizer

# Ejecutar visualizador
try:
    run_visualizer()
except KeyboardInterrupt:
    print("Detenido")
```

---

### Constantes Configurables

```python
# Personalizar antes de importar o modificar directamente
N_BANDS = 7          # Número de bandas de frecuencia
BAR_HEIGHT = 12      # Altura de las barras en caracteres
FS = 44100           # Sample rate
DURATION = 0.05      # Duración de cada bloque en segundos
MIN_GAIN = 0.5       # Ganancia mínima adaptativa
MAX_GAIN = 10.0      # Ganancia máxima adaptativa
ADAPT_SPEED = 0.1    # Velocidad de adaptación (0-1)
```

---

## 🖥️ API Python - Monitor de Sistema

Módulo: `hydra_observer.py`

### Funciones Exportables

#### `log_event(event_type, info)`

Registra un evento en el log.

**Parámetros**:
- `event_type` (str): Tipo de evento ('key', 'click', 'system', 'audio', 'hydra')
- `info` (dict): Información del evento

**Ejemplo**:
```python
from hydra_observer import log_event

log_event('custom', {
    'action': 'user_interaction',
    'details': 'Button clicked'
})
```

---

#### `record_audio(duration=5, samplerate=44100)`

Graba audio del micrófono y lo guarda en la carpeta logs.

**Parámetros**:
- `duration` (float): Duración en segundos
- `samplerate` (int): Frecuencia de muestreo

**Ejemplo**:
```python
from hydra_observer import record_audio

# Grabar 10 segundos de audio
record_audio(duration=10, samplerate=48000)
```

---

#### `active_window_title() -> str | None`

Obtiene el título de la ventana activa.

**Retorna**:
- `str`: Título de la ventana o `None` si no está disponible

**Ejemplo**:
```python
from hydra_observer import active_window_title

window = active_window_title()
if window:
    print(f"Ventana activa: {window}")
else:
    print("No se puede detectar ventana (macOS o pygetwindow no instalado)")
```

---

### Variables de Entorno

```bash
# Configuración del monitor
export HYDRA_CLI="hydra"                    # Path al CLI de Hydra
export HYDRA_SLEEP_DURATION="2.0"           # Intervalo de monitoreo (segundos)
export HYDRA_USER_CONSENT="true"            # Habilitar monitoreo de teclado
```

---

## 🌈 API Python - Control RGB

Módulo: `keyboard_rgb.py`

### Uso Programático

```python
import time
from openrgb import OpenRGBClient

# Conectar al servidor OpenRGB
client = OpenRGBClient(host='127.0.0.1', port=6742)

# Obtener dispositivos
devices = client.devices

# Seleccionar teclado (ajusta el índice según tu setup)
keyboard = devices[0]

# Definir colores del arcoíris
rainbow = [
    (255, 0, 0),      # Rojo
    (255, 165, 0),    # Naranja
    (255, 255, 0),    # Amarillo
    (0, 255, 0),      # Verde
    (0, 255, 255),    # Cyan
    (0, 0, 255),      # Azul
    (255, 0, 255),    # Magenta
]

# Animar colores
while True:
    for color in rainbow:
        keyboard.set_color(color)
        time.sleep(0.5)
```

---

## 🔧 Ejemplos de Integración

### Integración: Visualizador + Spotify

Sincroniza el visualizador de audio con la canción en reproducción:

```python
import requests
import time
from ondads import get_band_amps, audio_source

# Sesión con Spotify Live
session = requests.Session()
# ... login ...

def get_current_track():
    response = session.get('http://localhost:8888/current')
    data = response.json()
    if 'error' not in data:
        return data['name'], data['artists']
    return None, None

# Visualizar con información de Spotify
for audio_block in audio_source():
    track, artist = get_current_track()
    amps = get_band_amps(audio_block, 44100, 7)
    
    if track:
        print(f"🎵 {track} - {artist}")
    print(f"Amplitudes: {amps}")
    
    time.sleep(1)
```

---

### Integración: RGB + Audio

Sincroniza luces RGB con el audio:

```python
import numpy as np
from openrgb import OpenRGBClient
from ondads import get_band_amps, audio_source

client = OpenRGBClient()
keyboard = client.devices[0]

for audio_block in audio_source():
    amps = get_band_amps(audio_block, 44100, 7)
    
    # Convertir amplitud promedio a color
    avg_amp = np.mean(amps)
    brightness = int(avg_amp * 255)
    
    # Color basado en amplitud
    color = (brightness, 0, 255 - brightness)
    keyboard.set_color(color)
```

---

### Integración: Monitor + Spotify

Detecta contexto musical y actualiza Spotify:

```python
import time
from hydra_observer import active_window_title, log_event
import requests

session = requests.Session()
# ... login ...

last_window = None

while True:
    window = active_window_title()
    
    if window != last_window:
        log_event('window_change', {'window': window})
        
        # Si detecta reproductor de música
        if window and 'spotify' in window.lower():
            response = session.get('http://localhost:8888/current')
            track = response.json()
            if 'error' not in track:
                print(f"Detectado Spotify: {track['name']}")
        
        last_window = window
    
    time.sleep(2)
```

---

### Integración: Crear Dashboard Web

Dashboard que muestra todos los componentes:

```python
from flask import Flask, jsonify
import psutil
from ondads import get_band_amps
import numpy as np

app = Flask(__name__)

@app.route('/api/system')
def system_metrics():
    return jsonify({
        'cpu': psutil.cpu_percent(),
        'memory': psutil.virtual_memory().percent,
        'timestamp': time.time()
    })

@app.route('/api/audio')
def audio_levels():
    # Capturar un bloque de audio
    audio_block = np.random.uniform(-1, 1, (2205, 1))  # Simulado
    amps = get_band_amps(audio_block, 44100, 7)
    
    return jsonify({
        'bands': amps.tolist(),
        'timestamp': time.time()
    })

if __name__ == '__main__':
    app.run(port=5000)
```

HTML frontend:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Rainvow Dashboard</title>
</head>
<body>
    <h1>Rainvow Dashboard</h1>
    <div id="system"></div>
    <div id="audio"></div>
    
    <script>
        setInterval(() => {
            fetch('/api/system')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('system').innerHTML = 
                        `CPU: ${data.cpu}% | Memory: ${data.memory}%`;
                });
            
            fetch('/api/audio')
                .then(r => r.json())
                .then(data => {
                    const bars = data.bands.map(amp => '█'.repeat(amp * 10)).join(' ');
                    document.getElementById('audio').innerHTML = bars;
                });
        }, 1000);
    </script>
</body>
</html>
```

---

## 📊 Esquemas de Datos

### Formato de Log del Monitor

```json
{
  "time": 1697388123.456,
  "event": "system",
  "info": {
    "window": "Visual Studio Code",
    "cpu": 45.2,
    "mem": 62.8
  }
}
```

### Tipos de Eventos

| Tipo | Descripción | Campos en `info` |
|------|-------------|------------------|
| `key` | Tecla presionada | (string): Tecla |
| `click` | Click de mouse | `button`, `pos` |
| `system` | Métricas de sistema | `window`, `cpu`, `mem` |
| `audio` | Audio grabado | `file` |
| `hydra` | Comando a Hydra | (string): Comando |

---

## 🔐 Consideraciones de Seguridad

### Spotify API

- ✅ Tokens almacenados en sesión del servidor (no en cliente)
- ✅ Renovación automática de tokens
- ✅ No exposición de Client Secret al navegador
- ⚠️ Usar HTTPS en producción
- ⚠️ Configurar FLASK_SECRET con valor seguro

### Monitor de Sistema

- ⚠️ Requiere consentimiento explícito para monitoreo de teclado
- ⚠️ Excluye ventanas con "password" o "login" en el título
- ✅ Logs almacenados localmente
- ⚠️ No compartir logs sin sanitizar

---

## 📝 Mejores Prácticas

1. **Manejo de Errores**
   ```python
   try:
       response = session.get('/current')
       response.raise_for_status()
       data = response.json()
   except requests.exceptions.RequestException as e:
       print(f"Error: {e}")
   ```

2. **Rate Limiting**
   ```python
   import time
   last_request = 0
   MIN_INTERVAL = 1.0
   
   def rate_limited_request():
       global last_request
       now = time.time()
       if now - last_request < MIN_INTERVAL:
           time.sleep(MIN_INTERVAL - (now - last_request))
       last_request = time.time()
       return requests.get('...')
   ```

3. **Gestión de Recursos**
   ```python
   import atexit
   
   def cleanup():
       print("Limpiando recursos...")
       # Cerrar conexiones, guardar logs, etc.
   
   atexit.register(cleanup)
   ```

---

## 🔄 Control de Versiones de API

**Versión actual**: v1.0

Esta documentación corresponde a la versión 1.0 de las APIs de Rainvow.

---

## 📞 Soporte

Para preguntas sobre la API:
1. Consulta el código fuente en cada módulo
2. Revisa los ejemplos en [QUICKSTART.md](QUICKSTART.md)
3. Abre un issue en GitHub con la etiqueta `api`

---

**Última actualización**: 2025-10-15
