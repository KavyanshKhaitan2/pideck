import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer
from widgets.resizing_text import ResizingTextWidget
import comm
from comm_updater import comm_updater


class SimpleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()

        self.comm_port = comm.Serial(port="/dev/ttyV1")

        self.setWindowTitle("Pideck Raspberry Pi Client")
        layout = QVBoxLayout()

        self.loading_widget = ResizingTextWidget("Initial Loading\nWaiting for host...")
        layout.addWidget(self.loading_widget)

        self.timer.timeout.connect(self.look_into_serial_comm)
        self.timer.start(200)

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
