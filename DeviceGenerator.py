import platform
import time
import binascii
import random
import os
import requests
import subprocess
import re
import tkinter as tk
from tkinter import messagebox
from pathlib import Path


def getrandommc():
    mcrandom = ["a", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    mc = '{}:{}:{}:{}:{}:{}'.format("".join(random.choices(mcrandom, k=2)), "".join(random.choices(mcrandom, k=2)),
                                    "".join(random.choices(mcrandom, k=2)), "".join(random.choices(mcrandom, k=2)),
                                    "".join(random.choices(mcrandom, k=2)), "".join(random.choices(mcrandom, k=2)))
    return mc


def getsystem():
    system = platform.system()
    if system.startswith("Win"):
        return "win" + platform.machine()[-2:]
    elif system.startswith("Lin"):
        return "linux" + platform.machine()[-2:]
    else:
        return "osx64"


def copy_to_clipboard(content):
    root.clipboard_clear()
    root.clipboard_append(content)
    messagebox.showinfo("Copied", "Content copied to clipboard!")


def generate_device():
    system = getsystem()

    nativate_path = Path(__file__).resolve().parent / "Libs"
    jni_path = nativate_path / "prebuilt" / system
    
    os.chdir(nativate_path)

    headers = {
        'user-agent': 'com.zhiliaoapp.musically/2023105030',
        'content-type': 'application/octet-stream;tt-data=a'
    }

    gentime = str(int(time.time() * 1000))
    ud_id = str(random.randint(221480502743165, 821480502743165))
    openu_did = "".join([random.choice("0123456789abcdef")
                         for i in range(16)])
    mc = getrandommc()

    message = " ".join([gentime, ud_id, openu_did, mc])

    command = r"java -jar -Djna.library.path={} -Djava.library.path={} unidbg.jar {}".format(jni_path, jni_path, message)
    stdout, stderr = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    hex_str = re.search(r'hex=([\s\S]*?)\nsize', stdout.decode()).group(1)

    def hexStrtostr(hex_str):
        hexadecimal = hex_str.encode('utf-8')
        str_bin = binascii.unhexlify(hexadecimal)
        return str_bin

    astr = hexStrtostr(hex_str)

    register = 'https://log-va.tiktokv.com/service/2/device_register/'
    with requests.session() as s:
        response = s.post(register, data=astr, headers=headers).json()
    openudid.set(openu_did)
    device_id.set(response['device_id'])
    iid.set(response['install_id'])


# Initialize the main window
root = tk.Tk()
root.title("Device Generator")

# Variables to hold the generated data
openudid = tk.StringVar()
device_id = tk.StringVar()
iid = tk.StringVar()

# Create a LabelFrame to group the output fields
output_frame = tk.LabelFrame(root, text="Generated Device Information", padx=10, pady=10)
output_frame.grid(row=0, column=0, padx=10, pady=10)

# OpenUDID
tk.Label(output_frame, text="OpenUDID:").grid(row=0, column=0, sticky=tk.W)
openudid_entry = tk.Entry(output_frame, textvariable=openudid, width=50, state="readonly")
openudid_entry.grid(row=0, column=1)
copy_openudid_button = tk.Button(output_frame, text="Copy", command=lambda: copy_to_clipboard(openudid.get()))
copy_openudid_button.grid(row=0, column=2)

# Device ID
tk.Label(output_frame, text="Device ID:").grid(row=1, column=0, sticky=tk.W)
device_id_entry = tk.Entry(output_frame, textvariable=device_id, width=50, state="readonly")
device_id_entry.grid(row=1, column=1)
copy_device_id_button = tk.Button(output_frame, text="Copy", command=lambda: copy_to_clipboard(device_id.get()))
copy_device_id_button.grid(row=1, column=2)

# IID
tk.Label(output_frame, text="IID:").grid(row=2, column=0, sticky=tk.W)
iid_entry = tk.Entry(output_frame, textvariable=iid, width=50, state="readonly")
iid_entry.grid(row=2, column=1)
copy_iid_button = tk.Button(output_frame, text="Copy", command=lambda: copy_to_clipboard(iid.get()))
copy_iid_button.grid(row=2, column=2)

# Generate button
generate_button = tk.Button(root, text="Generate Device", command=generate_device)
generate_button.grid(row=1, column=0, pady=10)

# Run the application
root.mainloop()