# Arquitectura del Proyecto Rainvow

## Resumen

Este documento describe la arquitectura modular implementada en los componentes musicales del proyecto Rainvow.

## Componentes Principales

### 1. Sistema de Login y Registro (Spotify Live)

**Ubicación**: `spotify_live/`

**Estado**: ✅ Funcionando correctamente

#### Arquitectura

El sistema utiliza una arquitectura web estándar con Flask:

```
spotify_live/
├── app.py              # Servidor Flask y rutas
└── templates/
    └── index.html      # Interfaz de usuario
```

#### Módulos Principales

##### `app.py`

**Función**: Servidor web y gestión de autenticación

**Componentes modulares**:

- `get_token()`: Gestión centralizada de tokens OAuth
  - Verifica validez del token
  - Renueva automáticamente tokens expirados
  - Mantiene sesión del usuario

- `@app.route('/login')`: Endpoint de autenticación
  - Redirige a Spotify para autorización
  - Implementa flujo OAuth estándar

- `@app.route('/callback')`: Callback OAuth
  - Recibe código de autorización
  - Intercambia código por token de acceso
  - Guarda token en sesión

- `@app.route('/current')`: API de canción actual
  - Consulta Spotify API
  - Retorna datos estructurados en JSON
  - Maneja errores de autenticación

- `@app.route('/search')`: API de búsqueda
  - Búsqueda en catálogo de Spotify
  - Retorna resultados formateados
  - Incluye previsualizaciones de audio

**Ventajas de la modularidad**:
- Fácil de extender con nuevas rutas
- Gestión de tokens centralizada
- Separación entre lógica y presentación

### 2. Visualizador de Audio Modular (ondads.py)

**Ubicación**: `ondads.py`

**Estado**: ✅ Modularidad implementada exitosamente

#### Arquitectura

Componentes separados y reutilizables:

```
ondads.py
├── get_band_amps()     # Análisis de frecuencias
├── audio_source()      # Captura de audio
└── run_visualizer()    # Renderizado visual
```

#### Módulos Principales

##### `get_band_amps(audio_block, fs, n_bands) -> np.ndarray`

**Función**: Análisis de frecuencias modulares

**Responsabilidades**:
- Aplica FFT al bloque de audio
- Separa espectro en bandas de frecuencia
- Calcula amplitud por banda
- Retorna array normalizado

**Ventajas**:
- Función pura sin efectos secundarios
- Fácilmente testeable
- Reutilizable en otros visualizadores

##### `audio_source() -> Generator`

**Función**: Fuente de audio configurable

**Responsabilidades**:
- Captura audio del micrófono
- Fallback automático a ruido de prueba
- Yield de bloques de audio

**Ventajas**:
- Abstracción de la fuente de audio
- Manejo robusto de errores
- Permite testing sin hardware de audio

##### `run_visualizer()`

**Función**: Loop principal de visualización

**Responsabilidades**:
- Consume bloques de audio
- Aplica ganancia adaptativa
- Renderiza barras de colores
- Anima el efecto arcoíris

**Ventajas**:
- Separación de concerns
- Fácil de modificar efectos visuales
- Independiente del análisis de audio

## Beneficios de la Arquitectura Modular

### 1. Mantenibilidad
- Cada módulo tiene una responsabilidad clara
- Fácil localizar y corregir bugs
- Actualizaciones aisladas sin efectos colaterales

### 2. Reutilización
- `get_band_amps()` puede usarse en otros proyectos
- `audio_source()` es reutilizable en cualquier aplicación de audio
- Componentes de login pueden adaptarse a otras APIs

### 3. Testing
- Funciones puras fáciles de testear
- Mock de fuentes de audio para testing
- Tests unitarios independientes

### 4. Extensibilidad
- Agregar nuevas rutas en Spotify Live
- Crear nuevos efectos visuales
- Integrar nuevas fuentes de audio

## Ejemplos de Extensión

### Agregar nueva funcionalidad en Spotify Live

```python
@app.route('/playlists')
def playlists():
    token = get_token()  # Reutiliza gestión de tokens
    if not token:
        return jsonify({'error': 'not_authenticated'}), 401
    sp = spotipy.Spotify(auth=token)
    playlists = sp.current_user_playlists()
    # ... procesar y retornar
```

### Crear nuevo visualizador usando componentes existentes

```python
def custom_visualizer():
    for audio_block in audio_source():  # Reutiliza fuente de audio
        amps = get_band_amps(audio_block, FS, N_BANDS)  # Reutiliza análisis
        # ... tu lógica de visualización personalizada
```

## Conclusión

La arquitectura modular implementada proporciona una base sólida para:
- ✅ Mantener y evolucionar el código
- ✅ Reutilizar componentes en otros proyectos
- ✅ Facilitar la colaboración del equipo
- ✅ Realizar pruebas de forma efectiva

Esta modularidad fue clave para el éxito del proyecto y la efectividad de la colaboración del equipo.
