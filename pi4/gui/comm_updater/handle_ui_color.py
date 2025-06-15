from comm import UIColorParseOutput
from app import SimpleWindow
from widgets.scalable_button import ScalableButton


def handle_ui_color(self: SimpleWindow, data: UIColorParseOutput):
    type = data['type']
    x = data['x']
    y = data['y']
    color = data['color']
    
    widget:ScalableButton = self.main_grid.widgets[x, y]
    
    if type == "ui_bgcolor":
        widget.set_background_color(color)
    
    if type == "ui_textcolor":
        widget.set_text_color(color)