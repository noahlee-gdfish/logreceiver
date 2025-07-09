import sys
import socket
import threading
import RPi.GPIO as GPIO
import spidev
import time

DEFAULT_HOST = "192.168.219.117"
DEFAULT_PORT = 9090
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

def main(argc, argv):
    print("Trying to connect to server")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((DEFAULT_HOST, DEFAULT_PORT))
    print("Connect to server")

    if argc <= 1:
        mode = "f"
    else:
        mode = argv[1]

    sock.send(mode.encode())

    while True:
        try:
            msg = recv_data(sock)
            if msg == "":
                break

            print(msg, end='')

        except KeyboardInterrupt:
            print("Thread exit by KeyboardInterrupt")
            break

    print("socket closed")
    sock.close()

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
