Задание: Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу 
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС. 
Эмулятор должен запускаться из реальной командной строки, а файл с 
виртуальной файловой системой не нужно распаковывать у пользователя. 
Эмулятор принимает образ виртуальной файловой системы в виде файла формата 
tar. Эмулятор должен работать в режиме GUI.

Основные компоненты кода
Импорт библиотек:

    import os
    import tarfile
    import tkinter as tk
    from tkinter import scrolledtext
    from tkinter import messagebox
    os: используется для работы с файловой системой.
    tarfile: используется для работы с TAR-архивами.
    tkinter: используется для создания графического интерфейса.
    scrolledtext: предоставляет текстовую область с прокруткой.
    messagebox: используется для отображения сообщений пользователю.
Класс ShellEmulator:
Этот класс инкапсулирует функциональность эмулятора оболочки.

    __init__: Конструктор класса, который инициализирует хостнейм, текущий путь и загружает файловую систему из TAR-архива.

    def __init__(self, hostname, tar_path, startup_script):
        self.hostname = hostname
        self.current_path = '/'
        self.filesystem = {}
        self.load_filesystem(tar_path)
        self.setup_gui()
        self.execute_startup_script(startup_script)
    
    load_filesystem: Загружает содержимое TAR-архива в словарь self.filesystem.
    def load_filesystem(self, tar_path):
        with tarfile.open(tar_path, 'r') as tar:
            for member in tar.getmembers():
                self.filesystem[member.name] = member

    setup_gui: Настраивает графический интерфейс.
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title(f"{self.hostname} Shell Emulator")
    
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill='both')
    
        self.entry = tk.Entry(self.root)
        self.entry.bind("<Return>", self.process_command)
        self.entry.pack(fill='x')
    
        self.prompt()

    prompt: Обновляет текстовое поле ввода, отображая текущий путь и хостнейм.
    def prompt(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, f"{self.hostname}:{self.current_path}$ ")

    process_command: Обрабатывает введенную пользователем команду.
    def process_command(self, event):
        command = self.entry.get()
        self.text_area.insert(tk.END, f"{command}\n")
        self.entry.delete(0, tk.END)
        ...

Команды эмулятора:
ls: Показать файлы в текущем каталоге.
cd: Перейти в указанную директорию.
head: Показать первые 10 строк указанного файла.
find: Найти файлы, содержащие указанный термин.
exit: Закрыть эмулятор.
Каждая из этих команд реализована в соответствующих методах класса.

Методы для выполнения команд:

ls: Выводит список файлов и директорий в текущем каталоге.
cd: Изменяет текущий путь на указанный.
head: Читает и выводит первые 10 строк указанного файла.
find: Ищет файлы по заданному шаблону.
execute_startup_script: Выполняет команды из стартового скрипта, если файл существует.

    def execute_startup_script(self, startup_script):
        if os.path.exists(startup_script):
            with open(startup_script, 'r') as file:
                for line in file:
                    self.entry.insert(len(self.current_path) + len(self.hostname) + 5, line.strip())
                    self.process_command(line.strip())

Запуск приложения:
В блоке if __name__ == "__main__": код проверяет количество аргументов командной строки и инициализирует эмулятор.

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

Команда сборки:

    python shell_emulator.py localhost my_filesystem.tar startup_script.txt
