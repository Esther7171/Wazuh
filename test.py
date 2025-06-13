import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import subprocess
import time
import win32api
import win32con
import win32security
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class StrictProtectHandler(FileSystemEventHandler):
    def __init__(self, extensions, root_path, app):
        self.extensions = extensions
        self.root_path = root_path
        self.app = app
        self.protected_files = set()
        self.scan_existing_files()

    def scan_existing_files(self):
        """Scan and protect existing files in the directory"""
        for root_dir, _, files in os.walk(self.root_path):
            for file in files:
                file_path = os.path.join(root_dir, file)
                ext = os.path.splitext(file_path)[1].lower()
                if ext in self.extensions:
                    self.protect_file(file_path)
                    self.protected_files.add(os.path.normcase(file_path))

    def protect_file(self, file_path):
        """Apply multiple protection layers to a file"""
        try:
            # Set read-only attribute
            win32api.SetFileAttributes(file_path, win32con.FILE_ATTRIBUTE_READONLY)
            
            # Remove all permissions except read
            sd = win32security.GetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION)
            dacl = win32security.ACL()
            sd.SetSecurityDescriptorDacl(1, dacl, 0)
            win32security.SetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION, sd)
            
            # Deny write and delete permissions for Everyone
            subprocess.call(f'icacls "{file_path}" /deny *S-1-1-0:(WD,DE,DC)', shell=True)
            
            # Deny access to SYSTEM and Administrators as well
            subprocess.call(f'icacls "{file_path}" /deny *S-1-5-18:(WD,DE,DC)', shell=True)
            subprocess.call(f'icacls "{file_path}" /deny *S-1-5-32-544:(WD,DE,DC)', shell=True)
            
            print(f"Protected: {file_path}")
        except Exception as e:
            print(f"Error protecting {file_path}: {str(e)}")

    def on_modified(self, event):
        if not event.is_directory:
            file_path = os.path.normcase(event.src_path)
            ext = os.path.splitext(file_path)[1].lower()
            if ext in self.extensions:
                if file_path not in self.protected_files:
                    # New file with protected extension detected
                    self.protect_file(file_path)
                    self.protected_files.add(file_path)
                    self.app.log_action(f"Protected new file: {file_path}")
                else:
                    # Existing protected file was modified
                    self.protect_file(file_path)
                    self.app.log_action(f"Re-protected modified file: {file_path}")

    def on_created(self, event):
        if not event.is_directory:
            file_path = os.path.normcase(event.src_path)
            ext = os.path.splitext(file_path)[1].lower()
            if ext in self.extensions:
                time.sleep(0.5)  # Wait for file operations to complete
                self.protect_file(file_path)
                self.protected_files.add(file_path)
                self.app.log_action(f"Protected newly created file: {file_path}")

    def on_deleted(self, event):
        if not event.is_directory:
            file_path = os.path.normcase(event.src_path)
            if file_path in self.protected_files:
                self.protected_files.remove(file_path)
                self.app.log_action(f"Detected deletion attempt: {file_path}")

    def on_moved(self, event):
        if not event.is_directory:
            src_path = os.path.normcase(event.src_path)
            dest_path = os.path.normcase(event.dest_path)
            ext = os.path.splitext(dest_path)[1].lower()
            
            if src_path in self.protected_files:
                self.protected_files.remove(src_path)
                self.app.log_action(f"Detected move/rename attempt: {src_path} -> {dest_path}")
            
            if ext in self.extensions:
                time.sleep(0.5)  # Wait for file operations to complete
                self.protect_file(dest_path)
                self.protected_files.add(dest_path)
                self.app.log_action(f"Protected moved/renamed file: {dest_path}")

class USBProtector:
    def __init__(self, root):
        self.root = root
        self.root.title("Sachet Pro - Advanced USB File Protection")
        self.root.geometry("600x500")
        self.usb_path = tk.StringVar()
        self.observer = None
        self.file_types = {
            'Word': ['.doc', '.docx'],
            'Excel': ['.xls', '.xlsx'],
            'PowerPoint': ['.ppt', '.pptx'],
            'PDF': ['.pdf'],
            'Text': ['.txt'],
            'Images': ['.jpg', '.jpeg', '.png', '.bmp'],
            'Archives': ['.zip', '.rar', '.7z']
        }
        self.check_vars = {}
        self.log_text = None
        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=10, padx=10, fill='both', expand=True)

        # USB Selection Frame
        usb_frame = ttk.LabelFrame(main_frame, text="USB Drive Selection")
        usb_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(usb_frame, text="Select USB Drive:").pack(anchor='w')
        entry_frame = ttk.Frame(usb_frame)
        entry_frame.pack(anchor='w', fill='x')
        ttk.Entry(entry_frame, textvariable=self.usb_path, width=50).pack(side=tk.LEFT, fill='x', expand=True)
        ttk.Button(entry_frame, text="Browse", command=self.browse_usb).pack(side=tk.LEFT, padx=5)

        # File Type Protection Frame
        type_frame = ttk.LabelFrame(main_frame, text="File Protection Settings")
        type_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(type_frame, text="Select file types to protect:").pack(anchor='w')
        check_frame = ttk.Frame(type_frame)
        check_frame.pack(fill='x')
        
        # Create checkboxes in two columns
        col1 = ttk.Frame(check_frame)
        col1.pack(side=tk.LEFT, fill='both', expand=True)
        col2 = ttk.Frame(check_frame)
        col2.pack(side=tk.LEFT, fill='both', expand=True)
        
        for i, (name, exts) in enumerate(self.file_types.items()):
            var = tk.BooleanVar()
            self.check_vars[name] = var
            frame = col1 if i % 2 == 0 else col2
            ttk.Checkbutton(frame, text=f"{name} ({', '.join(exts)})", variable=var).pack(anchor='w')

        # Control Buttons Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="Start Protection", command=self.start_protection).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Stop Protection", command=self.stop_protection).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log).pack(side=tk.RIGHT, padx=5)
        
        self.status = tk.Label(button_frame, text="Status: Inactive", foreground='red')
        self.status.pack(side=tk.LEFT, padx=20)

        # Log Frame
        log_frame = ttk.LabelFrame(main_frame, text="Protection Log")
        log_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.log_text.pack(fill="both", expand=True)

    def browse_usb(self):
        path = filedialog.askdirectory(title="Select USB Root")
        if path:
            self.usb_path.set(path)

    def get_extensions(self):
        selected = []
        for name, var in self.check_vars.items():
            if var.get():
                selected.extend(self.file_types[name])
        return selected

    def apply_strict_permissions(self, ext_list):
        for root_dir, _, files in os.walk(self.usb_path.get()):
            for file in files:
                file_path = os.path.join(root_dir, file)
                if os.path.splitext(file)[1].lower() in ext_list:
                    try:
                        # Set read-only attribute
                        win32api.SetFileAttributes(file_path, win32con.FILE_ATTRIBUTE_READONLY)
                        
                        # Remove all permissions except read
                        sd = win32security.GetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION)
                        dacl = win32security.ACL()
                        sd.SetSecurityDescriptorDacl(1, dacl, 0)
                        win32security.SetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION, sd)
                        
                        # Deny write and delete permissions for Everyone
                        subprocess.call(f'icacls "{file_path}" /deny *S-1-1-0:(WD,DE,DC)', shell=True)
                        
                        # Deny access to SYSTEM and Administrators as well
                        subprocess.call(f'icacls "{file_path}" /deny *S-1-5-18:(WD,DE,DC)', shell=True)
                        subprocess.call(f'icacls "{file_path}" /deny *S-1-5-32-544:(WD,DE,DC)', shell=True)
                        
                        self.log_action(f"Initial protection applied: {file_path}")
                    except Exception as e:
                        self.log_action(f"Error protecting {file_path}: {str(e)}")

    def start_protection(self):
        if not self.usb_path.get():
            messagebox.showerror("Error", "Please select a USB drive")
            return

        if not os.path.exists(self.usb_path.get()):
            messagebox.showerror("Error", "The selected path does not exist")
            return

        extensions = self.get_extensions()
        if not extensions:
            messagebox.showerror("Error", "Select at least one file type")
            return

        self.apply_strict_permissions(extensions)

        handler = StrictProtectHandler(extensions, self.usb_path.get(), self)
        self.observer = Observer()
        self.observer.schedule(handler, self.usb_path.get(), recursive=True)
        self.observer.start()

        self.status.config(text="Status: Active", foreground='green')
        self.log_action(f"Protection started for extensions: {', '.join(extensions)}")
        messagebox.showinfo("Protection Started", f"Active protection for: {', '.join(extensions)}")

    def stop_protection(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.status.config(text="Status: Inactive", foreground='red')
            self.log_action("Protection stopped")
            messagebox.showinfo("Stopped", "File protection stopped.")

    def log_action(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        print(log_entry.strip())

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    try:
        app = USBProtector(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Critical Error", f"The application encountered an error:\n{str(e)}")
        root.destroy()
