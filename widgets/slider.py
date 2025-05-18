from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import Qt

class ClickableSlider(QSlider):
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            x = event.position().x()
            width = self.width()
            value = self.minimum() + (self.maximum() - self.minimum()) * x / width
            self.setValue(int(value))
            self.sliderMoved.emit(int(value))
        super().mousePressEvent(event)