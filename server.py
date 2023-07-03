import json
import os

import openai
from dotenv import load_dotenv
from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
from loguru import logger
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
CORS(app)

REDIRECT_URI = 'http://localhost:8000/spotify-callback'
SCOPE = 'user-read-playback-state,user-modify-playback-state'

load_dotenv(dotenv_path="creds/.env")

auth_manager = SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
)


@app.route('/spotify-auth', methods=['GET'])
def spotify_auth():
    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)


@app.route('/spotify-callback', methods=['GET'])
def spotify_callback():
    code = request.args.get('code')
    token_info = auth_manager.get_access_token(code)
    return jsonify(access_token=token_info['access_token'])


@app.route("/generate-playlist", methods=['POST'])
def generate_playlist():
    # Get the OpenAI API key from the environment
    api_key = os.getenv("OPENAI_API_KEY")
    playlist_description = request.json.get('description')
    # Set the OpenAI API key
    openai.api_key = api_key

    # Construct the prompt for GPT-4
    prompt = f"""
{playlist_description}. Generate a list of 15 songs in the format of a JSON with song name and artist name:"
Use the following JSON format:
{{
    "playlist":
    [
        {{"song_name": "The long and winding road", "artist_name": "The Beatles"}},
        {{"song_name": "Sweet Child o' Mine", "artist_name": "Guns N' Roses"}},
    ]
}}
"""

    # Call the GPT-4 model to generate a response
    logger.info("Calling GPT")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",  # Set the model
        messages=[
            {"role": "system", "content": "You are a knowledgeable AI trained to generate music playlists."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the assistant's reply (assumes the reply is the last message)
    assistant_reply = response['choices'][0]['message']['content']

    # Parse JSON and return it
    playlist = json.loads(assistant_reply)

    return playlist


if __name__ == '__main__':
    app.run(port=8000)
