"""Aplicación web Flask para integración con Spotify.

Esta aplicación proporciona autenticación OAuth con Spotify y permite
visualizar la canción que se está reproduciendo actualmente, además de
buscar canciones en el catálogo de Spotify.

Características:
    - Sistema de autenticación OAuth 2.0 con Spotify
    - Gestión automática de tokens con renovación
    - Visualización de canción actual en reproducción
    - Búsqueda de canciones con caché para optimización
    - API REST para integración con frontends

Variables de entorno requeridas:
    SPOTIPY_CLIENT_ID: Client ID de Spotify Developer Dashboard
    SPOTIPY_CLIENT_SECRET: Client Secret de Spotify Developer Dashboard
    SPOTIPY_REDIRECT_URI: URI de callback (default: http://localhost:8888/callback)
    FLASK_SECRET: Secreto para sesiones Flask (default: 'change-me')

Uso:
    python3 app.py

El servidor escucha en http://0.0.0.0:8888
"""

import os
import time
import threading
from flask import Flask, redirect, request, session, url_for, jsonify, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'change-me')

# Caché thread-safe para optimizar búsquedas repetidas
# Estructura: {query: {'results': [...], 'timestamp': time.time()}}
SEARCH_CACHE = {}
CACHE_EXPIRY_SECONDS = 300  # 5 minutos
CACHE_MAX_SIZE = 100  # Máximo de entradas en caché
cache_lock = threading.Lock()  # Lock para acceso thread-safe

CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI', 'http://localhost:8888/callback')
SCOPE = 'user-read-currently-playing'

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=SCOPE)


def get_token():
    """Obtiene un token de acceso válido de Spotify desde la sesión.

    Verifica si existe un token en la sesión, comprueba su validez,
    y lo renueva automáticamente si está expirado usando el refresh token.

    Returns:
        str or None: Token de acceso válido, o None si no hay sesión activa

    Note:
        Esta función centraliza la lógica de gestión de tokens OAuth,
        facilitando el mantenimiento y reduciendo código duplicado.
    """
    token_info = session.get('token_info')
    if token_info and not sp_oauth.is_token_expired(token_info):
        return token_info['access_token']
    if token_info and sp_oauth.is_token_expired(token_info):
        try:
            # Renovación automática del token usando refresh_token
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info
            return token_info['access_token']
        except Exception:
            # Si falla la renovación, limpiar sesión
            session.pop('token_info', None)
            return None
    return None


@app.route('/')
def index():
    """Página principal de la aplicación.

    Muestra la interfaz de usuario y pasa el estado de autenticación
    al template para mostrar/ocultar elementos según corresponda.
    """
    token = get_token()
    logged_in = token is not None
    return render_template('index.html', logged_in=logged_in)


@app.route('/login')
def login():
    """Inicia el flujo de autenticación OAuth con Spotify.

    Redirige al usuario a la página de autorización de Spotify
    donde puede dar permisos a la aplicación.
    """
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/callback')
def callback():
    """Procesa el callback de OAuth después de la autorización.

    Spotify redirige aquí después de que el usuario autoriza la app.
    Intercambia el código de autorización por tokens de acceso
    y los guarda en la sesión del usuario.
    """
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('index'))


@app.route('/current')
def current():
    """API endpoint que retorna información de la canción actual.

    Consulta la API de Spotify para obtener la canción que el usuario
    está reproduciendo en este momento.

    Returns:
        JSON con datos de la canción (nombre, artistas, álbum, imagen, preview)
        o error si no hay autenticación o no hay canción reproduciéndose

    Status Codes:
        200: Canción encontrada y retornada exitosamente
        401: No autenticado
    """
    token = get_token()
    if not token:
        return jsonify({'error': 'not_authenticated'}), 401

    try:
        sp = spotipy.Spotify(auth=token)
        # Consulta optimizada: solo obtiene campos necesarios
        track = sp.current_user_playing_track()

        if track and track.get('item'):
            item = track['item']
            # Validación defensiva de datos
            artists = [a.get('name', 'Unknown') for a in item.get('artists', [])]
            album = item.get('album', {})
            images = album.get('images', [])

            return jsonify({
                'name': item.get('name', 'Unknown'),
                'artists': ', '.join(artists) if artists else 'Unknown Artist',
                'album': album.get('name', 'Unknown Album'),
                'image': images[0].get('url') if images else None,
                'preview': item.get('preview_url')
            })
        else:
            return jsonify({'error': 'no_track'})
    except spotipy.exceptions.SpotifyException as e:
        # Manejo específico de errores de Spotify API
        return jsonify({'error': 'spotify_api_error', 'message': str(e)}), 503
    except Exception as e:
        # Manejo de errores generales
        return jsonify({'error': 'internal_error', 'message': str(e)}), 500


def _clean_expired_cache_unsafe():
    """Limpia entradas expiradas del caché sin adquirir el lock.

    ADVERTENCIA: Esta función debe ser llamada solo cuando cache_lock ya está adquirido.
    No es thread-safe por sí sola.
    """
    global SEARCH_CACHE
    now = time.time()
    SEARCH_CACHE = {k: v for k, v in SEARCH_CACHE.items()
                    if now - v['timestamp'] < CACHE_EXPIRY_SECONDS}


@app.route('/search')
def search():
    """API endpoint para búsqueda de canciones en Spotify.

    Busca canciones en el catálogo de Spotify usando el query proporcionado
    y retorna los primeros 5 resultados con información relevante.

    Implementa caché thread-safe en memoria para optimizar búsquedas repetidas,
    reduciendo llamadas innecesarias a la API de Spotify. El caché tiene límite
    de tamaño y limpieza automática de entradas expiradas.

    Query Parameters:
        q: Término de búsqueda

    Returns:
        JSON con array de resultados, cada uno con nombre, artistas, imagen y preview

    Status Codes:
        200: Búsqueda exitosa (puede tener 0 resultados)
        401: No autenticado
    """
    token = get_token()
    if not token:
        return jsonify({'error': 'not_authenticated'}), 401

    query = request.args.get('q', '')
    if not query:
        return jsonify({'results': []})

    # Verificar caché primero (thread-safe)
    query_lower = query.lower()
    with cache_lock:
        if query_lower in SEARCH_CACHE:
            cached = SEARCH_CACHE[query_lower]
            # Verificar si el caché no ha expirado
            if time.time() - cached['timestamp'] < CACHE_EXPIRY_SECONDS:
                return jsonify({'results': cached['results'], 'cached': True})

        # Limpiar caché si ha crecido demasiado
        if len(SEARCH_CACHE) >= CACHE_MAX_SIZE:
            _clean_expired_cache_unsafe()
            # Si aún está lleno después de limpiar, remover la entrada más antigua
            if len(SEARCH_CACHE) >= CACHE_MAX_SIZE:
                oldest_key = min(SEARCH_CACHE.keys(),
                                 key=lambda k: SEARCH_CACHE[k]['timestamp'])
                del SEARCH_CACHE[oldest_key]

    # Si no hay caché válido, consultar Spotify API
    sp = spotipy.Spotify(auth=token)
    results = sp.search(q=query, type='track', limit=5)
    tracks = []
    for item in results['tracks']['items']:
        tracks.append({
            'name': item['name'],
            'artists': ', '.join(a['name'] for a in item['artists']),
            'image': item['album']['images'][0]['url'] if item['album']['images'] else None,
            'preview': item['preview_url']
        })

    # Guardar en caché (thread-safe)
    with cache_lock:
        SEARCH_CACHE[query_lower] = {
            'results': tracks,
            'timestamp': time.time()
        }

    return jsonify({'results': tracks, 'cached': False})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
