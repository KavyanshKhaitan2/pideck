from comm import TickLoadingOutput, UIButtonParseOutput, UICleanParseOutput
from .handle_loading_status import handle_loading_status
from .handle_ui_button import handle_ui_button
from .handle_ui_clean import handle_ui_clean


def update_comm(self, dataList: list[dict] | None):
    if dataList is None:
        return

    for data in dataList:
        if data is None:
            continue

        if data["type"] == "loading_status":
            data = TickLoadingOutput(data)
            handle_loading_status(self, data)

        if data["type"] == "ui_clean":
            data = UICleanParseOutput(data)
            handle_ui_clean(self, data)

        if data["type"] == "ui_button":
            data = UIButtonParseOutput(data)
            handle_ui_button(self, data)
