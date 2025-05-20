from PyQt6.QtWidgets import QPushButton, QHBoxLayout

def create_controls(player):
    controls = QHBoxLayout()
    controls.setSpacing(18)
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
    player.fav_btn = QPushButton("⭐")
    player.fav_btn.setStyleSheet(btn_style + "QPushButton { font-size: 18px; min-width: 40px; min-height: 40px; }")
    player.fav_btn.clicked.connect(player.toggle_favorite)
    controls.addWidget(player.fav_btn)

    player.show_fav_btn = QPushButton("מועדפים")
    player.show_fav_btn.setStyleSheet(btn_style + "QPushButton { font-size: 14px; min-width: 80px; min-height: 40px; }")
    player.show_fav_btn.clicked.connect(player.show_favorites)
    controls.addWidget(player.show_fav_btn)

    player.prev_btn = QPushButton("⏮")
    player.prev_btn.setStyleSheet(btn_style)
    player.prev_btn.clicked.connect(player.prev_song)
    controls.addWidget(player.prev_btn)

    player.play_pause_btn = QPushButton("▶")
    player.play_pause_btn.setStyleSheet(
        btn_style + "QPushButton { font-size: 28px; min-width: 56px; min-height: 56px; }"
    )
    player.play_pause_btn.clicked.connect(player.toggle_play_pause)
    controls.addWidget(player.play_pause_btn)

    player.next_btn = QPushButton("⏭")
    player.next_btn.setStyleSheet(btn_style)
    player.next_btn.clicked.connect(player.next_song)
    controls.addWidget(player.next_btn)

    player.repeat_btn = QPushButton("🔁")
    player.repeat_btn.setStyleSheet(
        btn_style + "QPushButton { font-size: 18px; min-width: 40px; min-height: 40px; }"
    )
    player.repeat_btn.clicked.connect(player.toggle_repeat)
    controls.addWidget(player.repeat_btn)

    player.shuffle_btn = QPushButton("🔀")
    player.shuffle_btn.setStyleSheet(
        btn_style + "QPushButton { font-size: 18px; min-width: 40px; min-height: 40px; }"
    )
    player.shuffle_btn.clicked.connect(player.toggle_shuffle)
    controls.addWidget(player.shuffle_btn)

    player.add_to_playlist_btn = QPushButton("הוסף")
    player.add_to_playlist_btn.setStyleSheet(btn_style + "QPushButton { font-size: 14px; min-width: 80px; min-height: 40px; }")
    player.add_to_playlist_btn.clicked.connect(player.add_current_song_to_playlist)
    controls.addWidget(player.add_to_playlist_btn)

    player.remove_from_playlist_btn = QPushButton("הסר")
    player.remove_from_playlist_btn.setStyleSheet(btn_style + "QPushButton { font-size: 14px; min-width: 80px; min-height: 40px; }")
    player.remove_from_playlist_btn.clicked.connect(player.remove_current_song_from_playlist)
    controls.addWidget(player.remove_from_playlist_btn)

    return controls