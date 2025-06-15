from comm import UIIconParseOutput
from app import SimpleWindow
from widgets.scalable_button import ScalableButton
from PIL import Image
from PIL.ImageQt import ImageQt
from io import BytesIO
import base64
from PySide6.QtGui import QPixmap, QIcon


def handle_ui_icon(self: SimpleWindow, data: UIIconParseOutput):
    x = data["x"]
    y = data["y"]
    base64icon = data["base64icon"]

    widget: ScalableButton = self.main_grid.widgets[x, y]

    print(base64icon)
    
    image = Image.open(BytesIO(base64.b64decode(base64icon)))
    qimage = ImageQt(image)
    icon = QIcon(QPixmap.fromImage(qimage))

    widget.setIcon(icon)
