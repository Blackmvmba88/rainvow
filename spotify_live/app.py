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
    token_info = session.get('token_info')
    if token_info and not sp_oauth.is_token_expired(token_info):
        return token_info['access_token']
    if token_info and sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info
        return token_info['access_token']
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
    token = get_token()
    if not token:
        return jsonify({'error': 'not_authenticated'}), 401
    sp = spotipy.Spotify(auth=token)
    track = sp.current_user_playing_track()
    if track and track.get('item'):
        item = track['item']
        return jsonify({
            'name': item['name'],
            'artists': ', '.join(a['name'] for a in item['artists']),
            'album': item['album']['name'],
            'image': item['album']['images'][0]['url'] if item['album']['images'] else None,
            'preview': item['preview_url']
        })
    else:
        return jsonify({'error': 'no_track'})

@app.route('/search')
def search():
    token = get_token()
    if not token:
        return jsonify({'error': 'not_authenticated'}), 401
    query = request.args.get('q', '')
    if not query:
        return jsonify({'results': []})
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
    return jsonify({'results': tracks})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
