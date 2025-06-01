import serial
import time


class Serial:
    def __init__(
        self,
        port="/dev/ttyACM0",
        baudrate=115200,
        timeout=1,
        verbose: bool | None = None,
    ):
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
            return data
        else:
            return False

    def send(self, data: str, end=""):
        self.ser.write((data + end).encode("utf-8"))
    
    def wait_for_connection_stage1(
        self, iterations: int | None = None, delay=0.5
    ):
        iters_done = 0
        while (iterations is None) or (iters_done <= iterations):
            iters_done += 1
            data = self.read()
            if "handshake stage1 init" in str(data):
                self.send("handshake stage1 complete")
                return True
            time.sleep(delay)
        return False
