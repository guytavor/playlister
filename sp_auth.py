# Spotify authorization
import os

from dotenv import load_dotenv
from flask import Flask, request
from spotipy import SpotifyOAuth
from termcolor import colored

redirect_uri = "http://localhost"  # os.getenv("SPOTIFY_REDIRECT_URI")
scope = "user-read-playback-state,user-modify-playback-state"

load_dotenv(dotenv_path="creds/.env")

sp_oauth = SpotifyOAuth(client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                        redirect_uri='http://localhost:8888/callback',
                        scope=scope)

auth_url = sp_oauth.get_authorize_url()
print(colored(f'Please visit this URL to authorize the app: {auth_url}', 'yellow', attrs=['bold']))

app = Flask(__name__)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    # Use the code to request an access token
    token_info = sp_oauth.get_access_token(code)
    # Perform further operations with the access token
    access_token = token_info['access_token']

    if not os.path.exists('creds'):
        os.makedirs('creds')
    with open('creds/access_token.txt', 'w') as f:
        f.write(access_token)

    print(colored('Authorization successful!', 'green', attrs=['bold']))
    print(colored('You can now close this window and run playlister.py', 'green', attrs=['bold']))
    return 'Authorization successful!'


if __name__ == '__main__':
    app.run(port=8888)
