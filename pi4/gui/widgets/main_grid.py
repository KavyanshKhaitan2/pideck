from PySide6.QtWidgets import QLabel, QGridLayout, QWidget, QApplication, QPushButton, QSizePolicy
from PySide6.QtCore import QTimer, QSize, Qt
import sys
from widgets.scalable_button import ScalableButton
import random

class MainGridWidget(QWidget):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.timer = QTimer()
        
        self.gridlayout = QGridLayout()
        self.gridlayout.setSpacing(1)

        self.array_size = (width, height)

        self.widgets: dict[tuple[int, int], QWidget] = {}

        self.resizeGrid(width, height)

        self.setLayout(self.gridlayout)
        

    def addWidget(self, widget: QWidget, x: int, y: int, x_span=1, y_span=1, save=True):
        if x >= self.array_size[0]:
            raise IndexError(
                f"x={x} is not in range of this layout configuration (w={self.array_size[0]}, h={self.array_size[1]}). Use MainGridWidget.resizeGrid() to change to a minimum of width={x+1}."
            )
        if y >= self.array_size[1]:
            raise IndexError(
                f"y={y} is not in range of this layout configuration {self.array_size}. Use MainGridWidget.resizeGrid() to change to a minimum of height={y+1}."
            )

        old_wg = self.widgets.get((x, y))

        if old_wg is not None:
            old_wg.deleteLater()

        if save:
            self.widgets[(x, y)] = widget
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.gridlayout.addWidget(widget, y, x, y_span, x_span)

    def resizeGrid(self, width: int, height: int):
        for i in reversed(range(self.gridlayout.count())):
            self.gridlayout.itemAt(i).widget().deleteLater()

        self.array_size = (width, height)

        self.widgets = {}

        for x in range(width):
            self.gridlayout.setColumnStretch(x, 1)
        for y in range(height):
            self.gridlayout.setRowStretch(y, 1)
        
        self.addWidget(QLabel(), 0, 0, width, height, save=False)
        for x in range(width):
            for y in range(height):
                btn = ScalableButton()
                # btn = QPushButton()
                self.addWidget(btn, x, y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # widget = MainGridWidget(width=4, height=4)
    widget = MainGridWidget(width=10, height=5)
    widget.show()
    widget.resize(1024, 600)
    sys.exit(app.exec())
