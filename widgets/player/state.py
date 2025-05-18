# State management for MusicPlayer

class PlayerState:
    def __init__(self, parent):
        self.parent = parent
        self.current_song_index = 0
        self.repeat_mode = "none"
        self.shuffle = False
        self.is_paused = False
        # Add more state variables as needed
