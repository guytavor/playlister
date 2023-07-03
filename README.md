Playlister.ai
-------------

Hi there! Playlister.ai is an very simple command-line tool that
helps you generate and play Spotify playlists using ChatGPT.

During my journey of learning a new language, I had a preference for
instrumental electronic music, specifically the kind that aids concentration .

I used ChatGPT to recommend a suitable playlist based on my preference.
And was looking for a way to find a convenient method to import this list into
Spotify.
So here we are.

### Implementation details

* Playlister.ai saves all the previous playlists under ~/.playlister.ai
* Each playlist that's generated by ChatGPT is saved as a Spotify playlist

### Installation

* Create a `.env` file under `~/.playlister.ai` with the following contents:

```
SPOTIFY_USERNAME="<your spotify username string>"
SPOTIFY_CLIENT_ID="<spotify client id>"
SPOTIFY_CLIENT_SECRET="<spotify client secret>"
OPENAI_API_KEY="<openai api key>"
```

* Make sure you have the spotify player installed on your Mac, and that you are logged-in
* Run py sp_auth.py to authorize the app to access your Spotify account.
* Run playlister.py 


