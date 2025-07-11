import sys
import socket
import threading
import RPi.GPIO as GPIO
import spidev
import time
import conf_parser

BUF_SIZE = 1024
condition=threading.Condition()

def recv_data(sock):
    try:
        data = sock.recv(BUF_SIZE)

        if data:
            str = data.decode()
            return str

        print("Disconnected by no data")

    except socket.error:
        print("Thread exit by socket error")

    except ConnectionResetError:
        print("Disconnected by exception")

    return ""

def print_color(logstr):
    if logstr.startswith(LOGTAG_0):
        print("\033[96m", end='')
        print(logstr)
        print("\033[0m", end='')
    elif logstr.startswith(LOGTAG_1):
        print("\033[92m", end='')
        print(logstr)
        print("\033[0m", end='')
    else:
        print(logstr)


def main(argc, argv):
    print("Trying to connect to server")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((DEFAULT_HOST, DEFAULT_PORT))
    print("Connect to server")

    # LOG mask (4bit hex [0 to f])
    # BIT(0) : CameraServer
    # BIT(1) : BLEServer
    if argc <= 1:
        mode = "f"
    else:
        mode = argv[1]

    sock.send(mode.encode())

    tempstr = ""
    while True:
        try:
            msg = recv_data(sock)
            if msg == "":
                break

            logarr = msg.strip('\r').split('\n')
            i = 0
            for logline in logarr:
                if len(logline):
                    if tempstr != "":
                        logline = tempstr + logline
                        tempstr = ""

                    if len(msg) == BUF_SIZE and i == len(logarr) -1:
                        tempstr = logline
                    else:
                        print_color(logline)
                i+=1
            #print(msg, end='')

        except KeyboardInterrupt:
            print("Thread exit by KeyboardInterrupt")
            break

    print("socket closed")
    sock.close()

def get_config():
    config = conf_parser.get_config("LOGRECEIVER")

    global DEFAULT_HOST, DEFAULT_PORT, LOGTAG_0, LOGTAG_1
    DEFAULT_HOST = config["host_addr"]
    DEFAULT_PORT = int(config["host_port_num"])
    LOGTAG_0 = config["logtag_0"]
    LOGTAG_1 = config["logtag_1"]

if __name__ == '__main__':
    get_config()

    main(len(sys.argv), sys.argv)
