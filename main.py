import json
import os
import subprocess

import openai
import spotipy
from termcolor import colored

TOKEN_FILE = "creds/access_token.txt"


def generate_playlist(playlist_description):
    # Get the OpenAI API key from the environment
    api_key = os.getenv("OPENAI_API_KEY")

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


def setup_spotify():
    # Read access token from creds/access_token.txt
    with open(TOKEN_FILE, "r") as f:
        access_token = f.read()
        return spotipy.Spotify(auth=access_token)


def play_playlist(sp, playlist, device_id):
    track_uris = []

    # Fetch URIs of the tracks
    for track in playlist["playlist"]:
        results = sp.search(q='track:{} artist:{}'.format(track['song_name'], track['artist_name']), type='track')
        if results['tracks']['items']:
            track_uris.append(results['tracks']['items'][0]['uri'])

    # Start playback on the selected device
    if track_uris:
        sp.start_playback(device_id=device_id, uris=track_uris)


def main():
    # if token file does not exist
    if not os.path.exists(TOKEN_FILE):
        print(colored("Please run sp_auth.py first to authenticate with Spotify", "red", attrs=["bold"]))
        exit(1)
    sp = setup_spotify()

    # Ask the user for their desired playlist
    playlist_description = input("Enter a description for the playlist you want:\n")

    print(colored("Opening your spotify desktop app", "yellow", attrs=["bold"]))
    command = "/Applications/Spotify.app/Contents/MacOS/Spotify"
    subprocess.Popen(command)

    print(colored("Generating playlist...", "yellow", attrs=["bold"]))
    playlist = generate_playlist(playlist_description)

    print(colored("Playlist generated:", "green"))
    text_list = playlist_json_to_text(playlist)
    print(colored(text_list, "yellow"))

    devices = sp.devices()
    device_id = devices['devices'][0]['id']  # get the first device

    print(colored("\n\nPlaying...", "yellow", attrs=["bold"]))

    play_playlist(sp, playlist, device_id)


def playlist_json_to_text(playlist):
    text_list = ""
    for i, song in enumerate(playlist["playlist"], start=1):
        text_list += f"{i}. {song['song_name']} by {song['artist_name']}\n"
    return text_list


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
