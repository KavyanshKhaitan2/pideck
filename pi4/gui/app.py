import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer
from widgets.scalable_text import ScalableTextWidget
from widgets.main_grid import MainGridWidget
import comm
from comm_updater import comm_updater


class SimpleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()

        self.comm_port = comm.Serial(port="/dev/ttyV1")

        self.setWindowTitle("Pideck Raspberry Pi Client")
        layout = QVBoxLayout()

        self.loading_widget = ScalableTextWidget("Initial Loading\nWaiting for host...")
        layout.addWidget(self.loading_widget)

        self.main_grid = MainGridWidget(1, 1)
        layout.addWidget(self.main_grid)
        self.main_grid.hide()
        
        self.timer.timeout.connect(self.look_into_serial_comm)
        self.timer.start(100)

        self.setLayout(layout)

    def look_into_serial_comm(self):
        data_received = self.comm_port.tick()
        comm_updater.update_comm(self, data_received)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    # window.showFullScreen()
    window.resize(1024, 600)
    sys.exit(app.exec())
