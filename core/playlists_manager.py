import os
import json
import sys

PLAYLISTS_FILE = os.path.join(sys.path[0], "playlists.json")

class PlaylistsManager:
    def __init__(self):
        self.playlists_file = PLAYLISTS_FILE

    def load_playlists(self):
        if not os.path.exists(PLAYLISTS_FILE):
            return []
        with open(self.playlists_file, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def save_playlists(self, playlists):
        with open(self.playlists_file, "w", encoding="utf-8") as f:
            json.dump(playlists, f, ensure_ascii=False, indent=2)

    def add_to_playlist(self, song, playlist_name):
        playlists = self.load_playlists()
        for pl in playlists:
            if pl["name"] == playlist_name:
                if song not in pl["songs"]:
                    pl["songs"].append(song)
                break
        else: 
            playlists.append({"name": playlist_name, "songs": [song]})
        self.save_playlists(playlists)

    def remove_from_playlist(self, song, playlist_name):
        playlists = self.load_playlists()
        for pl in playlists:
            if pl["name"] == playlist_name and song in pl["songs"]:
                pl["songs"].remove(song)
                break
        self.save_playlists(playlists)