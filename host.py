import socket
import pickle
from PIL import Image
import io
import os

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1243))
s.listen(5)

clientsocket, address = s.accept()
print(f"Connection from {address} has been established.")

while True:
    d = input("What command do you want to send: ")
    msg = pickle.dumps(d)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
    clientsocket.send(msg)
    print("Command sent")

    if d == "223":
        img_count = 0
        while img_count < 10:
            full_msg = b''
            new_msg = True
            while True:
                msg = clientsocket.recv(16)
                if new_msg:
                    if len(msg) >= HEADERSIZE:
                        msglen = int(msg[:HEADERSIZE])
                        new_msg = False
                    else:
                        print("Received incomplete header")
                        break

                full_msg += msg

                if len(full_msg) - HEADERSIZE == msglen:
                    img_data = pickle.loads(full_msg[HEADERSIZE:])
                    img = Image.open(io.BytesIO(img_data))
                    img.save(f'screenshot_{img_count}.png')
                    img_count += 1
                    new_msg = True
                    full_msg = b""
        print("Received 10 screenshots. You can send another command.")