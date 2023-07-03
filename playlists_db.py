import json
import os
import re
from collections import deque


class PlaylistManager:
    def __init__(self, directory, max_playlists=10):
        self.directory = directory
        self.max_playlists = max_playlists
        self.recent_playlists = deque(maxlen=max_playlists)

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.load_recent_playlists()

    def sanitize_name(self, name):
        return re.sub(r'\W+', '_', name)

    def save_playlist(self, playlist_name, playlist_data):
        sanitized_name = self.sanitize_name(playlist_name)
        file_path = os.path.join(self.directory, sanitized_name + ".json")
        with open(file_path, 'w') as f:
            json.dump(playlist_data, f)

        if len(self.recent_playlists) == self.max_playlists:
            oldest_playlist = self.recent_playlists.popleft()
            os.remove(os.path.join(self.directory, self.sanitize_name(oldest_playlist) + ".json"))

        self.recent_playlists.append(playlist_name)

        self.save_recent_playlists()

    def list_playlists(self):
        return list(self.recent_playlists)

    def load_playlist(self, index):
        if index < 0 or index >= len(self.recent_playlists):
            return None

        playlist_name = self.recent_playlists[index]
        file_path = os.path.join(self.directory, self.sanitize_name(playlist_name) + ".json")

        with open(file_path, 'r') as f:
            playlist_data = json.load(f)

        return playlist_data

    def load_recent_playlists(self):
        try:
            with open(os.path.join(self.directory, "recent_playlists.json"), 'r') as f:
                self.recent_playlists = deque(json.load(f), self.max_playlists)
        except FileNotFoundError:
            pass

    def save_recent_playlists(self):
        with open(os.path.join(self.directory, "recent_playlists.json"), 'w') as f:
            json.dump(list(self.recent_playlists), f)
