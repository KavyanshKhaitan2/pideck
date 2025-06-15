from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Slot
from comm import UIButtonParseOutput
from app import SimpleWindow
from widgets.scalable_button import ScalableButton
import shlex

def handle_ui_button(self: SimpleWindow, data: UIButtonParseOutput):
    btn = ScalableButton(data["text"])
    
    if data['broadcast']:
        
        def broadcast_on_click():
            self.comm_port.send(shlex.join(["broadcast", "recieve", data["message"]]))
            
        btn.clicked.connect(broadcast_on_click)
    

    supported_dispatches = ["nop"]

    if not data["broadcast"]:
        if data["message"].lower() not in supported_dispatches:
            raise NotImplementedError

    self.main_grid.addWidget(
        btn, x=data["x"], y=data["y"], x_span=data["x_span"], y_span=data["y_span"]
    )
