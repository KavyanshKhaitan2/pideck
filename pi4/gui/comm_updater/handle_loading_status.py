from comm import TickLoadingOutput
from app import SimpleWindow

def handle_loading_status(self:SimpleWindow, data:TickLoadingOutput):
    self.loading_widget.setText(data['data'])