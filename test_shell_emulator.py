import unittest
from shell_emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        # Инициализация ShellEmulator с тестовыми параметрами
        self.username = "test_user"
        self.zip_path = "Fs.zip"
        self.log_path = "log.csv"
        self.emulator = ShellEmulator(self.username, self.zip_path, self.log_path)

    def test_ls_command(self):
        result = self.emulator.ls()
        # Проверьте наличие нужных файлов в списке
        self.assertIn("file2.txt", result)  # Замените на актуальное имя файла
        self.assertIn("start.sh", result)   # Пример другого файла
        self.assertIn("subdir1", result)     # Проверка наличия подкаталога

    def test_cd_command_valid(self):
        # Попробуйте перейти в существующую директорию
        self.emulator.cd("subdir1")  # Замените на реальное имя директории
        self.assertEqual(self.emulator.current_directory, "/Fs/subdir1")  # Ожидаемый путь

    def test_cd_command_invalid(self):
        result = self.emulator.cd("invalid_directory")
        self.assertEqual(result, "Директория 'invalid_directory' не найдена.")

    def test_pwd_command(self):
        # Убедитесь, что pwd возвращает текущую директорию
        self.assertEqual(self.emulator.pwd(), self.emulator.current_directory)

    def test_chown_command(self):
        # Убедитесь, что команда chown работает корректно
        self.emulator.cd("subdir1")  # Переход в директорию с файлом
        result = self.emulator.chown("new_owner", "file1.txt")  # Замените на реальное имя файла
        self.assertIn("Владелец файла", result)

    def test_chown_command_invalid_file(self):
        result = self.emulator.chown("new_owner", "invalid_file.txt")
        self.assertEqual(result, "Файл 'invalid_file.txt' не найден.")

    def test_exit_command(self):
        result = self.emulator.exit()
        self.assertEqual(result, "Выход из эмулятора.")
        self.assertEqual(self.emulator.current_directory, "/")  # Проверьте, что текущая директория сбрасывается

    def test_uniq_command(self):
        self.emulator.cd("subdir1")  # Переход в директорию с файлом
        result = self.emulator.uniq("file1.txt")  # Замените на реальное имя файла
        self.assertIsInstance(result, str)  # Убедитесь, что возвращается строка

    def test_uniq_command_invalid(self):
        result = self.emulator.uniq("invalid_file.txt")
        self.assertEqual(result, "Файл 'invalid_file.txt' не найден.")

if __name__ == '__main__':
    unittest.main()
