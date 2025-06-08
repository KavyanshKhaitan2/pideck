from comm import TickLoadingOutput
from .handle_loading_status import handle_loading_status

def update_comm(self, data:dict):
    if data is None:
        return
    
    if data["type"] == "loading_status":
        data = TickLoadingOutput(data)
        handle_loading_status(self, data)