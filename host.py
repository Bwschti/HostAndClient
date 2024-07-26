import socket
import pickle
import os

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.2', 1243))  # Replace with the IP address of the host machine

while True:
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print("new msg len:", msg[:HEADERSIZE])
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        print(f"full message length: {msglen}")

        full_msg += msg

        print(len(full_msg))

        if len(full_msg) - HEADERSIZE == msglen:
            print("full msg recvd")
            command = pickle.loads(full_msg[HEADERSIZE:])
            print(command)
            if command == "213":
                if os.name == 'nt':  # Windows
                    os.system("shutdown /s /t 1")
                elif os.name == 'posix':  # Linux
                    os.system("shutdown now")
            new_msg = True
            full_msg = b""