# Rainvow Tools

[![CI/CD Pipeline](https://github.com/Blackmvmba88/rainvow/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Blackmvmba88/rainvow/actions/workflows/ci-cd.yml)
[![Jekyll CI](https://github.com/Blackmvmba88/rainvow/actions/workflows/jekyll-docker.yml/badge.svg)](https://github.com/Blackmvmba88/rainvow/actions/workflows/jekyll-docker.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Este repositorio contiene utilidades de Python para efectos visuales y aplicaciones musicales interactivas.

## ✅ Estado del Proyecto

- **Sistema de Login y Registro**: ✅ Funcionando correctamente
- **Componentes Musicales Modulares**: ✅ Implementados exitosamente
- **Colaboración del Equipo**: ✅ Efectiva
- **Pruebas Básicas**: ✅ Completadas exitosamente
- **Documentación y Onboarding**: ✅ Mejorada y actualizada

Ver [CHANGELOG.md](CHANGELOG.md) para más detalles sobre las funcionalidades implementadas.

## 🚀 Inicio Rápido

### Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/Blackmvmba88/rainvow.git
cd rainvow

# Instalar dependencias
pip install -r requirements.txt

# Opción 1: Ejecutar el dashboard unificado (RECOMENDADO)
python3 dashboard.py
# Abre http://localhost:5000 en tu navegador

# Opción 2: Ejecutar el visualizador de audio en terminal
python3 ondads.py
```

**Para instrucciones detalladas**, consulta [QUICKSTART.md](QUICKSTART.md).

### Requisitos

- Python 3.8 o superior
- Micrófono (para visualizador de audio)
- Cuenta de Spotify Developer (para integración musical)

Ver [requirements.txt](requirements.txt) para la lista completa de dependencias.

## 🌈 Dashboard Unificado

**NUEVO**: Panel web centralizado para monitorear y controlar todos los componentes de Rainvow.

```bash
python3 dashboard.py
# Abre http://localhost:5000 en tu navegador
```

**Características del Dashboard:**
- 📊 Monitoreo en tiempo real de CPU y memoria
- 🎵 Visualizador de audio con barras de colores del arcoíris
- 🪟 Detección de ventana activa
- 🎧 Integración con Spotify Live
- ⌨️ Estado de RGB Keyboard
- 🔗 Enlaces rápidos a todos los demos y utilidades
- 🔄 Actualizaciones en vivo con WebSocket

Ver [DASHBOARD.md](DASHBOARD.md) para documentación completa y API REST.

## 📚 Documentación

### Documentos Principales

- **[QUICKSTART.md](QUICKSTART.md)**: 🚀 **¡Empieza aquí!** Guía de inicio rápido para nuevos usuarios
- **[DASHBOARD.md](DASHBOARD.md)**: 🌈 **Dashboard Unificado** - WebUI para ver y monitorear todos los componentes
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)**: Estado actual del proyecto, métricas y roadmap
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)**: Documentación completa de APIs y componentes reutilizables

### Documentos Técnicos

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Arquitectura modular del proyecto
- **[TESTING.md](TESTING.md)**: Pruebas realizadas y resultados
- **[CHANGELOG.md](CHANGELOG.md)**: Historial de cambios y funcionalidades implementadas

## `spotify_live/`
Aplicación web Flask que integra login/registro con Spotify OAuth.
Permite visualizar en tiempo real la canción que estás escuchando
y buscar canciones en el catálogo de Spotify.

**Características implementadas:**
- ✅ Sistema de autenticación OAuth con Spotify
- ✅ Gestión automática de tokens y sesiones
- ✅ Visualización de canción en reproducción
- ✅ Búsqueda de canciones con previsualizaciones
- ✅ Interfaz web responsive

Ver [spotify_live/README.md](spotify_live/README.md) para instrucciones de uso.

## `holi.py`
Saludo colorido animado que muestra "HOLI!" con colores del arcoíris.
Un pequeño script de bienvenida con el estilo visual del proyecto.

```bash
python3 holi.py
```

## `ondads.py`
Visualiza un arcoíris animado en la terminal sincronizado con el audio
capturado por el micrófono.

**Arquitectura modular:**
- ✅ Componentes separados y reutilizables
- ✅ Análisis de frecuencias independiente
- ✅ Fuente de audio configurable (micrófono o ruido de prueba)
- ✅ Sistema de ganancia adaptativa automática

## `keyboard_rgb.py`
Controla las luces de un teclado a través de
[OpenRGB](https://openrgb.org/). El script se conecta a un servidor
OpenRGB local o remoto y recorre los colores del arcoíris.

OpenRGB no tiene soporte nativo para macOS, por lo que puedes
ejecutarlo en otra máquina (Windows o Linux) o en una máquina virtual y
usar la opción `--host` para indicar su dirección.

### Requisitos
- Python 3
- `pip install openrgb-python`
- Un servidor OpenRGB ejecutándose con la opción `--server`.

### Uso
```bash
python keyboard_rgb.py --show --host 127.0.0.1
```
Interrumpe con `Ctrl+C` para apagar las luces.

## `hydra_observer.py`
Monitorea el sistema en tiempo real, detectando contextos de trabajo y 
registrando eventos del sistema. Puede detectar ventanas específicas
(como archivos ZIP o aplicaciones de música) y grabar audio cuando
se detecta contexto musical.

### Variables de Entorno
- `HYDRA_CLI`: Ruta al ejecutable de Hydra CLI (por defecto: "hydra")
- `USER_CONSENT`: Habilita/deshabilita el registro de teclas ("true"/"false", por defecto: "true")
- `SLEEP_DURATION`: Intervalo entre lecturas del sistema en segundos (por defecto: "2.0")

### Uso
```bash
# Con valores por defecto
python3 hydra_observer.py

# Con configuración personalizada
USER_CONSENT=false SLEEP_DURATION=5.0 python3 hydra_observer.py
```

Los logs se guardan en la carpeta `logs/` con formato JSON.
# Rainvow AR Demo

Este proyecto incluye una sencilla demostración de realidad aumentada con [A-Frame](https://aframe.io/) y [AR.js](https://ar-js-org.github.io/AR.js/). El archivo `ar.html` despliega un cubo 3D animado cuando la cámara detecta el marcador *hiro*.
Para hacerlo más visual, se integra [Hydra-synth](https://github.com/ojack/hydra) como capa de efectos sobre la escena.

## Cómo ejecutar

1. Inicia un servidor local en la raíz del proyecto. Por ejemplo:
   
   ```bash
   # Con Python
   python3 -m http.server
   
   # o con Node
   npx http-server
   ```
2. Abre `http://localhost:8000/ar.html` en un navegador moderno (Chrome, Firefox, Safari).
3. Concede permisos de cámara cuando lo solicite el navegador.
4. Apunta la cámara a un marcador *hiro*. Puedes imprimir uno desde [este enlace](https://raw.githubusercontent.com/AR-js-org/AR.js/master/data/images/HIRO.jpg).

Para que la cámara funcione, la página debe servirse mediante `https` o desde `localhost`.

## Requisitos

- Navegador con soporte WebGL y permisos de cámara.
- Conexión segura (HTTPS o entorno local) para acceder a la cámara.

Esta demo es autónoma y no necesita dependencias adicionales.

### Efecto Hydra

Al abrir `ar.html`, notarás una capa de patrones generativos. Estos efectos se generan con Hydra-synth y se mezclan sobre la imagen de la cámara para dar un aspecto más dinámico. Puedes modificar el código de Hydra en el archivo para experimentar con otros visuales.

### Lectura de PDFs con Hydra

También puedes abrir `pdf_overlay.html` para cargar un archivo PDF desde tu equipo. La página renderiza la primera página del documento y superpone una capa de efectos con Hydra-synth, ideal para resaltar pasos importantes o experimentar con anotaciones visuales.

1. Inicia el servidor como en el paso anterior.
2. Abre `http://localhost:8000/pdf_overlay.html`.
3. Selecciona un PDF local desde el control "Cargar PDF".

El efecto Hydra se puede modificar editando el código de la página para ajustar colores y animaciones.

### Capturas de pantalla

Si deseas guardar una imagen de tu escritorio para documentar tus experimentos, utiliza el script `screenshot.py`:

```bash
pip install pyautogui colorama
python3 screenshot.py --tag prueba
```

Las capturas se guardarán en la carpeta `screenshots` y el mensaje aparecerá resaltado en azul para mayor claridad.
