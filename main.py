import sys
import os
import random
import vlc
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider,
    QListWidget, QListWidgetItem, QFrame, QSplitter
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor

SONGS_DIR = os.path.join(os.path.dirname(__file__), "songs")

class ClickableSlider(QSlider):
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            x = event.position().x()
            width = self.width()
            value = self.minimum() + (self.maximum() - self.minimum()) * x / width
            self.setValue(int(value))
            self.sliderMoved.emit(int(value))
        super().mousePressEvent(event)

class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Re'em - Music Player")
        self.setMinimumSize(700, 420)
        self.setStyleSheet("""
            QWidget { background: #0A2239; }
            QLabel#NowPlaying { color: #00BFFF; font-size: 22px; font-weight: bold; font-family: 'Segoe UI', Arial, sans-serif; }
            QListWidget { background: #164B74; color: #FFD700; border-radius: 12px; font-size: 16px; font-family: 'Segoe UI', Arial, sans-serif; border: none; }
            QListWidget::item:selected { background: #FFD700; color: #00BFFF; font-weight: bold; }
            QSlider::groove:horizontal { background: #1565C0; height: 8px; border-radius: 4px; }
            QSlider::handle:horizontal { background: #FFD700; width: 18px; border-radius: 9px; }
            QPushButton { border: none; }
        """)

        self.instance = vlc.Instance("--quiet")
        self.player = self.instance.media_player_new()
        self.current_song_index = 0
        self.repeat_mode = "none"
        self.shuffle = False
        self.is_paused = False

        self._setup_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000)
        self.load_songs()

    def _setup_ui(self):
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(8)

        sidebar = QFrame()
        sidebar.setMinimumWidth(180)
        sidebar.setMaximumWidth(500)
        sidebar.setStyleSheet("background: #164B74; border-top-left-radius: 16px; border-bottom-left-radius: 16px;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(18, 18, 18, 18)
        sidebar_layout.setSpacing(12)

        sidebar_label = QLabel("שירים")
        sidebar_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))
        sidebar_label.setStyleSheet("color: #FFD700; letter-spacing: 1px;")
        sidebar_layout.addWidget(sidebar_label)

        self.song_list = QListWidget()
        self.song_list.setFont(QFont("Montserrat", 13, QFont.Weight.DemiBold))
        self.song_list.setStyleSheet("""
            QListWidget { padding-right: 0px; }
            QListWidget::item { padding: 10px 8px; }
        """)
        self.song_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.song_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.song_list.itemDoubleClicked.connect(self.song_double_clicked)
        sidebar_layout.addWidget(self.song_list, 1)
        splitter.addWidget(sidebar)

        content = QFrame()
        content.setStyleSheet("background: #0A2239; border-top-right-radius: 16px; border-bottom-right-radius: 16px;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(32, 32, 32, 32)
        content_layout.setSpacing(24)

        self.now_playing = QLabel("בחר שיר מהרשימה")
        self.now_playing.setObjectName("NowPlaying")
        self.now_playing.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.now_playing)

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
        content_layout.addWidget(self.seek_slider)

        controls = QHBoxLayout()
        controls.setSpacing(18)
        content_layout.addLayout(controls)

        btn_style = """
            QPushButton {
                background: #FFD700;
                color: #00BFFF;
                border-radius: 24px;
                font-size: 22px;
                min-width: 48px;
                min-height: 48px;
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

        self.prev_btn = QPushButton("⏮")
        self.prev_btn.setStyleSheet(btn_style)
        self.prev_btn.clicked.connect(self.prev_song)
        controls.addWidget(self.prev_btn)

        self.play_pause_btn = QPushButton("▶")
        self.play_pause_btn.setStyleSheet(btn_style + "QPushButton { font-size: 28px; min-width: 56px; min-height: 56px; }")
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)
        controls.addWidget(self.play_pause_btn)

        self.next_btn = QPushButton("⏭")
        self.next_btn.setStyleSheet(btn_style)
        self.next_btn.clicked.connect(self.next_song)
        controls.addWidget(self.next_btn)

        self.repeat_btn = QPushButton("🔁")
        self.repeat_btn.setStyleSheet(btn_style + "QPushButton { font-size: 18px; min-width: 40px; min-height: 40px; }")
        self.repeat_btn.clicked.connect(self.toggle_repeat)
        controls.addWidget(self.repeat_btn)

        self.shuffle_btn = QPushButton("🔀")
        self.shuffle_btn.setStyleSheet(btn_style + "QPushButton { font-size: 18px; min-width: 40px; min-height: 40px; }")
        self.shuffle_btn.clicked.connect(self.toggle_shuffle)
        controls.addWidget(self.shuffle_btn)

        splitter.addWidget(content)
        splitter.setSizes([320, 600])

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(splitter)
        main_layout.addWidget(content, 1)

    def load_songs(self):
        self.song_list.clear()
        if not os.path.exists(SONGS_DIR):
            os.makedirs(SONGS_DIR)
        self.songs = [f for f in os.listdir(SONGS_DIR) if f.endswith('.mp3')]
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

    def song_double_clicked(self, item):
        idx = self.song_list.row(item)
        self.start_song(idx)

    def start_song(self, idx):
        if not self.songs:
            return
        self.current_song_index = idx
        song_name = os.path.splitext(self.songs[idx])[0]
        self.now_playing.setText(song_name)
        self.song_list.setCurrentRow(idx)
        for i in range(self.song_list.count()):
            item = self.song_list.item(i)
            font = QFont("Segoe UI", 12)
            if i == idx:
                font.setBold(True)
                item.setForeground(QColor("#00BFFF"))
            else:
                font.setBold(False)
                item.setForeground(QColor("#FFD700"))
            item.setFont(font)
        song_path = os.path.join(SONGS_DIR, self.songs[idx])
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
        if not self.songs:
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
        if not self.songs:
            return
        if self.shuffle:
            self.current_song_index = random.randint(0, len(self.songs) - 1)
        else:
            self.current_song_index = (self.current_song_index - 1) % len(self.songs)
        self.start_song(self.current_song_index)

    def toggle_repeat(self):
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
        try:
            self.player.set_time(int(float(value) * 1000))
        except Exception:
            pass

    def update_ui(self):
        if self.player.is_playing() or self.is_paused:
            try:
                length = self.player.get_length() // 1000
                pos = self.player.get_time() // 1000
                if length > 0:
                    self.seek_slider.setMaximum(length)
                    self.seek_slider.setValue(pos)
            except Exception:
                pass
        state = self.player.get_state()
        if state == vlc.State.Ended:
            self.next_song()
        elif state == vlc.State.Paused:
            self.play_pause_btn.setText("▶")
        elif state == vlc.State.Playing:
            self.play_pause_btn.setText("⏸")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec())