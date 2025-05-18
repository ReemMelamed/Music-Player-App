from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMessageBox, QListWidgetItem

# Event handling for MusicPlayer

class PlayerEvents:
    def __init__(self, parent):
        self.parent = parent
        self._setup_shortcuts()
        self._connect_events()
        self.timer = QTimer(self.parent)
        self.timer.timeout.connect(self.parent.update_ui)
        self.timer.start(1000)
        self.parent.load_songs()

    def _setup_shortcuts(self):
        QShortcut(QKeySequence("Space"), self.parent, self.parent.toggle_play_pause)
        QShortcut(QKeySequence("S"), self.parent, self.parent.toggle_play_pause)
        QShortcut(QKeySequence("Right"), self.parent, self.parent.next_song)
        QShortcut(QKeySequence("D"), self.parent, self.parent.next_song)
        QShortcut(QKeySequence("Left"), self.parent, self.parent.prev_song)
        QShortcut(QKeySequence("A"), self.parent, self.parent.prev_song)
        QShortcut(QKeySequence("Up"), self.parent, self.parent.toggle_repeat)
        QShortcut(QKeySequence("W"), self.parent, self.parent.toggle_repeat)
        QShortcut(QKeySequence("Down"), self.parent, self.parent.toggle_shuffle)
        QShortcut(QKeySequence("F"), self.parent, lambda: self.parent.search_bar.setFocus())
        QShortcut(QKeySequence("H"), self.parent, self.parent.show_shortcuts_help)

    def _connect_events(self):
        self.parent.search_bar.textChanged.connect(self.parent.filter_songs)
        self.parent.song_list.itemDoubleClicked.connect(self.parent.song_double_clicked)
        self.parent.seek_slider.sliderMoved.connect(self.parent.seek_song)
