import vlc

class VLCController:
    def __init__(self):
        self.instance = vlc.Instance("--quiet")
        self.player = self.instance.media_player_new()

    def play_song(self, path):
        media = self.instance.media_new(path)
        self.player.set_media(media)
        self.player.play()

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def is_playing(self):
        return self.player.is_playing()

    def set_time(self, ms):
        self.player.set_time(ms)

    def get_length(self):
        return self.player.get_length()

    def get_time(self):
        return self.player.get_time()

    def get_state(self):
        state = self.player.get_state()
        return str(state).split('.')[-1]