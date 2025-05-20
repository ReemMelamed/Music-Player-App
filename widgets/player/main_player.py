# Main player logic and UI for the music player app
# This is the central widget that manages playback, playlists, favorites, and all user interactions
import sys
import os
import random
import json
import vlc
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QInputDialog, QHBoxLayout, QLabel, QFrame, QSplitter, QLineEdit, QMessageBox, QListWidgetItem
)
from widgets.slider import ClickableSlider
from widgets.controls import create_controls
from widgets.sidebar import create_sidebar
from core.playlists_manager import PlaylistsManager

# All mp3 files should be placed in this directory
SONGS_DIR = os.path.join(sys.path[0], "songs")

class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        # Window setup
        self.setWindowTitle("Re'em - Music Player")
        self.setMinimumSize(700, 420)
        # Favorites management
        self.favorites = set()
        self.favorites_file = os.path.join(sys.path[0], "favorites.txt")
        self.load_favorites()
        # Playlist manager
        self.playlists_manager = PlaylistsManager()
        # Playback state
        self.current_song_index = 0
        self.repeat_mode = "none"
        self.shuffle = False
        self.is_paused = False
        # VLC setup
        self.instance = vlc.Instance("--quiet")
        self.player = self.instance.media_player_new()
        # App stylesheet
        self.dark_stylesheet = """
            QWidget { background: #0A2239; color: #FFD700; }
            QLineEdit { background: #164B74; color: #FFD700; border-radius: 8px; padding: 6px; font-size: 16px; }
            QLabel#NowPlaying { color: #00BFFF; font-size: 22px; font-weight: bold; }
            QListWidget { background: #164B74; color: #FFD700; border-radius: 12px; }
            QListWidget::item:selected { background: #FFD700; color: #00BFFF; font-weight: bold; }
            QSlider::groove:horizontal { background: #1565C0; height: 8px; border-radius: 4px; }
            QSlider::handle:horizontal { background: #FFD700; width: 18px; border-radius: 9px; }
            QPushButton { border: none; }
        """
        self.setStyleSheet(self.dark_stylesheet)
        self._setup_ui()
        self._setup_shortcuts()
        # UI update timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000)
        self.load_songs()

        self.active_playlist_songs = None
        self.active_playlist_index = None

    def _setup_shortcuts(self):
        # Keyboard shortcuts for all main actions
        QShortcut(QKeySequence("Space"), self, self.toggle_play_pause)
        QShortcut(QKeySequence("S"), self, self.toggle_play_pause)
        QShortcut(QKeySequence("Right"), self, self.next_song)
        QShortcut(QKeySequence("D"), self, self.next_song)
        QShortcut(QKeySequence("Left"), self, self.prev_song)
        QShortcut(QKeySequence("A"), self, self.prev_song)
        QShortcut(QKeySequence("Up"), self, self.toggle_repeat)
        QShortcut(QKeySequence("W"), self, self.toggle_repeat)
        QShortcut(QKeySequence("Down"), self, self.toggle_shuffle)
        QShortcut(QKeySequence("F"), self, lambda: self.search_bar.setFocus())
        QShortcut(QKeySequence("H"), self, self.show_shortcuts_help)

    def _setup_ui(self):
        # Main layout: sidebar (song/playlist list) + content (now playing, controls)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(8)
        sidebar = create_sidebar(self)
        splitter.addWidget(sidebar)
        content = QFrame()
        content.setStyleSheet("background: #0A2239; border-top-right-radius: 16px; border-bottom-right-radius: 16px;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(32, 32, 32, 32)
        content_layout.setSpacing(24)
        # Now playing label
        self.now_playing = QLabel("בחר שיר מהרשימה")
        self.now_playing.setObjectName("NowPlaying")
        self.now_playing.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.now_playing)
        # Slider row (seek bar + time labels)
        slider_row = QHBoxLayout()
        slider_row.setSpacing(10)
        self.current_time_label = QLabel("0:00")
        self.current_time_label.setFont(QFont("Segoe UI", 11))
        self.current_time_label.setStyleSheet("color: #FFD700; min-width: 48px;")
        slider_row.addWidget(self.current_time_label)
        self.seek_slider = ClickableSlider(Qt.Orientation.Horizontal)
        self.seek_slider.setRange(0, 100)
        self.seek_slider.sliderMoved.connect(self.seek_song)
        self.seek_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: none;
                height: 8px;
                background: #1565C0;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: #FFF;
                border-radius: 4px;
            }
            QSlider::add-page:horizontal {
                background: #1565C0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #FFD700;
                border: 2px solid #FFF;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
        """)
        slider_row.addWidget(self.seek_slider, 1)
        self.total_time_label = QLabel("0:00")
        self.total_time_label.setFont(QFont("Segoe UI", 11))
        self.total_time_label.setStyleSheet("color: #FFD700; min-width: 48px;")
        slider_row.addWidget(self.total_time_label)
        content_layout.addLayout(slider_row)
        # Playback controls (play, pause, next, prev, etc)
        controls = create_controls(self)
        content_layout.addLayout(controls)
        splitter.addWidget(content)
        splitter.setSizes([320, 600])
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(splitter)

    def toggle_favorite(self):
        # Toggle favorite status for the current song
        if not self.songs:
            return
        song = self.songs[self.current_song_index]
        if song in self.favorites:
            self.favorites.remove(song)
        else:
            self.favorites.add(song)
        self.save_favorites()
        self.update_fav_btn()

    def update_fav_btn(self):
        # Update the favorite button icon based on current song
        if not self.songs:
            self.fav_btn.setText("⭐")
            return
        song = self.songs[self.current_song_index]
        if song in self.favorites:
            self.fav_btn.setText("★")
        else:
            self.fav_btn.setText("⭐")

    def show_favorites(self):
        # Show only favorite songs in the list
        self.song_list.clear()
        for i, song in enumerate(self.songs):
            if song in self.favorites:
                item = QListWidgetItem(os.path.splitext(song)[0])
                item.setData(Qt.ItemDataRole.UserRole, i)
                self.song_list.addItem(item)
        self.show_fav_btn.setText("חזור לרשימה")
        self.show_fav_btn.clicked.disconnect()
        self.show_fav_btn.clicked.connect(self.show_all_songs)

    def show_all_songs(self):
        # Restore the full song list
        self.load_songs()
        self.show_fav_btn.setText("מועדפים")
        self.show_fav_btn.clicked.disconnect()
        self.show_fav_btn.clicked.connect(self.show_favorites)

    def load_favorites(self):
        # Load favorites from file (if exists)
        if os.path.exists(self.favorites_file):
            with open(self.favorites_file, "r", encoding="utf-8") as f:
                self.favorites = set(json.load(f))

    def save_favorites(self):
        # Save favorites to file
        with open(self.favorites_file, "w", encoding="utf-8") as f:
            json.dump(list(self.favorites), f, ensure_ascii=False)

    def load_songs(self):
        # Load all mp3 files from the songs directory
        self.song_list.clear()
        if not os.path.exists(SONGS_DIR):
            os.makedirs(SONGS_DIR)
        self.songs = [f for f in os.listdir(SONGS_DIR) if f.endswith('.mp3')]
        self.update_fav_btn()
        for i, song in enumerate(self.songs):
            song_name = os.path.splitext(song)[0]
            item = QListWidgetItem(song_name)
            font = QFont("Segoe UI", 12)
            if i == self.current_song_index:
                font.setBold(True)
                item.setForeground(QColor("#00BFFF"))
            else:
                font.setBold(False)
                item.setForeground(QColor("#FFD700"))
            item.setFont(font)
            self.song_list.addItem(item)

    def filter_songs(self, text=""):
        # Filter songs in the list by search text
        self.song_list.clear()
        for i, song in enumerate(self.songs):
            if text.lower() in song.lower():
                item = QListWidgetItem(os.path.splitext(song)[0])
                item.setData(Qt.ItemDataRole.UserRole, i)
                self.song_list.addItem(item)

    def song_double_clicked(self, item):
        idx = item.data(Qt.ItemDataRole.UserRole)
        if self.active_playlist_songs:
            # קבל את שם השיר שנבחר (מתוך הפלייליסט)
            song_name = os.path.splitext(item.text())[0]
            for i, song in enumerate(self.active_playlist_songs):
                if os.path.splitext(song)[0] == song_name:
                    self.start_song(i)
                    return
        else:
            if idx is None:
                idx = self.song_list.row(item)
            self.start_song(idx)

    def start_song(self, idx):
        # Start playback of the song at index idx
        if self.active_playlist_songs:
            song = self.active_playlist_songs[idx]
            self.active_playlist_index = idx
            self.current_song_index = self.songs.index(song)
            song_name = os.path.splitext(song)[0]
            song_path = os.path.join(SONGS_DIR, song)
        else:
            self.current_song_index = idx
            song_name = os.path.splitext(self.songs[idx])[0]
            song_path = os.path.join(SONGS_DIR, self.songs[idx])
        self.update_fav_btn()
        if not self.songs:
            return
        self.now_playing.setText(song_name)
        # Update song_list selection by matching the displayed name
        for i in range(self.song_list.count()):
            item = self.song_list.item(i)
            item_name = item.text()
            font = QFont("Segoe UI", 12)
            if item_name == song_name:
                font.setBold(True)
                item.setForeground(QColor("#00BFFF"))
                self.song_list.setCurrentRow(i)
            else:
                font.setBold(False)
                item.setForeground(QColor("#FFD700"))
            item.setFont(font)
        media = self.instance.media_new(song_path)
        self.player.set_media(media)
        self.player.play()
        self.is_paused = False
        self.play_pause_btn.setText("⏸")

    def toggle_play_pause(self):
        if self.player.is_playing():
            self.player.pause()
            self.is_paused = True
            self.play_pause_btn.setText("▶")
        elif self.is_paused:
            self.player.play()
            self.is_paused = False
            self.play_pause_btn.setText("⏸")
        else:
            self.start_song(self.current_song_index)

    def next_song(self):
        # Go to next song (handles repeat and shuffle modes)
        if not self.songs:
            return
        if self.active_playlist_songs:
            if self.shuffle:
                self.active_playlist_index = random.randint(0, len(self.active_playlist_songs) - 1)
            else:
                self.active_playlist_index = (self.active_playlist_index + 1) % len(self.active_playlist_songs)
            self.start_song(self.active_playlist_index)
            return
        if self.repeat_mode == "once":
            self.start_song(self.current_song_index)
            self.repeat_mode = "none"
            self.repeat_btn.setText("🔁")
            self.repeat_btn.setStyleSheet(
                self.repeat_btn.styleSheet()
                .replace("background: #00BFFF;", "background: #FFD700;")
                .replace("border: 2px solid #00BFFF;", "")
                .replace("color: #FFD700;", "color: #00BFFF;")
            )
        elif self.repeat_mode == "always":
            self.start_song(self.current_song_index)
        else:
            if self.shuffle:
                self.current_song_index = random.randint(0, len(self.songs) - 1)
            else:
                self.current_song_index = (self.current_song_index + 1) % len(self.songs)
            self.start_song(self.current_song_index)

    def prev_song(self):
        # Go to previous song (handles shuffle mode)
        if not self.songs:
            return
        if self.active_playlist_songs:
            if self.shuffle:
                self.active_playlist_index = random.randint(0, len(self.active_playlist_songs) - 1)
            else:
                self.active_playlist_index = (self.active_playlist_index - 1) % len(self.active_playlist_songs)
            self.start_song(self.active_playlist_index)
            return
        if self.shuffle:
            self.current_song_index = random.randint(0, len(self.songs) - 1)
        else:
            self.current_song_index = (self.current_song_index - 1) % len(self.songs)
        self.start_song(self.current_song_index)

    def toggle_repeat(self):
        # Cycle repeat mode: none -> once -> always -> none
        if self.repeat_mode == "none":
            self.repeat_mode = "once"
            self.repeat_btn.setText("🔁1")
            self.repeat_btn.setStyleSheet(
                self.repeat_btn.styleSheet()
                .replace("background: #FFD700;", "background: #00BFFF;")
                .replace("color: #00BFFF;", "color: #FFD700;")
            )
        elif self.repeat_mode == "once":
            self.repeat_mode = "always"
            self.repeat_btn.setText("🔁♾️")
            self.repeat_btn.setStyleSheet(
                self.repeat_btn.styleSheet()
                .replace("background: #00BFFF;", "background: #00BFFF;")
                .replace("color: #FFD700;", "color: #FFD700;")
                .replace("border: 2px solid #FFD700;", "border: 2px solid #00BFFF;")
            )
        else:
            self.repeat_mode = "none"
            self.repeat_btn.setText("🔁")
            self.repeat_btn.setStyleSheet(
                self.repeat_btn.styleSheet()
                .replace("background: #00BFFF;", "background: #FFD700;")
                .replace("border: 2px solid #00BFFF;", "")
                .replace("color: #FFD700;", "color: #00BFFF;")
            )

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle
        if self.shuffle:
            self.shuffle_btn.setStyleSheet(
                self.shuffle_btn.styleSheet()
                .replace("background: #FFD700;", "background: #00BFFF;")
                .replace("color: #00BFFF;", "color: #FFD700;")
                + "border: 2px solid #00BFFF;"
            )
        else:
            self.shuffle_btn.setStyleSheet(
                self.shuffle_btn.styleSheet()
                .replace("background: #00BFFF;", "background: #FFD700;")
                .replace("color: #FFD700;", "color: #00BFFF;")
                .replace("border: 2px solid #00BFFF;", "")
            )

    def seek_song(self, value):
        # Seek to a specific time in the song (in seconds)
        try:
            self.player.set_time(int(float(value) * 1000))
        except Exception:
            pass

    def format_time(self, seconds):
        # Format seconds as m:ss (used for time labels)
        if seconds is None or seconds < 0:
            return "0:00"
        m = int(seconds) // 60
        s = int(seconds) % 60
        return f"{m}:{s:02d}"

    def update_ui(self):
        # Update UI elements (seek bar, time labels, play/pause button)
        if self.player.is_playing() or self.is_paused:
            try:
                length = self.player.get_length() // 1000
                pos = self.player.get_time() // 1000
                if length > 0:
                    self.seek_slider.setMaximum(length)
                    self.seek_slider.setValue(pos)
                self.current_time_label.setText(self.format_time(pos))
                self.total_time_label.setText(self.format_time(length))
            except Exception:
                pass
        else:
            self.current_time_label.setText("0:00")
            self.total_time_label.setText("0:00")
        state = self.player.get_state()
        if state == vlc.State.Ended:
            self.next_song()
        elif state == vlc.State.Paused:
            self.play_pause_btn.setText("▶")
        elif state == vlc.State.Playing:
            self.play_pause_btn.setText("⏸")

    def show_shortcuts_help(self):
        # Show a dialog with all keyboard shortcuts
        msg = QMessageBox(self)
        msg.setWindowTitle("קיצורי מקלדת")
        msg.setText(
            "קיצורי מקלדת:\n"
            "⏯ ניגון/השהיה = רווח / S\n"
            "⏭ השיר הבא = → / D\n"
            "⏮ השיר הקודם: ← / A\n"
            "🔁 Repeat = ↑ / W\n"
            "🔀 Shuffle = ↓\n"
            "🔎 חיפוש שירים = F\n"
            "❓ עזרה = H\n"
        )
        msg.setStyleSheet("""
            QMessageBox { background: white; }
            QLabel { background: white; color: #222; font-size: 18px; }
            QPushButton { background: #f5f5f5; color: #222; border-radius: 8px; min-width: 250px; min-height: 28px; }
            QPushButton:hover { background: #e0e0e0; }
        """)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setFixedSize(840, 700)
        msg.exec()

    def show_playlist_songs(self, item):
        playlist_name = item.text()
        playlists = self.playlists_manager.load_playlists()
        for pl in playlists:
            if pl["name"] == playlist_name:
                self.active_playlist_songs = [song for song in pl["songs"] if song in self.songs]
                selected_song_name = item.text()
                idx_in_playlist = 0
                for i, song in enumerate(self.active_playlist_songs):
                    if os.path.splitext(song)[0] == selected_song_name:
                        idx_in_playlist = i
                        break
                self.active_playlist_index = idx_in_playlist
                self.song_list.clear()
                for song in pl["songs"]:
                    if song in self.songs:
                        idx = self.songs.index(song)
                        song_item = QListWidgetItem(os.path.splitext(song)[0])
                        song_item.setData(Qt.ItemDataRole.UserRole, idx)
                        self.song_list.addItem(song_item)
                break
        if hasattr(self, "show_playlists_btn") and self.show_playlists_btn is not None:
            self.show_playlists_btn.hide()
        if hasattr(self, "back_to_playlists_btn") and self.back_to_playlists_btn is not None:
            self.back_to_playlists_btn.hide()
            sidebar_layout = self.song_list.parentWidget().layout()
            sidebar_layout.removeWidget(self.back_to_playlists_btn)
            self.back_to_playlists_btn.deleteLater()
            self.back_to_playlists_btn = None
        from PyQt6.QtWidgets import QPushButton
        self.back_to_playlists_btn = QPushButton("חזור לרשימות ההשמעה")
        self.back_to_playlists_btn.setStyleSheet(
            "background: #FFD700; color: #164B74; font-weight: bold; border-radius: 8px; padding: 8px; margin-top: 12px;"
        )
        self.back_to_playlists_btn.clicked.connect(self.show_playlists_list)
        sidebar_layout = self.song_list.parentWidget().layout()
        sidebar_layout.addWidget(self.back_to_playlists_btn)
        self.back_to_playlists_btn.show()

    def toggle_playlists_view(self):
        # Toggle between playlists list and song list
        if hasattr(self, "show_playlists_btn") and self.show_playlists_btn is not None:
            self.show_playlists_btn.show()
        if hasattr(self, "back_to_playlists_btn") and self.back_to_playlists_btn is not None:
            self.back_to_playlists_btn.hide()
            sidebar_layout = self.song_list.parentWidget().layout()
            sidebar_layout.removeWidget(self.back_to_playlists_btn)
            self.back_to_playlists_btn.deleteLater()
            self.back_to_playlists_btn = None
        if hasattr(self, "create_playlist_btn") and self.create_playlist_btn is not None:
            sidebar_layout = self.song_list.parentWidget().layout()
            sidebar_layout.removeWidget(self.create_playlist_btn)
            self.create_playlist_btn.deleteLater()
            self.create_playlist_btn = None
        if not hasattr(self, 'showing_playlists'):
            self.showing_playlists = False
        if not self.showing_playlists:
            self.song_list.clear()
            playlists = self.playlists_manager.load_playlists()
            try:
                self.song_list.itemClicked.disconnect()
            except TypeError:
                pass
            for pl in playlists:
                item = QListWidgetItem(pl["name"])
                self.song_list.addItem(item)
            self.song_list.itemClicked.connect(self.show_playlist_songs)
            self.song_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.song_list.customContextMenuRequested.connect(self.show_playlist_context_menu)
            self.show_playlists_btn.setText("חזור לרשימת השירים")
            self.showing_playlists = True
            from PyQt6.QtWidgets import QPushButton
            btn_style = """
                QPushButton {
                    background: #FFD700;
                    color: #00BFFF;
                    border-radius: 16px;
                    font-size: 15px;
                    min-width: 80px;
                    min-height: 36px;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-weight: bold;
                    border: 2px solid #e6c200;
                }
                QPushButton:hover {
                    background: #FFF5B7;
                    color: #164B74;
                    border: 2px solid #bfa600;
                }
                QPushButton:pressed {
                    background: #e6c200;
                    color: #164B74;
                    border: 2px solid #bfa600;
                }
            """
            self.create_playlist_btn = QPushButton("צור רשימת השמעה")
            self.create_playlist_btn.setStyleSheet(btn_style)
            self.create_playlist_btn.clicked.connect(self.create_new_playlist)
            sidebar_layout = self.song_list.parentWidget().layout()
            sidebar_layout.addWidget(self.create_playlist_btn)
        else:
            try:
                self.song_list.itemClicked.disconnect()
            except TypeError:
                pass
            self.load_songs()
            self.show_playlists_btn.setText("הצג רשימות השמעה")
            self.showing_playlists = False
            self.song_list.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
            if hasattr(self, "create_playlist_btn") and self.create_playlist_btn is not None:
                sidebar_layout = self.song_list.parentWidget().layout()
                sidebar_layout.removeWidget(self.create_playlist_btn)
                self.create_playlist_btn.deleteLater()
                self.create_playlist_btn = None

    def show_playlists_list(self):
        # Show the list of playlists in the sidebar
        self.active_playlist_songs = None
        self.active_playlist_index = None
        if hasattr(self, "show_playlists_btn") and self.show_playlists_btn is not None:
            self.show_playlists_btn.show()
        if hasattr(self, "back_to_playlists_btn") and self.back_to_playlists_btn is not None:
            self.back_to_playlists_btn.hide()
            sidebar_layout = self.song_list.parentWidget().layout()
            sidebar_layout.removeWidget(self.back_to_playlists_btn)
            self.back_to_playlists_btn.deleteLater()
            self.back_to_playlists_btn = None
        if hasattr(self, "create_playlist_btn") and self.create_playlist_btn is not None:
            sidebar_layout = self.song_list.parentWidget().layout()
            sidebar_layout.removeWidget(self.create_playlist_btn)
            self.create_playlist_btn.deleteLater()
            self.create_playlist_btn = None
        self.song_list.clear()
        playlists = self.playlists_manager.load_playlists()
        try:
            self.song_list.itemClicked.disconnect()
        except TypeError:
            pass
        for pl in playlists:
            item = QListWidgetItem(pl["name"])
            self.song_list.addItem(item)
        self.song_list.itemClicked.connect(self.show_playlist_songs)
        self.song_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.song_list.customContextMenuRequested.connect(self.show_playlist_context_menu)
        self.show_playlists_btn.setText("חזור לרשימת השירים")
        self.showing_playlists = True
        from PyQt6.QtWidgets import QPushButton
        btn_style = """
            QPushButton {
                background: #FFD700;
                color: #00BFFF;
                border-radius: 16px;
                font-size: 15px;
                min-width: 80px;
                min-height: 36px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-weight: bold;
                border: 2px solid #e6c200;
            }
            QPushButton:hover {
                background: #FFF5B7;
                color: #164B74;
                border: 2px solid #bfa600;
            }
            QPushButton:pressed {
                background: #e6c200;
                color: #164B74;
                border: 2px solid #bfa600;
            }
        """
        self.create_playlist_btn = QPushButton("צור רשימת השמעה")
        self.create_playlist_btn.setStyleSheet(btn_style)
        self.create_playlist_btn.clicked.connect(self.create_new_playlist)
        sidebar_layout = self.song_list.parentWidget().layout()
        sidebar_layout.addWidget(self.create_playlist_btn)

    def show_playlist_context_menu(self, pos):
        item = self.song_list.itemAt(pos)
        if not item:
            return
        from PyQt6.QtWidgets import QMenu
        menu = QMenu(self)
        delete_action = menu.addAction("מחק פלייליסט")
        action = menu.exec(self.song_list.mapToGlobal(pos))
        if action == delete_action:
            playlist_name = item.text()
            reply = QMessageBox.question(self, "אישור מחיקה", f"האם למחוק את הפלייליסט '{playlist_name}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                playlists = self.playlists_manager.load_playlists()
                playlists = [pl for pl in playlists if pl["name"] != playlist_name]
                self.playlists_manager.save_playlists(playlists)
                QMessageBox.information(self, "נמחק", f"הפלייליסט '{playlist_name}' נמחק.")
                self.toggle_playlists_view()
                self.toggle_playlists_view()

    def add_current_song_to_playlist(self):
        playlists = [pl["name"] for pl in self.playlists_manager.load_playlists()]
        if not playlists:
            QMessageBox.information(self, "הוספה", "אין רשימות השמעה קיימות. צור אחת תחילה.")
            return
        playlist_name, ok = QInputDialog.getItem(self, "הוסף", "בחר רשימה:", playlists, editable=False)
        if ok and playlist_name:
            song = self.songs[self.current_song_index]
            self.playlists_manager.add_to_playlist(song, playlist_name)
            QMessageBox.information(self, "הוספה", f"השיר נוסף לרשימה '{playlist_name}'.")

    def remove_current_song_from_playlist(self):
        song = self.songs[self.current_song_index]
        playlists = [pl["name"] for pl in self.playlists_manager.load_playlists() if song in pl["songs"]]
        if not playlists:
            QMessageBox.information(self, "הסר", "השיר לא נמצא באף רשימת השמעה.")
            return
        playlist_name, ok = QInputDialog.getItem(self, "הסר מרשימת השמעה", "בחר רשימה:", playlists, editable=False)
        if ok and playlist_name:
            self.playlists_manager.remove_from_playlist(song, playlist_name)
            QMessageBox.information(self, "הסרה", f"השיר הוסר מהרשימה '{playlist_name}'.")

    def create_new_playlist(self):
        # Create a new playlist with a unique name
        playlists = [pl["name"] for pl in self.playlists_manager.load_playlists()]
        name, ok = QInputDialog.getText(self, "צור רשימת השמעה", "שם רשימת ההשמעה:")
        if not ok or not name.strip():
            return
        name = name.strip()
        if name in playlists:
            QMessageBox.warning(self, "שגיאה", f"רשימת השמעה בשם '{name}' כבר קיימת.")
            return
        all_playlists = self.playlists_manager.load_playlists()
        all_playlists.append({"name": name, "songs": []})
        self.playlists_manager.save_playlists(all_playlists)
        QMessageBox.information(self, "נוצרה רשימה", f"הרשימה '{name}' נוצרה בהצלחה.")
        if hasattr(self, 'showing_playlists') and self.showing_playlists:
            self.toggle_playlists_view()
            self.toggle_playlists_view()