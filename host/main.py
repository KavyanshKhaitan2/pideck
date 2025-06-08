import comm

def main():
    # ser = comm.Serial(port="/dev/ttyV0")
    ser = comm.Serial(port="/dev/ttyV0")
    print("Waiting for handshake...")
    output = ser.wait_for_connection_stage1()
    print(output)
    print("Initial handshake complete")
    ser.send("ui clean 8 5")
    ser.send("ui button 0 0 'Hello world!' dispatch nop")
    ser.send("ui button 0 1 'Here is some data...' dispatch nop")
    while True:
        ser.send(input(">>> "))

if __name__ == "__main__":
    main()
