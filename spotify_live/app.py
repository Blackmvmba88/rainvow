import os
from flask import Flask, redirect, request, session, url_for, jsonify, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'change-me')

CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI', 'http://localhost:8888/callback')
SCOPE = 'user-read-currently-playing'

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=SCOPE)

def get_token():
    """Obtiene y gestiona el token de acceso de Spotify.
    
    Implementa renovación automática de tokens expirados para mantener
    la sesión del usuario sin interrupciones.
    
    Returns:
        str: Token de acceso válido o None si no hay sesión activa.
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
    token = get_token()
    logged_in = token is not None
    return render_template('index.html', logged_in=logged_in)

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('index'))

@app.route('/current')
def current():
    """Obtiene la canción actualmente en reproducción.
    
    Returns:
        JSON con datos de la canción o error si no está autenticado/no hay canción.
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

@app.route('/search')
def search():
    """Busca canciones en el catálogo de Spotify.
    
    Query Parameters:
        q (str): Término de búsqueda
        limit (int): Número máximo de resultados (default: 5, max: 20)
    
    Returns:
        JSON con lista de canciones encontradas o error.
    """
    token = get_token()
    if not token:
        return jsonify({'error': 'not_authenticated'}), 401
    
    # Validación y sanitización de parámetros
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'results': []})
    
    # Límite configurable con máximo de 20 para no sobrecargar
    try:
        limit = min(int(request.args.get('limit', 5)), 20)
    except ValueError:
        limit = 5
    
    try:
        sp = spotipy.Spotify(auth=token)
        # Consulta optimizada con límite configurable
        results = sp.search(q=query, type='track', limit=limit)
        
        tracks = []
        for item in results.get('tracks', {}).get('items', []):
            # Validación defensiva de cada item
            artists = [a.get('name', 'Unknown') for a in item.get('artists', [])]
            album = item.get('album', {})
            images = album.get('images', [])
            
            tracks.append({
                'name': item.get('name', 'Unknown'),
                'artists': ', '.join(artists) if artists else 'Unknown Artist',
                'image': images[0].get('url') if images else None,
                'preview': item.get('preview_url')
            })
        
        return jsonify({'results': tracks})
    except spotipy.exceptions.SpotifyException as e:
        # Manejo específico de errores de Spotify API
        return jsonify({'error': 'spotify_api_error', 'message': str(e)}), 503
    except Exception as e:
        # Manejo de errores generales
        return jsonify({'error': 'internal_error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
