from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QLineEdit, QListWidget, QPushButton, QInputDialog, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

def create_sidebar(player):
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
    player.search_bar = QLineEdit()
    player.search_bar.setPlaceholderText("מה אתם רוצים לנגן?")
    player.search_bar.textChanged.connect(player.filter_songs)
    sidebar_layout.addWidget(player.search_bar)
    player.song_list = QListWidget()
    player.song_list.setFont(QFont("Montserrat", 13, QFont.Weight.DemiBold))
    player.song_list.setStyleSheet("""
        QListWidget { padding-right: 0px; }
        QListWidget::item { padding: 10px 8px; }
    """)
    player.song_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    player.song_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    player.song_list.itemDoubleClicked.connect(player.song_double_clicked)
    sidebar_layout.addWidget(player.song_list, 1)
    # עיצוב אחיד לכפתורים
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
    player.show_playlists_btn = QPushButton("הצג רשימות השמעה")
    player.show_playlists_btn.setStyleSheet(btn_style)
    sidebar_layout.addWidget(player.show_playlists_btn)
    player.show_playlists_btn.clicked.connect(player.toggle_playlists_view)

    return sidebar