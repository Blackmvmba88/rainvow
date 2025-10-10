# Spotify Live

✅ **Estado: Sistema de login y registro funcionando correctamente**

Esta miniaplicación permite mostrar en vivo la canción que estás escuchando en tu cuenta de Spotify y buscar otras canciones.

## Funcionalidades Implementadas

- ✅ **Autenticación OAuth 2.0**: Sistema completo de login con Spotify
- ✅ **Gestión de Sesiones**: Tokens persistentes con renovación automática
- ✅ **Visualización en Tiempo Real**: Muestra la canción actual con carátula
- ✅ **Búsqueda de Canciones**: Explora el catálogo de Spotify
- ✅ **Previsualizaciones de Audio**: Escucha fragmentos de las canciones

## Requisitos

- Python 3
- `pip install flask spotipy`
- Una aplicación de Spotify registrada en <https://developer.spotify.com/>

Configura las siguientes variables de entorno:

```bash
export SPOTIPY_CLIENT_ID="tu-client-id"
export SPOTIPY_CLIENT_SECRET="tu-client-secret"
export SPOTIPY_REDIRECT_URI="http://localhost:8888/callback"
export FLASK_SECRET="alguna-clave"
```

## Uso

1. Ejecuta el servidor:

```bash
python3 app.py
```

2. Abre <http://localhost:8888> en tu navegador.
3. Inicia sesión con tu cuenta de Spotify.
4. La página mostrará la canción que estás reproduciendo y podrás buscar otras canciones para escucharlas.

La vista es sencilla pero puedes personalizarla editando `templates/index.html`.
