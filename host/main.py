import comm
import shlex

def main():
    # ser = comm.Serial(port="/dev/ttyV0")
    ser = comm.Serial(port="/dev/ttyV0")
    print("Waiting for handshake...")
    output = ser.wait_for_connection_stage1()
    print(output)
    print("Initial handshake complete")
    ser.send("ui clean 8 5")
    ser.send("ui button 0 0 1 1 'Hello world! Howdy!' dispatch nop")
    ser.send("ui button 0 1 2 2 'This is an x_span\ny_span test...' dispatch nop")

    ser.send("ui button 3 0 1 1 'Different bg and text color!' broadcast uuid_here")
    ser.send("ui bgcolor 3 0 #FF0000")
    ser.send("ui textcolor 3 0 #FFFFFF")
    
    act = False
    while True:
        read = ser.read()
        if read:
            print(read)
        
            if read.startswith("broadcast recieve"):
                d = shlex.split(read)
                bm = d[2]
                if bm == "uuid_here":
                    if act:
                        ser.send("ui bgcolor 3 0 #FF0000")
                    else:
                        ser.send("ui bgcolor 3 0 #00FF00")
                    act = not act

if __name__ == "__main__":
    while True:
        main()
