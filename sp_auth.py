# Spotify authorization
import os
import webbrowser

from dotenv import load_dotenv
from flask import Flask, request
from spotipy import SpotifyOAuth
from termcolor import colored

from config import DATA_PATH, ACCESS_TOKEN_FILE, ENV_FILE

app = Flask(__name__)

scope = "user-read-playback-state,user-modify-playback-state,playlist-modify-public,streaming user-modify-playback-state"

load_dotenv(dotenv_path=ENV_FILE)
sp_oauth = SpotifyOAuth(client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                        redirect_uri='http://localhost:8888/callback',
                        scope=scope)


def run_flow():
    auth_url = sp_oauth.get_authorize_url()
    webbrowser.open(auth_url)
    app.run(port=8888)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    # Use the code to request an access token
    token_info = sp_oauth.get_access_token(code)
    # Perform further operations with the access token
    access_token = token_info['access_token']

    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
    with open(ACCESS_TOKEN_FILE, 'w') as f:
        f.write(access_token)

    print(colored('Authorization successful!', 'green', attrs=['bold']))
    print(colored('You can now close this window and run playlister.py again', 'green', attrs=['bold']))
    return 'Authorization successful!'


if __name__ == '__main__':
    run_flow()
