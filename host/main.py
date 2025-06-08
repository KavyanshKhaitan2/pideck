import comm

def main():
    # ser = comm.Serial(port="/dev/ttyV0")
    ser = comm.Serial(port="/dev/ttyV0")
    print("Waiting for handshake...")
    output = ser.wait_for_connection_stage1()
    print(output)
    print("Initial handshake complete")


if __name__ == "__main__":
    main()
