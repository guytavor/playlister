import json
import os

import openai
import spotipy
from loguru import logger


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


def setup_spotify():
    # Read access token from creds/access_token.txt
    with open("creds/access_token.txt", "r") as f:
        access_token = f.read()
        return spotipy.Spotify(auth=access_token)


def play_playlist(sp, playlist):
    track_uris = []

    # Fetch URIs of the tracks
    for track in playlist["playlist"]:
        results = sp.search(q='track:{} artist:{}'.format(track['song_name'], track['artist_name']), type='track')
        if results['tracks']['items']:
            track_uris.append(results['tracks']['items'][0]['uri'])

    # List available devices
    devices = sp.devices()
    for i, device in enumerate(devices['devices']):
        print(f"{i + 1}: {device['name']} ({device['id']})")

    # Let the user select a device
    device_index = int(input("Select a device by number: ")) - 1
    device_id = devices['devices'][device_index]['id']

    # Start playback on the selected device
    if track_uris:
        sp.start_playback(device_id=device_id, uris=track_uris)


def main():
    sp = setup_spotify()
    devices = sp.devices()

    # Ask the user for their desired playlist
    playlist_description = input("Enter a description for the playlist you want: ")

    # Generate the playlist and print it
    playlist = generate_playlist(playlist_description)
    play_playlist(sp, playlist)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
