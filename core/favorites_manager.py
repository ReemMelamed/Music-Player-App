import os
import json
import sys

FAVORITES_FILE = os.path.join(sys.path[0], "favorites.txt")

class FavoritesManager:
    def __init__(self):
        self.favorites_file = FAVORITES_FILE
        self.favorites = set()
        self.load_favorites()

    def load_favorites(self):
        if os.path.exists(self.favorites_file):
            with open(self.favorites_file, "r", encoding="utf-8") as f:
                self.favorites = set(json.load(f))

    def save_favorites(self):
        with open(self.favorites_file, "w", encoding="utf-8") as f:
            json.dump(list(self.favorites), f, ensure_ascii=False)

    def add(self, song):
        self.favorites.add(song)
        self.save_favorites()

    def remove(self, song):
        self.favorites.discard(song)
        self.save_favorites()

    def is_favorite(self, song):
        return song in self.favorites