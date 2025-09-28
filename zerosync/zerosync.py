import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
import subprocess
from datetime import datetime
from PIL import Image, ImageTk
import sys
import ctypes
import threading
import pystray
from pystray import MenuItem as item
from PIL import Image as PILImage

APP_NAME = "ZeroSync"
APPDATA_PATH = os.path.join(os.getenv('APPDATA'), APP_NAME)
os.makedirs(APPDATA_PATH, exist_ok=True)

PERMANENT_SOURCE = os.path.join(APPDATA_PATH, "permanent_sources.json")
PERMANENT_BACKUP = os.path.join(APPDATA_PATH, "permanent_backups.json")
PERMANENT_EXCLUDE = os.path.join(APPDATA_PATH, "permanent_excludes.json")

TRAY_ICON_PATH = os.path.join(os.path.dirname(sys.argv[0]), "icon.ico")

# Request Admin Privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    sys.exit()

def show_splash():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.configure(bg="black")

    width, height = 300, 300
    screen_w = splash.winfo_screenwidth()
    screen_h = splash.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    splash.geometry(f"{width}x{height}+{x}+{y}")

    try:
        img_path = os.path.join(os.path.dirname(sys.argv[0]), "logo.png")
        img = Image.open(img_path).resize((200, 200), Image.LANCZOS)
        logo = ImageTk.PhotoImage(img)
        tk.Label(splash, image=logo, bg="black").pack(expand=True)
        splash.image = logo
    except:
        tk.Label(splash, text="deathesther", font=("Segoe UI", 24), bg="black", fg="white").pack(expand=True)

    splash.after(2000, splash.destroy)
    splash.mainloop()

class ZeroSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("600x580")
        self.root.configure(bg="#f4f4f4")
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.source_frames = []
        self.backup_frames = []
        self.exclude_frames = []

        self.build_ui()
        self.load_permanent_paths()
        self.init_tray_icon()

    def init_tray_icon(self):
        try:
            image = PILImage.open(TRAY_ICON_PATH)
            menu = (item('Show', self.show_window), item('Exit', self.quit_app))
            self.tray_icon = pystray.Icon(APP_NAME, image, menu=menu)
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
        except Exception as e:
            print("[TrayIcon Error]", e)

    def hide_window(self):
        self.root.withdraw()

    def show_window(self, icon=None, item=None):
        self.root.after(0, self.root.deiconify)

    def quit_app(self):
        self.tray_icon.stop()
        self.root.destroy()

    def build_ui(self):
        def create_section(title, add_command):
            tk.Label(self.root, text=title, bg="#f4f4f4", font=("Segoe UI", 10, "bold")).pack(pady=(10, 5), padx=12, anchor='w')
            frame = tk.Frame(self.root, bg="#f4f4f4")
            frame.pack(padx=12, anchor='w', fill='x')
            btn = tk.Button(self.root, text=f"Add New {title.split()[0]}", command=add_command,
                            font=("Segoe UI", 9, "bold"), bg="#d9d9d9", relief="ridge", padx=10, pady=4, bd=0)
            btn.pack(pady=(0, 10))
            self.add_hover_effect(btn)
            return frame

        self.source_container = create_section("Source Locations", self.add_source_entry)
        self.backup_container = create_section("Backup Locations", self.add_backup_entry)
        self.exclude_container = create_section("Excluded Folders", self.add_exclude_entry)

        backup_btn = tk.Button(self.root, text="Start Backup", command=self.start_backup,
                               font=("Segoe UI", 11, "bold"), bg="#4CAF50", fg="white",
                               padx=20, pady=10, relief="flat", bd=0)
        backup_btn.pack(pady=20)
        self.add_hover_effect(backup_btn)

        footer = tk.Frame(self.root, bg="#f4f4f4")
        footer.pack(side='bottom', fill='x', pady=10)
        tk.Label(footer, text="© deathesther", font=("Segoe UI", 8), bg="#f4f4f4", fg="#888").pack(side='left', padx=10)
        cybrotech = tk.Label(footer, text="cybrotech", font=("Segoe UI", 8, "underline"), fg="#0066cc", cursor="hand2", bg="#f4f4f4")
        cybrotech.pack(side='right', padx=10)
        cybrotech.bind("<Button-1>", lambda e: os.system("start https://cybrotech.us"))

    def add_hover_effect(self, widget):
        def on_enter(e): widget.config(bg="#b0e0b0" if widget.cget("text") == "Start Backup" else "#cccccc")
        def on_leave(e): widget.config(bg="#4CAF50" if widget.cget("text") == "Start Backup" else "#d9d9d9")
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def add_path_entry(self, container, path_list, path="", is_permanent=False):
        frame = tk.Frame(container, bg="#f4f4f4")
        frame.pack(pady=4, anchor='w')

        var = tk.StringVar(value=path)
        permanent_var = tk.BooleanVar(value=is_permanent)

        entry = tk.Entry(frame, textvariable=var, width=40, font=("Segoe UI", 9), relief="solid", bd=1)
        entry.pack(side='left', padx=(0, 6))

        browse_btn = tk.Button(frame, text="ADD", command=lambda: self.browse_folder(var),
                               font=("Segoe UI", 9, "bold"), bg="#a4dfa4", relief="ridge", padx=10, pady=3, bd=0)
        browse_btn.pack(side='left', padx=(0, 4))
        self.add_hover_effect(browse_btn)

        remove_btn = tk.Button(frame, text="Remove", command=lambda: self.remove_path_entry(frame, path_list),
                               font=("Segoe UI", 9, "bold"), bg="#f28b82", relief="ridge", padx=10, pady=3, bd=0)
        remove_btn.pack(side='left', padx=(0, 4))
        self.add_hover_effect(remove_btn)

        checkbox = tk.Checkbutton(frame, text="Make Permanent", variable=permanent_var, bg="#f4f4f4", command=self.save_all_permanents)
        checkbox.pack(side='left')

        path_list.append((frame, var, permanent_var))

    def add_source_entry(self, path="", is_permanent=False): self.add_path_entry(self.source_container, self.source_frames, path, is_permanent)
    def add_backup_entry(self, path="", is_permanent=False): self.add_path_entry(self.backup_container, self.backup_frames, path, is_permanent)
    def add_exclude_entry(self, path="", is_permanent=False): self.add_path_entry(self.exclude_container, self.exclude_frames, path, is_permanent)

    def remove_path_entry(self, frame, path_list):
        for f, var, perm in path_list:
            if f == frame:
                path_list.remove((f, var, perm))
                break
        frame.destroy()
        self.save_all_permanents()

    def browse_folder(self, var):
        folder = filedialog.askdirectory()
        if folder:
            var.set(folder)

    def save_all_permanents(self):
        def extract(paths): return [var.get() for _, var, perm in paths if perm.get() and var.get().strip()]
        json.dump(extract(self.source_frames), open(PERMANENT_SOURCE, "w"))
        json.dump(extract(self.backup_frames), open(PERMANENT_BACKUP, "w"))
        json.dump(extract(self.exclude_frames), open(PERMANENT_EXCLUDE, "w"))

    def load_permanent_paths(self):
        def load_and_add(file, add_func):
            if os.path.exists(file):
                try:
                    for path in json.load(open(file)): add_func(path, True)
                except: pass
            else:
                add_func(os.path.expandvars(r"%USERPROFILE%"))

        load_and_add(PERMANENT_SOURCE, self.add_source_entry)
        load_and_add(PERMANENT_BACKUP, self.add_backup_entry)
        load_and_add(PERMANENT_EXCLUDE, self.add_exclude_entry)

    def start_backup(self):
        sources = [var.get() for _, var, _ in self.source_frames if var.get().strip()]
        backups = [var.get() for _, var, _ in self.backup_frames if var.get().strip()]
        excludes = [var.get() for _, var, _ in self.exclude_frames if var.get().strip()]

        if not sources or not backups:
            messagebox.showerror("Missing Paths", "Please provide at least one Source and one Backup location.")
            return

        timestamp = datetime.now().strftime("backup_of_%d-%m-%Y_%H-%M")

        for src in sources:
            for dst in backups:
                backup_path = os.path.join(dst, timestamp)
                os.makedirs(backup_path, exist_ok=True)
                exclude_args = []

                for e in excludes:
                    try:
                        if os.path.commonpath([src, e]) == src:
                            exclude_args += ["/XD", f'"{e}"']
                    except ValueError:
                        continue

                cmd = ["robocopy", f'"{src}"', f'"{backup_path}"', "/MIR", "/Z", "/R:3", "/W:5"] + exclude_args
                try:
                    subprocess.run(" ".join(cmd), shell=True)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to backup from {src} to {backup_path}\n{e}")
                    return

        messagebox.showinfo("Backup Completed", "Backup successfully completed!")

if __name__ == "__main__":
    show_splash()
    root = tk.Tk()
    app = ZeroSyncApp(root)
    root.mainloop()
