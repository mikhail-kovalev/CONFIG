Команды УВМ
LOAD_CONST — загрузка константы в память по указанному адресу.
READ_MEM — чтение значения из одного адреса памяти и запись его в другой.
WRITE_MEM — запись значения в память по заданному адресу.
BITREVERSE — выполнение побитового реверса значения по указанному адресу.

Структура проекта

assembler.py — ассемблер, который принимает текстовую программу и создаёт бинарный файл, а также лог-файл.
interpreter.py — интерпретатор, который выполняет команды УВМ из бинарного файла и сохраняет результат выполнения.
program.asm — пример входного файла с текстом программы для ассемблера.
program.bin — бинарный файл, созданный ассемблером для использования интерпретатором.
program.log — лог-файл, содержащий описание каждой команды и её байтовое представление.
result.yaml — файл с результатами выполнения программы, записанными интерпретатором.

Установка и настройка

Создайте виртуальное окружение:

В корневой папке проекта выполните следующую команду для создания виртуального окружения:


python3 -m venv myenv

Активируйте виртуальное окружение:

Для Windows:

myenv\Scripts\activate

Для macOS и Linux:

source myenv/bin/activate

Установите необходимые зависимости:

Установите библиотеку PyYAML внутри виртуального окружения:

pip install pyyaml


Использование

1. Ассемблирование программы
Ассемблер принимает текстовый файл программы и создаёт бинарный файл для интерпретатора. Также он создаёт лог-файл с описанием команд в формате YAML.

Команда для запуска ассемблера:

python3 assembler.py program.asm program.bin program.log

<input_file> — путь к текстовому файлу с программой (например, program.asm).
<output_file> — путь к выходному бинарному файлу (например, program.bin).
<log_file> — путь к лог-файлу в формате YAML (например, program.log).

2. Выполнение программы на интерпретаторе
Интерпретатор выполняет команды из бинарного файла и сохраняет результат выполнения в выходной файл.

Команда для запуска интерпретатора:

python3 interpreter.py program.bin result.yaml 0 10

<input_file> — путь к бинарному файлу с программой (например, program.bin).
<output_file> — путь к файлу с результатами выполнения (например, result.yaml).
<memory_start> — начальный адрес диапазона памяти, который нужно сохранить в выходном файле.
<memory_end> — конечный адрес диапазона памяти, который нужно сохранить в выходном файле.