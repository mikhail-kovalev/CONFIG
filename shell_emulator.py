import os
import zipfile
from datetime import datetime
import csv


class ShellEmulator:
    def __init__(self, username, zip_path, log_path):
        self.username = username
        self.zip_path = zip_path
        self.log_path = log_path
        self.current_directory = '/Fs'  # Инициализация корневого каталога
        self.filesystem = self.load_filesystem(zip_path)  # Загрузка файловой системы

    def load_filesystem(self, zip_path):
        """Загрузить файловую систему из ZIP-файла."""
        filesystem = {}
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                print(f"Reading file: {file_name}")  # Логирование имени файла
                parts = file_name.split('/')
                current_level = filesystem

                # Создание структуры каталогов в файловой системе
                for part in parts[:-1]:  # Исключаем имя файла
                    if part not in current_level:
                        current_level[part] = {}  # Создаем новый каталог
                    current_level = current_level[part]

                # Чтение содержимого файла, если это не каталог
                if parts[-1]:  # Если это не каталог
                    try:
                        content = zip_ref.read(file_name).decode('utf-8')
                    except UnicodeDecodeError:
                        content = zip_ref.read(file_name).decode('utf-8', errors='ignore')  # Игнорирование ошибок
                    current_level[parts[-1]] = {
                        'content': content,
                        'owner': 'default_owner'  # Владельцем по умолчанию
                    }
        return filesystem

    def log_command(self, command):
        """Записывает команду в лог-файл."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, mode='a', newline='') as log_file:
            log_writer = csv.writer(log_file)
            log_writer.writerow([self.username, command, timestamp])

    def execute_command(self, command):
        self.log_command(command)
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]
        

        if cmd == 'ls':
            return self.ls()
        elif cmd == 'cd':
            return self.cd(args[0] if args else '')
        elif cmd == 'chown':
            return self.chown(args[1], args[0] if len(args) > 1 else '')
        elif cmd == 'pwd':
            return self.pwd()
        elif cmd == 'exit':
            return self.exit()
        elif cmd == 'uniq':
            return self.uniq(args[0] if args else '')
        else:
            return f"Команда '{cmd}' не поддерживается."

    def ls(self):
        current_level = self.get_current_directory()
        if current_level:
            output = []
            for item, properties in current_level.items():
                if isinstance(properties, dict):  # Проверка, что это файл или каталог
                    owner = properties.get('owner', 'Неизвестный владелец')
                    output.append(f"{item} (владелец: {owner})")
                else:
                    output.append(item)  # Это каталог, без информации о владельце
            return '\n'.join(output)
        else:
            return "Директория не найдена."


    def cd(self, path):
        if path == "..":
            if self.current_directory != '/Fs':
                self.current_directory = '/'.join(self.current_directory.strip('/').split('/')[:-1]) or '/Fs'
            return ""
    
        if path.startswith('/'):
            target = path.strip('/')
        else:
            target = '/'.join(self.current_directory.strip('/').split('/')[:-1] + [path.strip('/')])
    
        current_level = self.get_current_directory()
        if current_level is not None and target in current_level:
            self.current_directory = '/Fs/' + target  
            return ""
        else:
            return f"Директория '{path}' не найдена."


    def chown(self, new_owner, file_name):
        current_level = self.get_current_directory()
        if current_level is not None and file_name in current_level:
            current_level[file_name]['owner'] = new_owner
            return f"Владелец файла '{file_name}' изменен на '{new_owner}'."
        else:
            return f"Файл '{file_name}' не найден."

    def pwd(self):
        return self.current_directory

    def exit(self):
        self.current_directory = '/'  # Сброс на корень при выходе
        return "Выход из эмулятора."

    def uniq(self, file):
        current_level = self.get_current_directory()
        if current_level is not None and file in current_level:
            content = current_level[file]['content']
            return '\n'.join(sorted(set(content.splitlines()), key=content.splitlines().index)) if content else "Файл является двоичным."
        else:
            return f"Файл '{file}' не найден."

    def get_current_directory(self):
        current_level = self.filesystem
        for part in self.current_directory.strip('/').split('/'):
            if part:
                current_level = current_level.get(part)
                if current_level is None:
                    return None
        return current_level


# Пример использования
if __name__ == '__main__':
    username = 'test_user'
    zip_path = 'Fs.zip'
    log_path = 'log.csv'

    emulator = ShellEmulator(username, zip_path, log_path)
    while True:
        command = input(f"{username}@emulator:~$ ")
        output = emulator.execute_command(command)
        print(output)
        if command == 'exit':
            break
