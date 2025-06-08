import serial
import time
from typing import TypedDict, Literal
import shlex


class TickLoadingOutput(TypedDict):
    type: Literal["loading_status"]
    data: str

class UIButtonParseOutput(TypedDict):
    type: Literal["ui_button"]
    x: int
    y: int
    text: str
    broadcast: bool
    message: str

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
        args = shlex.split(data)
        if args[0] != "ui" or args[1] != "button":
            return
        x = int(args[2])
        y = int(args[3])
        text = args[4]
        broadcast = True if args[5] == "broadcast" else False
        message = args[6]

        return UIButtonParseOutput(
            type="ui_button", x=x, y=y, text=text, broadcast=broadcast, message=message
        )

    def ui_clean_parse(self, data: str):
        args = shlex.split(data)
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
        

        return UICleanParseOutput(
            type="ui_clean", width=width, height=height
        )

    def tick(self):
        data = self.read()
        if data is not None:
            datalines = data.splitlines()
        else:
            datalines = ['NOP']

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

        return returnData
