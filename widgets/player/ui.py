from PyQt6.QtWidgets import QSplitter, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from widgets.slider import ClickableSlider
from widgets.controls import create_controls

class PlayerUI:
    def __init__(self, parent):
        self.parent = parent
        self._setup_ui()

    def _setup_ui(self):
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(8)
        # Sidebar 
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
        self.parent.search_bar = QLineEdit()
        self.parent.search_bar.setPlaceholderText("מה אתם רוצים לנגן?")
        sidebar_layout.addWidget(self.parent.search_bar)
        self.parent.song_list = QListWidget()
        self.parent.song_list.setFont(QFont("Montserrat", 13, QFont.Weight.DemiBold))
        self.parent.song_list.setStyleSheet("""
            QListWidget { padding-right: 0px; }
            QListWidget::item { padding: 10px 8px; }
        """)
        self.parent.song_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.parent.song_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        sidebar_layout.addWidget(self.parent.song_list, 1)
        splitter.addWidget(sidebar)
        # Main content
        content = self._setup_content()
        splitter.addWidget(content)
        splitter.setSizes([320, 600])
        main_layout = QHBoxLayout(self.parent)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(splitter)

    def _setup_content(self):
        content = QFrame()
        content.setStyleSheet("background: #0A2239; border-top-right-radius: 16px; border-bottom-right-radius: 16px;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(32, 32, 32, 32)
        content_layout.setSpacing(24)
        self.parent.now_playing = QLabel("בחר שיר מהרשימה")
        self.parent.now_playing.setObjectName("NowPlaying")
        self.parent.now_playing.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.parent.now_playing)
        # Slider row
        slider_row = QHBoxLayout()
        slider_row.setSpacing(10)
        self.parent.current_time_label = QLabel("0:00")
        self.parent.current_time_label.setFont(QFont("Segoe UI", 11))
        self.parent.current_time_label.setStyleSheet("color: #FFD700; min-width: 48px;")
        slider_row.addWidget(self.parent.current_time_label)
        self.parent.seek_slider = ClickableSlider(Qt.Orientation.Horizontal)
        self.parent.seek_slider.setRange(0, 100)
        slider_row.addWidget(self.parent.seek_slider, 1)
        self.parent.total_time_label = QLabel("0:00")
        self.parent.total_time_label.setFont(QFont("Segoe UI", 11))
        self.parent.total_time_label.setStyleSheet("color: #FFD700; min-width: 48px;")
        slider_row.addWidget(self.parent.total_time_label)
        content_layout.addLayout(slider_row)
        # Controls row
        (
            controls, self.parent.fav_btn, self.parent.show_fav_btn, self.parent.prev_btn,
            self.parent.play_pause_btn, self.parent.next_btn, self.parent.repeat_btn,
            self.parent.shuffle_btn, self.parent.theme_btn
        ) = create_controls(
            self.parent.toggle_favorite, self.parent.show_favorites, self.parent.prev_song,
            self.parent.toggle_play_pause, self.parent.next_song, self.parent.toggle_repeat,
            self.parent.toggle_shuffle, self.parent.toggle_theme_icon
        )
        content_layout.addLayout(controls)
        return content
