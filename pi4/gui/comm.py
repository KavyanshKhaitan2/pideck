import serial
import time
from typing import TypedDict, Literal
import shlex


def shplit(raw_data: str):
    processed_data = raw_data.replace("\\\\", "\\").replace("\\n", "\n")
    return shlex.split(processed_data)


class TickLoadingOutput(TypedDict):
    type: Literal["loading_status"]
    data: str


class UIButtonParseOutput(TypedDict):
    type: Literal["ui_button"]
    x: int
    y: int
    x_span: int
    y_span: int
    text: str
    broadcast: bool
    message: str


class UIColorParseOutput(TypedDict):
    type: Literal["ui_bgcolor", "ui_textcolor"]
    x: int
    y: int
    color: str


class UIIconParseOutput(TypedDict):
    type: Literal["ui_icon"]
    x: int
    y: int
    base64icon: str


class UICleanParseOutput(TypedDict):
    type: Literal["ui_clean"]
    width: int
    height: int


class Serial:
    def __init__(
        self,
        port="/dev/ttyS0",
        baudrate=115200,
        timeout=1,
        verbose: bool | None = None,
    ):
        self.handshake_complete_stage = {1: False}

        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=timeout,
        )
        self.verbose = verbose

        if self.verbose:
            print("[INFO] Serial port opened successfully")

    def read(self):
        if self.ser.in_waiting > 0:
            data = (
                self.ser.read(self.ser.in_waiting).decode("utf-8").rstrip()
            )  # Read a line, decode, remove trailing newline
            # print(data)
            return data

    def send(self, data: str, end=""):
        self.ser.write((data + end).encode("utf-8"))

    def wait_for_connection_stage1(
        self, iterations: int | None = None, delay=1, data: str | None = None
    ):
        if self.handshake_complete_stage[1]:
            raise IOError("Stage 1 Handshake already complete")
        iters_done = 0
        if data is None:
            iterations = 1
        while (iterations is None) or (iters_done <= iterations):
            if data is None:
                data = self.read()
            self.send("handshake stage1 init")
            if "handshake stage1 complete" in str(data):
                print("Stage 1 Handshake Complete: Host is now online.")
                self.handshake_complete_stage[1] = True
                return True
            time.sleep(delay)
            iters_done += 1
        return False

    def ui_button_parse(self, data: str):
        args = shplit(data)
        if args[0] != "ui":
            return

        if args[1] != "button":
            return

        x = int(args[2])
        y = int(args[3])

        x_span = int(args[4])
        y_span = int(args[5])

        text = args[6]

        broadcast = True if args[7] == "broadcast" else False
        message = args[8]

        return UIButtonParseOutput(
            type="ui_button",
            x=x,
            y=y,
            x_span=x_span,
            y_span=y_span,
            text=text,
            broadcast=broadcast,
            message=message,
        )

    def ui_color_parse(self, data: str):
        args = shplit(data)

        if args[0] != "ui":
            return

        if args[1] not in ["bgcolor", "textcolor"]:
            return

        x = int(args[2])
        y = int(args[3])

        color = args[4]

        return UIColorParseOutput(type=f"ui_{args[1]}", x=x, y=y, color=color)

    def ui_icon_parse(self, data: str):
        args = shplit(data)

        if args[0] != "ui":
            return

        if args[1] != "icon":
            return

        x = int(args[2])
        y = int(args[3])

        base64icon = args[4]
        return UIIconParseOutput(type="ui_icon", x=x, y=y, base64icon=base64icon)

    def ui_clean_parse(self, data: str):
        args = shplit(data)
        if args[0] != "ui" or args[1] != "clean":
            return
        width = int(args[2])
        height = int(args[3])

        try:
            theme = args[4]
        except IndexError:
            theme = None

        if theme is not None:
            raise NotImplementedError

        return UICleanParseOutput(type="ui_clean", width=width, height=height)

    def tick(self):
        data = self.read()
        if data is not None:
            datalines = data.splitlines()
        else:
            datalines = ["NOP"]

        returnData = []

        for line in datalines:
            if line:
                line = line.strip()
            if not self.handshake_complete_stage[1]:
                if self.wait_for_connection_stage1(iterations=1, delay=0, data=line):
                    returnData.append(
                        TickLoadingOutput(
                            {
                                "type": "loading_status",
                                "data": "Initial Loading\nHost is online!",
                            }
                        )
                    )
                else:
                    returnData.append(
                        TickLoadingOutput(
                            {
                                "type": "loading_status",
                                "data": "Initial Loading\nWaiting for host...",
                            }
                        )
                    )

            if line.startswith("ui clean"):
                parsed = self.ui_clean_parse(line)
                if parsed is not None:
                    self.send("ok")
                    returnData.append(parsed)

            if line.startswith("ui button"):
                parsed = self.ui_button_parse(line)
                if parsed is not None:
                    self.send("ok")
                    returnData.append(parsed)

            if line.startswith("ui bgcolor") or line.startswith("ui textcolor"):
                parsed = self.ui_color_parse(line)
                if parsed is not None:
                    self.send("ok")
                    returnData.append(parsed)

            if line.startswith("ui icon"):
                parsed = self.ui_icon_parse(line)
                if parsed is not None:
                    self.send("ok")
                    returnData.append(parsed)

        return returnData
