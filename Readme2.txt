1. Установка необходимых библиотек

Перед началом работы убедитесь, что у вас установлен Python (рекомендуется версия 3.7 и выше) и pip.

Установка pipdeptree

Запустите команду:

pip install pipdeptree

2. Установка Mermaid

Для macOS

Для установки Mermaid на macOS используйте Homebrew:

brew install mermaid

Для Windows

Для установки Mermaid на Windows:

1. Убедитесь, что у вас установлен Node.js. Если он не установлен, скачайте и установите его с [официального сайта Node.js](https://nodejs.org/).
   
2. Установите Mermaid CLI с помощью npm:

npm install -g @mermaid-js/mermaid-cli


3. Использование проекта

После установки необходимых библиотек и Mermaid вы можете использовать проект для визуализации зависимостей.


Пример использования

Запустите скрипт `dependency_visualizer.py` с параметрами:

python dependency_visualizer.py --path-to-visualizer <путь к mermaid CLI> --package-name <имя пакета> --output-file <имя выходного файла> --max-depth <максимальная глубина>

Пример:

python dependency_visualizer.py --path-to-visualizer /opt/homebrew/bin/mmdc --package-name numpy --output-file numpy_dependencies.png --max-depth 3


4. Примечания

- Убедитесь, что указанный путь к Mermaid CLI (`<путь к mermaid CLI>`) корректен для вашей системы.
- В случае ошибок проверьте, правильно ли указаны параметры и установлены ли все зависимости.

5. (Дополнительно) Удаление виртуального окружения
deactivate  # Для выхода из виртуального окружения
rm -rf venv  # Для удаления виртуального окружения
