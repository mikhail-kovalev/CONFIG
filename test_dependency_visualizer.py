import unittest
from unittest.mock import patch, MagicMock
import subprocess
import os
import dependency_visualizer  # Импортируйте ваш модуль

class TestDependencyVisualizer(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_dependencies_with_dependencies(self, mock_run):
        # Настраиваем возврат для вызова subprocess.run
        mock_run.return_value.stdout = 'Requires: dep1, dep2\nName: example'
        dependencies = dependency_visualizer.get_dependencies('example', 1)
        expected = {'example': ['dep1', 'dep2'], 'dep1': ['dep1', 'dep2'], 'dep2': ['dep1', 'dep2']}
        self.assertEqual(dependencies, expected)

    @patch('subprocess.run')
    def test_get_dependencies_without_dependencies(self, mock_run):
        mock_run.return_value.stdout = 'Name: package_without_deps'
        dependencies = dependency_visualizer.get_dependencies('package_without_deps', 1)
        expected = {'package_without_deps': []}
        self.assertEqual(dependencies, expected)

    @patch('subprocess.run')
    def test_get_dependencies_with_non_existing_package(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, 'pip show')
        dependencies = dependency_visualizer.get_dependencies('non_existing_package', 1)
        expected = {}
        self.assertEqual(dependencies, expected)

    def test_create_mermaid_graph(self):
        dependencies = {'example': ['dep1', 'dep2'], 'dep1': [], 'dep2': []}
        graph = dependency_visualizer.create_mermaid_graph(dependencies)
        expected_graph = 'graph TD\n    example --> dep1\n    example --> dep2'
        self.assertEqual(graph, expected_graph)

    @patch('subprocess.run')
    @patch('os.remove')
    def test_save_mermaid_graph(self, mock_remove, mock_run):
        mock_run.return_value = MagicMock()
        graph_description = 'graph TD\n    example --> dep1\n    example --> dep2'
        output_file = 'output.png'
        path_to_visualizer = 'mmdc'

        # Тестируем успешное выполнение
        dependency_visualizer.save_mermaid_graph(graph_description, output_file, path_to_visualizer)
        mock_run.assert_called_once_with([path_to_visualizer, '-i', 'graph.mmd', '-o', output_file], check=True)

        # Тестируем удаление файла
        mock_remove.assert_called_once_with('graph.mmd')

    @patch('subprocess.run')
    def test_save_mermaid_graph_error(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, 'mmdc error')
        graph_description = 'graph TD\n    example --> dep1\n    example --> dep2'
        output_file = 'output.png'
        path_to_visualizer = 'mmdc'

        with self.assertRaises(subprocess.CalledProcessError):
            dependency_visualizer.save_mermaid_graph(graph_description, output_file, path_to_visualizer)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('dependency_visualizer.get_dependencies')
    @patch('dependency_visualizer.create_mermaid_graph')
    @patch('dependency_visualizer.save_mermaid_graph')
    def test_main(self, mock_save, mock_create, mock_get, mock_parse):
        mock_parse.return_value = MagicMock(path_to_visualizer='mmdc', package_name='example', output_file='output.png', max_depth=3)
        mock_get.return_value = {'example': ['dep1', 'dep2']}
        mock_create.return_value = 'graph TD\n    example --> dep1\n    example --> dep2'

        # Вызов функции main
        dependency_visualizer.main()

        mock_get.assert_called_once_with('example', 3)
        mock_create.assert_called_once()
        mock_save.assert_called_once_with('graph TD\n    example --> dep1\n    example --> dep2', 'output.png', 'mmdc')

if __name__ == '__main__':
    unittest.main()
