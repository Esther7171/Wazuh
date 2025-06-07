import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def run_as_admin(command):
    try:
        subprocess.run(["powershell", "-Command", command], shell=True)
        messagebox.showinfo("Success", "Operation completed.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def disable_usb():
    command = r"Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\USBSTOR' -Name Start -Value 4"
    run_as_admin(command)

def enable_usb():
    command = r"Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\USBSTOR' -Name Start -Value 3"
    run_as_admin(command)

def disable_ethernet():
    command = r"Disable-NetAdapter -Name '*Ethernet*' -Confirm:$false"
    run_as_admin(command)

def enable_ethernet():
    command = r"Enable-NetAdapter -Name '*Ethernet*' -Confirm:$false"
    run_as_admin(command)

def enable_all():
    enable_usb()
    enable_ethernet()

# GUI setup
root = tk.Tk()
root.title("Port Control Panel")

tk.Button(root, text="Disable USB", width=25, command=disable_usb).pack(pady=10)
tk.Button(root, text="Disable Ethernet", width=25, command=disable_ethernet).pack(pady=10)
tk.Button(root, text="Enable All", width=25, command=enable_all).pack(pady=10)

root.mainloop()
