# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

## [No publicado] - 2025-10-10

### Completado

#### Sistema de Login y Registro
- ✅ El sistema de login con Spotify funciona correctamente
- ✅ Autenticación OAuth implementada con Spotify API
- ✅ Gestión de tokens con renovación automática
- ✅ Sesiones persistentes para usuarios autenticados
- ✅ Rutas protegidas para usuarios no autenticados

#### Componentes Musicales Modulares
- ✅ Implementada la modularidad en los componentes de visualización de audio
- ✅ Separación de responsabilidades:
  - Función `get_band_amps()` para análisis de frecuencias
  - Función `audio_source()` para captura de audio
  - Función `run_visualizer()` para renderizado visual
- ✅ Visualizador de audio en tiempo real con ondas de colores del arcoíris
- ✅ Sistema de ganancia adaptativa por banda de frecuencia

#### Colaboración del Equipo
- ✅ La colaboración del equipo fue efectiva
- ✅ Integración exitosa de múltiples componentes del proyecto

#### Pruebas
- ✅ Las pruebas básicas fueron exitosas
- ✅ Sistema de login verificado manualmente
- ✅ Visualizador de audio validado con entrada de micrófono
- ✅ Componentes modulares funcionando correctamente

### Detalles Técnicos

#### Spotify Live (`spotify_live/`)
El sistema incluye:
- Flask web server
- Integración con Spotify API vía spotipy
- Autenticación OAuth 2.0
- Interfaz web para visualizar canciones en reproducción
- Búsqueda de canciones con previsualizaciones de audio

#### Visualizador de Audio (`ondads.py`)
El visualizador incluye:
- Captura de audio en tiempo real con sounddevice
- Análisis FFT para separación de bandas de frecuencia
- Renderizado con rich console
- Sistema de ganancia adaptativa automática
- Animación de colores del arcoíris

## Próximos Pasos

- Añadir pruebas unitarias automatizadas
- Documentar APIs de los componentes modulares
- Expandir funcionalidad de búsqueda en Spotify Live
- Optimizar rendimiento del visualizador de audio
