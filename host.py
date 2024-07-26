import socket
import pickle
from PIL import Image
import io

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1243))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    d = input("What command do you want to send : ")
    msg = pickle.dumps(d)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
    clientsocket.send(msg)
    print("Command sent")

    if d == "223":
        while True:
            full_msg = b''
            new_msg = True
            while True:
                msg = clientsocket.recv(16)
                if new_msg:
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                full_msg += msg

                if len(full_msg) - HEADERSIZE == msglen:
                    img_data = pickle.loads(full_msg[HEADERSIZE:])
                    img = Image.open(io.BytesIO(img_data))
                    img.show()
                    new_msg = True
                    full_msg = b""