from PyQt6.QtWidgets import QApplication
import sys
from widgets.player.main_player import MusicPlayer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec())