from comm import UICleanParseOutput
from app import SimpleWindow


def handle_ui_clean(self:SimpleWindow, data:UICleanParseOutput):
    self.loading_widget.hide()
    self.main_grid.show()
    self.main_grid.resizeGrid(data['width'], data['height'])