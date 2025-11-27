# 🚀 Guía de Inicio Rápido - Rainvow

Esta guía te ayudará a ejecutar los componentes principales de Rainvow en menos de 10 minutos.

## 📋 Requisitos Previos

- **Python 3.8+** (recomendado 3.10+)
- **pip** (gestor de paquetes de Python)
- **Micrófono** (para visualizador de audio)
- **Cuenta de Spotify** (para integración musical)

## 🎯 Opción 1: Inicio Rápido (Solo Visualizador)

Si solo quieres ver el visualizador de audio funcionando:

```bash
# 1. Instalar dependencias mínimas
pip install numpy sounddevice rich colorama

# 2. Ejecutar el visualizador
python3 ondads.py
```

¡Eso es todo! Deberías ver barras de colores del arcoíris moviéndose con el audio de tu micrófono.

**Presiona `Ctrl+C` para detener.**

### Solución de Problemas

Si no tienes micrófono o aparece un error:
- ✅ El script automáticamente usará ruido de prueba
- ✅ Verás el mensaje: "No se pudo iniciar la entrada de audio"
- ✅ La visualización funcionará igual con datos de prueba

---

## 🎵 Opción 2: Spotify Live (Integración Musical)

### Paso 1: Configurar Credenciales de Spotify

1. Ve a [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Crea una nueva aplicación
3. En "Edit Settings", agrega esta Redirect URI:
   ```
   http://localhost:8888/callback
   ```
4. Copia tu **Client ID** y **Client Secret**

### Paso 2: Instalar Dependencias

```bash
pip install flask spotipy
```

### Paso 3: Configurar Variables de Entorno

**En Linux/macOS:**
```bash
export SPOTIPY_CLIENT_ID="tu-client-id"
export SPOTIPY_CLIENT_SECRET="tu-client-secret"
export SPOTIPY_REDIRECT_URI="http://localhost:8888/callback"
export FLASK_SECRET="cualquier-cadena-aleatoria"
```

**En Windows (PowerShell):**
```powershell
$env:SPOTIPY_CLIENT_ID="tu-client-id"
$env:SPOTIPY_CLIENT_SECRET="tu-client-secret"
$env:SPOTIPY_REDIRECT_URI="http://localhost:8888/callback"
$env:FLASK_SECRET="cualquier-cadena-aleatoria"
```

**En Windows (CMD):**
```cmd
set SPOTIPY_CLIENT_ID=tu-client-id
set SPOTIPY_CLIENT_SECRET=tu-client-secret
set SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
set FLASK_SECRET=cualquier-cadena-aleatoria
```

### Paso 4: Ejecutar la Aplicación

```bash
cd spotify_live
python3 app.py
```

### Paso 5: Usar la Aplicación

1. Abre tu navegador en `http://localhost:8888`
2. Haz clic en "Iniciar sesión con Spotify"
3. Autoriza la aplicación en Spotify
4. ¡Listo! Verás la canción que estás escuchando

**Características disponibles:**
- Ver canción actual en reproducción
- Buscar canciones en el catálogo de Spotify
- Escuchar previsualizaciones de audio

---

## 🖥️ Opción 3: Monitor de Sistema (Hydra Observer)

Monitorea tu sistema y detecta contextos específicos.

### Instalar Dependencias

```bash
pip install psutil pynput numpy sounddevice colorama

# En Linux/Windows (no macOS):
pip install pygetwindow
```

### Configurar Variables de Entorno (Opcional)

```bash
# Habilitar monitoreo de teclado (requiere consentimiento explícito)
export HYDRA_USER_CONSENT="true"

# Intervalo de monitoreo en segundos (default: 2.0)
export HYDRA_SLEEP_DURATION="2.0"

# Path al CLI de Hydra (si tienes Hydra instalado)
export HYDRA_CLI="hydra"
```

### Ejecutar el Monitor

```bash
python3 hydra_observer.py
```

**Presiona `Ctrl+C` para detener y guardar los logs.**

Los logs se guardarán en la carpeta `logs/` con formato JSON.

---

## 🌈 Opción 4: Control de Teclado RGB

Controla las luces de tu teclado RGB con colores del arcoíris.

### Requisitos

- Teclado RGB compatible con OpenRGB
- [OpenRGB](https://openrgb.org/) instalado y ejecutándose con `--server`

### Instalar Dependencias

```bash
pip install openrgb-python
```

### Ejecutar el Controlador

```bash
# Para teclado local
python3 keyboard_rgb.py --show --host 127.0.0.1

# Para teclado remoto
python3 keyboard_rgb.py --show --host 192.168.1.100
```

**Nota para macOS**: OpenRGB no tiene soporte nativo. Ejecuta OpenRGB en otra máquina (Windows/Linux) y conéctate remotamente.

---

## 🥽 Opción 5: Demo de Realidad Aumentada

Experiencia AR con marcadores y efectos visuales.

### Requisitos

- Navegador moderno (Chrome, Firefox, Safari)
- Cámara web
- Marcador HIRO impreso: [Descargar aquí](https://raw.githubusercontent.com/AR-js-org/AR.js/master/data/images/HIRO.jpg)

### Paso 1: Iniciar Servidor Local

```bash
# Con Python
python3 -m http.server 8000

# O con Node.js
npx http-server
```

### Paso 2: Abrir en Navegador

1. Abre `http://localhost:8000/ar.html`
2. Concede permisos de cámara
3. Apunta la cámara al marcador HIRO
4. ¡Verás un cubo 3D animado con efectos Hydra!

### Bonus: Visor de PDF con Efectos

Abre `http://localhost:8000/pdf_overlay.html` y carga cualquier PDF desde tu computadora.

---

## 📦 Instalación Completa (Todos los Componentes)

Si quieres instalar todo de una vez:

```bash
# 1. Clonar el repositorio
git clone https://github.com/Blackmvmba88/rainvow.git
cd rainvow

# 2. Crear entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar todas las dependencias
pip install -r requirements.txt

# 4. Verificar instalación
python3 -c "import numpy, sounddevice, rich; print('✅ Dependencias básicas instaladas')"
python3 -c "import flask, spotipy; print('✅ Dependencias de Spotify instaladas')"
```

---

## 🆘 Solución de Problemas Comunes

### Error: "ModuleNotFoundError"

**Problema**: Falta instalar una dependencia.

**Solución**:
```bash
pip install <nombre-del-modulo>
```

### Error: "PermissionError" en Micrófono

**Problema**: El sistema no tiene permisos para acceder al micrófono.

**Solución**:
- **macOS**: Ve a Preferencias del Sistema → Seguridad y Privacidad → Micrófono
- **Windows**: Ve a Configuración → Privacidad → Micrófono
- **Linux**: Verifica que tu usuario esté en el grupo `audio`

### Spotify Live: "401 Unauthorized"

**Problema**: Credenciales incorrectas o token expirado.

**Solución**:
1. Verifica que las variables de entorno estén configuradas
2. Verifica que el Client ID y Secret sean correctos
3. Asegúrate de que la Redirect URI coincida exactamente
4. Reinicia la aplicación Flask

### Hydra Observer: No detecta ventana activa

**Problema**: `pygetwindow` no está instalado o no es compatible.

**Solución**:
- En Linux/Windows: `pip install pygetwindow`
- En macOS: Esta funcionalidad no está disponible (limitación de la librería)

### Teclado RGB no responde

**Problema**: OpenRGB no está ejecutándose o no está en modo servidor.

**Solución**:
1. Inicia OpenRGB
2. Ve a Settings → Enable Server
3. Reinicia OpenRGB
4. Ejecuta el script de nuevo

---

## 📚 Próximos Pasos

Después de completar esta guía:

1. Lee [ARCHITECTURE.md](ARCHITECTURE.md) para entender la arquitectura del proyecto
2. Revisa [TESTING.md](TESTING.md) para ver las pruebas realizadas
3. Consulta [PROJECT_STATUS.md](PROJECT_STATUS.md) para el estado actual del proyecto
4. Lee el [CHANGELOG.md](CHANGELOG.md) para conocer las últimas actualizaciones

---

## 💡 Consejos Útiles

### Para Desarrolladores

```bash
# Ejecutar con modo debug en Spotify Live
cd spotify_live
python3 app.py --debug

# Ver logs en tiempo real de Hydra Observer
tail -f logs/session_*.json

# Ejecutar ondads.py con diferentes configuraciones
# Edita las constantes al inicio del archivo:
# - N_BANDS: Número de bandas de frecuencia
# - BAR_HEIGHT: Altura de las barras
# - DURATION: Duración de cada bloque de audio
```

### Para Usuarios Avanzados

Crea un archivo `.env` en la raíz del proyecto:

```bash
# .env
SPOTIPY_CLIENT_ID=tu-client-id
SPOTIPY_CLIENT_SECRET=tu-client-secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
FLASK_SECRET=tu-secret-key
HYDRA_CLI=/path/to/hydra
HYDRA_USER_CONSENT=true
HYDRA_SLEEP_DURATION=2.0
```

Luego usa `python-dotenv` para cargar automáticamente:

```bash
pip install python-dotenv
```

```python
# En tu script
from dotenv import load_dotenv
load_dotenv()
```

---

## 🤝 Contribuir

¿Encontraste un bug o tienes una idea? ¡Abre un issue en GitHub!

¿Quieres contribuir código? ¡Los pull requests son bienvenidos!

---

## 📞 Soporte

Si tienes problemas que no están cubiertos en esta guía:

1. Revisa [TESTING.md](TESTING.md) para casos de prueba similares
2. Consulta las secciones de troubleshooting en cada README específico
3. Abre un issue en GitHub con detalles de tu problema

---

**¡Disfruta usando Rainvow! 🌈🎵**
