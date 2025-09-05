# Spotify Live

Esta miniaplicación permite mostrar en vivo la canción que estás escuchando en tu cuenta de Spotify y buscar otras canciones.

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
