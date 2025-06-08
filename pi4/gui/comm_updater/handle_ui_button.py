from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QSize
from comm import UIButtonParseOutput
from app import SimpleWindow


def handle_ui_button(self:SimpleWindow, data:UIButtonParseOutput):
    btn = QPushButton(data['text'])
    btn.setMaximumSize(QSize(9999, 9999))
    
    supported_dispatches = [
        'nop'
    ]
    if not data['broadcast']:
        if data['message'].lower() not in supported_dispatches:
            raise NotImplementedError
    
    self.main_grid.addWidget(btn, x=data['x'], y=data['y'])