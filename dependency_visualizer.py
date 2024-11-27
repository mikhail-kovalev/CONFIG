import requests
import argparse
import re
from urllib.parse import quote
import subprocess
import time


def sanitize_dependency_name(dependency):
    """
    Очищает имя зависимости, удаляя все символы после условий и версий.
    """
    return re.split(r'[<>=!;,]', dependency.split(';')[0])[0].strip()


def fetch_dependencies(package):
    """
    Получаем зависимости для пакета с PyPI, с обработкой ошибок и повторными попытками.
    """
    package_name = sanitize_dependency_name(package)
    url = f"https://pypi.org/pypi/{quote(package_name)}/json"
    retries = 3  # Количество повторных попыток
    for attempt in range(retries):
        try:
            print(f"Fetching dependencies for: {package_name}")
            response = requests.get(url)
            response.raise_for_status()  # Проверяем статус код ответа
            data = response.json()

            # Для отладки выводим весь ответ
            print("Response data from PyPI:")
            print(data)

            dependencies = data.get('info', {}).get('requires_dist', [])
            print(f"Dependencies for {package_name}: {dependencies}")
            return dependencies
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)  # Задержка перед повторной попыткой
            else:
                print(f"Failed to fetch dependencies for {package_name} after {retries} attempts.")
                return []


def generate_mermaid_graph(package_name, dependencies):
    """
    Генерирует описание графа зависимостей для Mermaid.
    """
    graph = [f"graph TD\n    {package_name}"]
    for dep in dependencies:
        sanitized_dep = sanitize_dependency_name(dep)
        sanitized_dep = sanitized_dep.replace('-', '_').replace('.', '_')  # Заменяем символы для корректного отображения
        graph.append(f"    {package_name} --> {sanitized_dep}")
    return "\n".join(graph)


def save_mermaid_graph(graph_description, output_file, path_to_visualizer):
    """
    Сохраняет граф зависимостей в файл с помощью mermaid CLI.
    """
    with open('graph.mmd', 'w') as f:
        f.write(graph_description)

    try:
        subprocess.run([path_to_visualizer, '-i', 'graph.mmd', '-o', output_file], check=True)
        print(f'Graph successfully saved to {output_file}')
    except subprocess.CalledProcessError as e:
        print(f'Error occurred while generating the graph: {e}')
        raise  # Повторно выбрасываем ошибку


def main():
    """
    Главная функция, которая обрабатывает аргументы и вызывает необходимые функции.
    """
    parser = argparse.ArgumentParser(description="Dependency Visualizer")
    parser.add_argument("--path-to-visualizer", required=True, help="Path to the Mermaid CLI visualizer (e.g., 'mmdc')")
    parser.add_argument("--package-name", required=True, help="Name of the package to analyze")
    parser.add_argument("--output-file", required=True, help="Path to save the generated dependency graph")
    parser.add_argument("--max-depth", type=int, default=1, help="Maximum depth of dependency analysis (default: 1)")
    args = parser.parse_args()

    # Получаем зависимости для основного пакета
    dependencies = fetch_dependencies(args.package_name)
    if not dependencies:
        print(f"No dependencies found for {args.package_name}.")
        return

    # Генерируем описание графа
    graph_description = generate_mermaid_graph(args.package_name, dependencies)
    print("Graph description:")
    print(graph_description)

    # Сохраняем граф
    save_mermaid_graph(graph_description, args.output_file, args.path_to_visualizer)


if __name__ == "__main__":
    main()
