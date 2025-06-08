from comm import TickLoadingOutput
from .handle_loading_status import handle_loading_status

def update_comm(self, dataList:list[dict]|None):
    if dataList is None:
        return
    
    for data in dataList:
        if data is None:
            continue
        
        if data["type"] == "loading_status":
            data = TickLoadingOutput(data)
            handle_loading_status(self, data)