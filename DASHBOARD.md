# Dashboard Unificado de Rainvow

![Dashboard Preview](../screenshots/dashboard_preview.png)

## Descripción

El Dashboard Unificado de Rainvow es una interfaz web que centraliza el monitoreo y control de todos los componentes del proyecto Rainvow en un solo lugar. Proporciona visualización en tiempo real de:

- **Métricas del Sistema**: CPU, memoria y ventana activa
- **Visualización de Audio**: Análisis de frecuencias en tiempo real con barras de colores del arcoíris
- **Integración con Spotify**: Estado y enlace a Spotify Live
- **Control RGB Keyboard**: Estado del servidor OpenRGB
- **Enlaces Rápidos**: Acceso a demos AR, AuraWave y otras utilidades

## Características

✨ **Características principales:**

- 🎨 **Diseño Moderno**: Interfaz con tema oscuro (#121212) consistente con el proyecto
- 🔄 **Tiempo Real**: Actualizaciones en vivo mediante WebSocket
- 📊 **Visualización de Datos**: Barras de progreso animadas y visualizador de audio
- 🔗 **Integración Completa**: Conexión con todos los componentes existentes
- 📱 **Responsive**: Se adapta a diferentes tamaños de pantalla
- 🚀 **Fácil de Usar**: Interfaz intuitiva con tarjetas organizadas

## Requisitos

### Dependencias Obligatorias

```bash
pip install flask flask-socketio python-socketio psutil numpy
```

### Dependencias Opcionales

Para habilitar todas las funcionalidades:

```bash
# Audio en tiempo real
pip install sounddevice

# Integración con Spotify
pip install spotipy

# Control RGB Keyboard
pip install openrgb-python

# Seguimiento de ventanas (no disponible en macOS)
pip install pygetwindow
```

O instalar todo desde requirements.txt:

```bash
pip install -r requirements.txt
```

## Instalación y Uso

### 1. Instalación

```bash
# Clonar el repositorio si aún no lo has hecho
git clone https://github.com/Blackmvmba88/rainvow.git
cd rainvow

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Iniciar el Dashboard

```bash
python3 dashboard.py
```

El dashboard estará disponible en: **http://localhost:5000**

### 3. Configuración del Puerto (Opcional)

```bash
# Usar un puerto diferente
DASHBOARD_PORT=8080 python3 dashboard.py
```

## Estructura del Dashboard

### Tarjetas Disponibles

#### 1. 💻 Sistema
Muestra métricas del sistema en tiempo real:
- **CPU**: Porcentaje de uso con barra de progreso codificada por colores
- **Memoria**: Porcentaje de uso de RAM
- **Uptime**: Tiempo desde que se inició el dashboard

#### 2. 🎵 Visualizador de Audio
Análisis de frecuencias de audio en tiempo real con 7 bandas de colores del arcoíris. Funciona si el micrófono está disponible, de lo contrario usa datos de prueba.

#### 3. 🪟 Ventana Activa
Muestra el título de la ventana actualmente enfocada (solo en sistemas soportados).

#### 4. 🎧 Spotify
- Estado de la integración con Spotify
- Enlace directo a Spotify Live (puerto 8888)

#### 5. ⌨️ RGB Keyboard
- Estado de conexión con OpenRGB
- Instrucciones para ejecutar el controlador

#### 6. 🔗 Utilidades y Demos
Enlaces rápidos a:
- AR Demo
- PDF Overlay
- AuraWave
- GitHub del proyecto
- Lista de scripts disponibles

## API REST

El dashboard expone varios endpoints API:

### GET /api/status
Retorna el estado completo del sistema:

```json
{
  "cpu": 45.2,
  "memory": 62.8,
  "active_window": "Visual Studio Code",
  "audio_bands": [0.2, 0.5, 0.8, 0.6, 0.4, 0.3, 0.2],
  "uptime_seconds": 3600,
  "rgb_status": "conectado",
  "spotify": {
    "status": "disponible",
    "message": "Usar Spotify Live app"
  }
}
```

### GET /api/system
Retorna solo métricas del sistema:

```json
{
  "cpu": 45.2,
  "memory": 62.8,
  "active_window": "Visual Studio Code"
}
```

### GET /api/audio
Retorna datos de audio:

```json
{
  "bands": [0.2, 0.5, 0.8, 0.6, 0.4, 0.3, 0.2],
  "available": true
}
```

### GET /api/capabilities
Retorna capacidades disponibles:

```json
{
  "audio": true,
  "spotify": true,
  "rgb": false,
  "window_tracking": true
}
```

## WebSocket

El dashboard usa WebSocket para actualizaciones en tiempo real:

### Eventos del Servidor

- **`system_update`**: Actualización de métricas del sistema (cada 2 segundos)
- **`audio_update`**: Actualización de bandas de audio (cada 50ms cuando audio disponible)
- **`connected`**: Confirmación de conexión

### Eventos del Cliente

- **`request_update`**: Solicitar actualización inmediata del estado

## Troubleshooting

### El dashboard no muestra audio

**Problema**: La tarjeta de audio muestra "Audio no disponible"

**Solución**:
```bash
pip install sounddevice numpy
```

Asegúrate de tener un micrófono conectado o habilitado.

### RGB Keyboard muestra "Desconectado"

**Problema**: No puede conectar con OpenRGB

**Soluciones**:
1. Instalar OpenRGB: https://openrgb.org/
2. Ejecutar OpenRGB con opción `--server`
3. Asegurarse de que el puerto 6742 esté disponible

### Seguimiento de ventanas no funciona

**Problema**: "Seguimiento de ventanas no disponible"

**Nota**: pygetwindow no funciona en macOS. Solo está disponible en Windows y Linux.

### Error de permisos de micrófono

**Problema**: El navegador no puede acceder al micrófono

**Solución**: El dashboard en sí no usa el micrófono del navegador, solo del sistema. Asegúrate de que el proceso Python tenga permisos de micrófono.

## Arquitectura

### Backend (dashboard.py)

El backend está construido con Flask y Flask-SocketIO:

- **Threads de Monitoreo**:
  - `system_monitor_thread()`: Monitorea CPU, memoria y ventana activa
  - `audio_monitor_thread()`: Captura y analiza audio en tiempo real

- **Rutas HTTP**:
  - `/`: Página principal del dashboard
  - `/api/*`: Endpoints REST para datos

- **WebSocket**: Emisión de eventos en tiempo real a clientes conectados

### Frontend (templates/dashboard.html)

El frontend es una SPA (Single Page Application) con:

- **Socket.IO Client**: Para recibir actualizaciones en tiempo real
- **Fetch API**: Para consultas REST cada 5 segundos
- **CSS Grid**: Layout responsive con tarjetas
- **Vanilla JavaScript**: Sin frameworks, solo JS puro

## Extensión

### Agregar Nueva Tarjeta

1. Editar `dashboard.py` para agregar nuevo endpoint:

```python
@app.route('/api/mi_componente')
def api_mi_componente():
    return jsonify({'data': 'mi_data'})
```

2. Editar `templates/dashboard.html` para agregar la tarjeta:

```html
<div class="card">
    <div class="card-header">
        <span class="card-icon">🆕</span>
        <span class="card-title">Mi Componente</span>
    </div>
    <div id="miComponente">Cargando...</div>
</div>
```

3. Agregar JavaScript para actualizar la tarjeta:

```javascript
setInterval(() => {
    fetch('/api/mi_componente')
        .then(r => r.json())
        .then(data => {
            document.getElementById('miComponente').textContent = data.data;
        });
}, 5000);
```

## Integración con Otros Componentes

### Spotify Live

El dashboard se integra con Spotify Live (puerto 8888). Para usar ambos:

```bash
# Terminal 1: Spotify Live
cd spotify_live
python3 app.py

# Terminal 2: Dashboard
python3 dashboard.py
```

### Hydra Observer

El dashboard puede funcionar independientemente de hydra_observer.py, pero ambos pueden ejecutarse simultáneamente para tener logs adicionales:

```bash
# Terminal 1: Dashboard
python3 dashboard.py

# Terminal 2: Hydra Observer (logs a archivo)
python3 hydra_observer.py
```

## Contribuir

Para contribuir al dashboard:

1. Mantener el tema oscuro (#121212)
2. Usar colores del arcoíris para visualizaciones
3. Seguir la estructura de tarjetas existente
4. Documentar nuevos endpoints API
5. Mantener mensajes en español

## Licencia

Parte del proyecto Rainvow. Ver LICENSE en el directorio raíz.

## Soporte

Para reportar bugs o sugerir mejoras:
- Issues: https://github.com/Blackmvmba88/rainvow/issues
- Documentación: README.md del proyecto principal
