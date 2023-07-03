import json
import os

import openai
import spotipy
from loguru import logger
from spotipy.oauth2 import SpotifyOAuth


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
    # Spotify credentials

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(username=username,
                                                   scope=scope,
                                                   client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri))
    return sp


def play_playlist(sp, playlist):
    playlist = \
        """
{
    "playlist": [
        {
            "song_name": "The long and winding road",
            "artist_name": "The Beatles"
        },
        {
            "song_name": "Sweet Child o' Mine",
            "artist_name": "Guns N' Roses"
        },
        {
            "song_name": "Bohemian Rhapsody",
            "artist_name": "Queen"
        },
        {
            "song_name": "Hotel California",
            "artist_name": "Eagles"
        },
        {
            "song_name": "Imagine",
            "artist_name": "John Lennon"
        },
        {
            "song_name": "Hey Jude",
            "artist_name": "The Beatles"
        },
        {
            "song_name": "Stairway to Heaven",
            "artist_name": "Led Zeppelin"
        },
        {
            "song_name": "Smells Like Teen Spirit",
            "artist_name": "Nirvana"
        },
        {
            "song_name": "Wonderwall",
            "artist_name": "Oasis"
        },
        {
            "song_name": "Like a Rolling Stone",
            "artist_name": "Bob Dylan"
        },
        {
            "song_name": "Yesterday",
            "artist_name": "The Beatles"
        },
        {
            "song_name": "Black or White",
            "artist_name": "Michael Jackson"
        },
        {
            "song_name": "A Day in the Life",
            "artist_name": "The Beatles"
        },
        {
            "song_name": "Boys Don't Cry",
            "artist_name": "The Cure"
        },
        {
            "song_name": "Livin' on a Prayer",
            "artist_name": "Bon Jovi"
        }
    ]
}"""
    track_uris = []

    # Parse the JSON input
    playlist = json.loads(playlist)

    # Fetch URIs of the tracks
    for track in playlist["playlist"]:
        results = sp.search(q='track:{} artist:{}'.format(track['song_name'], track['artist_name']), type='track')
        if results['tracks']['items']:
            track_uris.append(results['tracks']['items'][0]['uri'])

    # Start playback
    if track_uris:
        sp.start_playback(uris=track_uris)


def pause():
    sp.pause_playback()


def resume():
    sp.start_playback()


def next_track():
    sp.next_track()


def previous_track():
    sp.previous_track()


def main():
    sp = setup_spotify()

    # # Ask the user for their desired playlist
    # playlist_description = input("Enter a description for the playlist you want: ")
    #
    # # Generate the playlist and print it
    # playlist = generate_playlist(playlist_description)
    # print(json.dumps(playlist, indent=4))
    play_playlist(sp, "")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
