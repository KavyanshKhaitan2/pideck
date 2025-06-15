from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6 import QtCore


class ScalableTextWidget(QWidget):
    def __init__(self, text):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel(
            text, wordWrap=True, alignment=QtCore.Qt.AlignCenter, scaledContents=True
        )
        self.setText(text)

        layout.addWidget(self.label)

        self.setLayout(layout)

    def setText(self, text, *args, **kwargs):
        self.label.setText(text, *args, **kwargs)
        new_size = min(self.label.width() // 10, self.label.height() // 2)
        font = self.label.font()
        font.setPointSize(new_size)
        self.label.setFont(font)
