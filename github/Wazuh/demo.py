import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
import subprocess
from datetime import datetime
import webbrowser

# Files to store permanent paths
PERMANENT_SOURCE = "permanent_sources.json"
PERMANENT_BACKUP = "permanent_backups.json"
PERMANENT_EXCLUDE = "permanent_excludes.json"

# ---------- Splash Screen ----------
def show_splash():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.configure(bg="black")
    splash.geometry("400x200+600+300")
    
    label = tk.Label(splash, text="deathesther", font=("Segoe UI", 24, "bold"), fg="white", bg="black")
    label.pack(expand=True)

    splash.after(2000, splash.destroy)
    splash.mainloop()

# ---------- Main Application ----------
class ZeroSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ZeroSync")
        self.root.geometry("580x560")
        self.root.configure(bg="#f4f4f4")
        self.root.resizable(False, False)

        self.source_frames = []
        self.backup_frames = []
        self.exclude_frames = []

        self.build_ui()
        self.load_permanent_paths()

    def build_ui(self):
        def create_section(title, add_command):
            tk.Label(self.root, text=title, bg="#f4f4f4", font=("Segoe UI", 10, "bold")).pack(pady=(10, 5), padx=12, anchor='w')
            frame = tk.Frame(self.root, bg="#f4f4f4")
            frame.pack(padx=12, anchor='w', fill='x')
            add_btn = self.make_button(self.root, f"Add New {title.split()[0]}", add_command, "#d9d9d9")
            add_btn.pack(pady=(0, 10))
            return frame

        self.source_container = create_section("Source Locations", self.add_source_entry)
        self.backup_container = create_section("Backup Locations", self.add_backup_entry)
        self.exclude_container = create_section("Excluded Folders", self.add_exclude_entry)

        start_btn = self.make_button(
            self.root,
            "Start Backup",
            self.start_backup,
            "#4CAF50",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=10
        )
        start_btn.pack(pady=20)

        # Footer and link
        footer = tk.Frame(self.root, bg="#f4f4f4")
        footer.pack(fill='x', side='bottom', pady=10)

        copy = tk.Label(footer, text="© deathesther", bg="#f4f4f4", anchor="w", font=("Segoe UI", 8))
        copy.pack(side='left', padx=10)

        link = tk.Label(footer, text="cybrotech", fg="blue", cursor="hand2", bg="#f4f4f4", anchor="e", font=("Segoe UI", 8, "underline"))
        link.pack(side='right', padx=10)
        link.bind("<Button-1>", lambda e: webbrowser.open("https://cybrotech.us"))

    def make_button(self, parent, text, command, bg, fg="black", font=("Segoe UI", 9, "bold"), padx=10, pady=4):
        btn = tk.Button(parent, text=text, command=command, bg=bg, fg=fg, font=font, relief="ridge", padx=padx, pady=pady, bd=0)
        btn.bind("<Enter>", lambda e: btn.config(bg="#bfbfbf"))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    def add_path_entry(self, container, path_list, path="", is_permanent=False):
        frame = tk.Frame(container, bg="#f4f4f4")
        frame.pack(pady=4, anchor='w')

        var = tk.StringVar(value=path)
        permanent_var = tk.BooleanVar(value=is_permanent)

        entry = tk.Entry(frame, textvariable=var, width=40, font=("Segoe UI", 9), relief="solid", bd=1)
        entry.pack(side='left', padx=(0, 6))

        browse_btn = self.make_button(frame, "ADD", lambda: self.browse_folder(var), "#a4dfa4", padx=8)
        browse_btn.pack(side='left', padx=(0, 4))

        remove_btn = self.make_button(frame, "Remove", lambda: self.remove_path_entry(frame, path_list), "#f28b82", padx=8)
        remove_btn.pack(side='left', padx=(0, 4))

        checkbox = tk.Checkbutton(frame, text="Make Permanent", variable=permanent_var, bg="#f4f4f4", command=self.save_all_permanents)
        checkbox.pack(side='left')

        path_list.append((frame, var, permanent_var))

    def add_source_entry(self, path="", is_permanent=False):
        self.add_path_entry(self.source_container, self.source_frames, path, is_permanent)

    def add_backup_entry(self, path="", is_permanent=False):
        self.add_path_entry(self.backup_container, self.backup_frames, path, is_permanent)

    def add_exclude_entry(self, path="", is_permanent=False):
        self.add_path_entry(self.exclude_container, self.exclude_frames, path, is_permanent)

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
        def extract(paths):
            return [var.get() for _, var, perm in paths if perm.get() and var.get().strip()]

        json.dump(extract(self.source_frames), open(PERMANENT_SOURCE, "w"))
        json.dump(extract(self.backup_frames), open(PERMANENT_BACKUP, "w"))
        json.dump(extract(self.exclude_frames), open(PERMANENT_EXCLUDE, "w"))

    def load_permanent_paths(self):
        def load_and_add(file, add_func):
            if os.path.exists(file):
                try:
                    paths = json.load(open(file))
                    for path in paths:
                        add_func(path, is_permanent=True)
                except Exception as e:
                    print(f"Error loading {file}:", e)
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
                            exclude_args.extend(["/XD", e])
                    except ValueError:
                        continue

                cmd = ["robocopy", src, backup_path, "/MIR", "/Z", "/R:3", "/W:5"] + exclude_args

                try:
                    subprocess.run(cmd, shell=True)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to backup from {src} to {backup_path}\n{e}")
                    return

        messagebox.showinfo("Backup Completed", "Backup successfully completed!")

# ---------- Entry Point ----------
if __name__ == "__main__":
    show_splash()
    root = tk.Tk()
    app = ZeroSyncApp(root)
    root.mainloop()
