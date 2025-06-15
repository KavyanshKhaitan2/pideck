from comm import (
    TickLoadingOutput,
    UIButtonParseOutput,
    UICleanParseOutput,
    UIColorParseOutput,
    UIIconParseOutput,
)
from .handle_loading_status import handle_loading_status
from .handle_ui_button import handle_ui_button
from .handle_ui_clean import handle_ui_clean
from .handle_ui_color import handle_ui_color
from .handle_ui_icon import handle_ui_icon


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

        if data["type"] in ["ui_bgcolor", "ui_textcolor"]:
            data = UIColorParseOutput(data)
            handle_ui_color(self, data)

        if data["type"] in ["ui_icon"]:
            data = UIIconParseOutput(data)
            handle_ui_icon(self, data)
