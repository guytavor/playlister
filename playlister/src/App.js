import React, { useEffect, useState } from "react";
import axios from "axios";
import PlaylistForm from "./PlaylistForm";
import SpotifyPlayer from "react-spotify-web-playback";

function App() {
  const [token, setToken] = useState(null); // user's Spotify access token
  const [playlist, setPlaylist] = useState([]);
  const [currentTrackUri, setCurrentTrackUri] = useState(null);

  useEffect(() => {
    // Assuming that there is a route on your server to authenticate a user and get their Spotify access token
    const getToken = async () => {
      const response = await axios.get("http://localhost:8000/spotify-auth");
      setToken(response.data.access_token);
    };

    getToken();
  }, []);

  const handleSubmit = async (description) => {
    const response = await axios.post("http://localhost:8000/generate-playlist", { description });
    setPlaylist(response.data.playlist);
    // Assuming that each song in the playlist has a "spotify_uri" property
    setCurrentTrackUri(response.data.playlist[0].spotify_uri);
  };

  const handlePlaybackEnd = () => {
    const currentSongIndex = playlist.findIndex((song) => song.spotify_uri === currentTrackUri);
    setCurrentTrackUri(playlist[currentSongIndex + 1]?.spotify_uri || null);
  };

  return (
    <div>
      <PlaylistForm onSubmit={handleSubmit} />
      {token && currentTrackUri && (
        <SpotifyPlayer
          token={token}
          uris={[currentTrackUri]}
          play
          callback={({ status }) => {
            if (status === "song-end") handlePlaybackEnd();
          }}
        />
      )}
    </div>
  );
}

export default App;
