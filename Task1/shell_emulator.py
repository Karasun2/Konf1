import os
import tarfile
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

class ShellEmulator:
    def __init__(self, hostname, tar_path, startup_script):
        self.hostname = hostname
        self.current_path = '/'
        self.filesystem = {}
        self.load_filesystem(tar_path)
        self.setup_gui()
        self.execute_startup_script(startup_script)

    def load_filesystem(self, tar_path):
        with tarfile.open(tar_path, 'r') as tar:
            for member in tar.getmembers():
                self.filesystem[member.name] = member

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title(f"{self.hostname} Shell Emulator")
        
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill='both')
        
        self.entry = tk.Entry(self.root)
        self.entry.bind("<Return>", self.process_command)
        self.entry.pack(fill='x')
        
        self.prompt()

    def prompt(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, f"{self.hostname}:{self.current_path}$ ")

    def process_command(self, event):
        command = self.entry.get()
        self.text_area.insert(tk.END, f"{command}\n")
        self.entry.delete(0, tk.END)
        if (command.find("$")):
            command = command[command.find(" ") + 1:]
            
        if command.startswith("ls"):
            self.ls()
        elif command.startswith("cd"):
            self.cd(command)
        elif command.startswith("head"):
            self.head(command)
        elif command.startswith("find"):
            self.find(command)
        elif command == "exit":
            self.root.quit()
        else:
            self.text_area.insert(tk.END, "Command not found\n")
        
        self.prompt()

    def ls(self):
        if (self.current_path == '/'):
            files1 = [name for name in self.filesystem if name.startswith("")]
            files = []
            for f in files1:
                if(f.find("/") == -1):
                    files.append(f)
        else:
            files = [name for name in self.filesystem if name.startswith(self.current_path)]
            files1 = []
            for f in files:
                if (f != self.current_path):
                    files1.append(f[len(self.current_path) + 1:])
            files.clear()
            for f in files1:
                if(f.find("/") == -1):
                    files.append(f)
        self.text_area.insert(tk.END, "\n".join(files) + "\n")

    def cd(self, command):
        if (command.count(" ") == 1):
            _, path = command.split()
            if path in self.filesystem:
                self.current_path = path
            elif self.current_path + "/" + path in self.filesystem:
                self.current_path += "/" + path
            elif path == "../":
                self.current_path = self.current_path[:len(self.current_path) - 1 - self.current_path.rfind('/')]
            else:
                self.text_area.insert(tk.END, "No such directory\n")
        else:
            self.current_path = '/'
            
    def head(self, command):
        _, file_name = command.split()
        if file_name in self.filesystem:
            member = self.filesystem[file_name]
            with tarfile.open(tar_path, 'r') as tar:
                f = tar.extractfile(member)
                lines = f.readlines()[:10]
                self.text_area.insert(tk.END, ''.join([line.decode() for line in lines]))
        elif self.current_path + "/" + file_name in self.filesystem:
            member = self.filesystem[self.current_path + "/" + file_name]
            with tarfile.open(tar_path, 'r') as tar:
                f = tar.extractfile(member)
                lines = f.readlines()[:10]
                self.text_area.insert(tk.END, ''.join([line.decode() for line in lines]))
        else:
            self.text_area.insert(tk.END, "No such file\n")

    def find(self, command):
        _, search_term = command.split()
        found_files = [name for name in self.filesystem.keys() if (search_term in name and not(search_term + "/" in name))]
        self.text_area.insert(tk.END, "\n".join(found_files) + "\n")

    def execute_startup_script(self, startup_script):
        if os.path.exists(startup_script):
            with open(startup_script, 'r') as file:
                for line in file:
                    self.entry.insert(len(self.current_path) + len(self.hostname) + 5, line.strip())
                    self.process_command(line.strip())

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python shell_emulator.py <hostname> <tar_path> <startup_script>")
        sys.exit(1)

    hostname = sys.argv[1]
    tar_path = sys.argv[2]
    startup_script = sys.argv[3]
    emulator = ShellEmulator(hostname, tar_path, startup_script)
    emulator.run()

