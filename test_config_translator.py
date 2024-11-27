import unittest
import re
import json
class ConfigTranslator:
    def translate(self, config, include_constants=False):
        output = ""

        # Обработка комментариев
        if "comment" in config:
            output += f"|| {config['comment']}\n"

        if "multi_comment" in config:
            output += "=begin\n"
            for line in config["multi_comment"]:
                output += f"{line}\n"
            output += "=cut\n"

        # Обработка констант (включается, если include_constants=True)
        if include_constants and "const" in config:
            for name, value in config["const"].items():
                if isinstance(value, int):
                    output += f"const {name} = {value}\n"
                elif isinstance(value, str):
                    output += f"const {name} = [[{value}]]\n"

        # Обработка выражений
        if "expression_addition" in config:
            expr = config["expression_addition"]
            match = re.match(r'\$\{\+\s+(\w+)\s+(\w+)\}', expr)
            if match:
                num1, num2 = match.groups()
                result = config["const"].get(num1, 0) + config["const"].get(num2, 0)
                output += f"expression result = {result}\n"

        if "expression_subtraction" in config:
            expr = config["expression_subtraction"]
            match = re.match(r'\$\{\-\s+(\w+)\s+(\w+)\}', expr)
            if match:
                num2, num1 = match.groups()
                result = config["const"].get(num2, 0) - config["const"].get(num1, 0)
                output += f"expression_subtraction = {result}\n"

        if "expression_multiplication" in config:
            expr = config["expression_multiplication"]
            match = re.match(r'\$\{\*\s+(\w+)\s+(\d+)\}', expr)
            if match:
                num1, multiplier = match.groups()
                result = config["const"].get(num1, 0) * int(multiplier)
                output += f"expression_multiplication = {result}\n"

        # Обработка конкатенации строк
        if "concat_example" in config:
            expr = config["concat_example"]
            match = re.match(r'\$\{concat\s+(\w+)\s+(\w+)\}', expr)
            if match:
                str1, str2 = match.groups()
                result = config["const"].get(str1, "") + config["const"].get(str2, "")
                output += f"concat_example = [[{result}]]\n"

        # Обработка функции ord
        if "ord_example" in config:
            expr = config["ord_example"]
            match = re.match(r'\$\{ord\s+(\w+)\}', expr)
            if match:
                str1 = match.group(1)
                result = ord(config["const"].get(str1, "")[0])
                output += f"ord_example = {result}\n"

        return output

class TestConfigTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = ConfigTranslator()

    def test_expression_addition(self):
        input_data = {
            "const": {
                "num1": 10,
                "num2": 20
            },
            "expression_addition": "${+ num1 num2}"
        }
        expected_output = "expression result = 30\n"
        result = self.translator.translate(input_data)
        self.assertEqual(result, expected_output)

    def test_expression_subtraction(self):
        input_data = {
            "const": {
                "num1": 10,
                "num2": 20
            },
            "expression_subtraction": "${- num2 num1}"
        }
        expected_output = "expression_subtraction = 10\n"
        result = self.translator.translate(input_data)
        self.assertEqual(result, expected_output)

    def test_expression_multiplication(self):
        input_data = {
            "const": {
                "num1": 10
            },
            "expression_multiplication": "${* num1 2}"
        }
        expected_output = "expression_multiplication = 20\n"
        result = self.translator.translate(input_data)
        self.assertEqual(result, expected_output)

    def test_concat_example(self):
        input_data = {
            "const": {
                "str1": "Hello",
                "str2": "World"
            },
            "concat_example": "${concat str1 str2}"
        }
        expected_output = "concat_example = [[HelloWorld]]\n"
        result = self.translator.translate(input_data)
        self.assertEqual(result, expected_output)

    def test_ord_example(self):
        input_data = {
            "const": {
                "str1": "Hello"
            },
            "ord_example": "${ord str1}"
        }
        expected_output = "ord_example = 72\n"
        result = self.translator.translate(input_data)
        self.assertEqual(result, expected_output)

    def test_full_configuration(self):
        input_data = {
            "comment": "Это комментарий",
            "multi_comment": ["Многострочный комментарий", "Продолжение"],
            "const": {
                "str1": "Hello",
                "str2": "World",
                "num1": 10,
                "num2": 20
            },
            "expression_addition": "${+ num1 num2}",
            "expression_subtraction": "${- num2 num1}",
            "expression_multiplication": "${* num1 2}",
            "concat_example": "${concat str1 str2}",
            "ord_example": "${ord str1}"
        }
        expected_output = (
            "|| Это комментарий\n"
            "=begin\nМногострочный комментарий\nПродолжение\n=cut\n"
            "const str1 = [[Hello]]\n"
            "const str2 = [[World]]\n"
            "const num1 = 10\n"
            "const num2 = 20\n"
            "expression result = 30\n"
            "expression_subtraction = 10\n"
            "expression_multiplication = 20\n"
            "concat_example = [[HelloWorld]]\n"
            "ord_example = 72\n"
        )
        result = self.translator.translate(input_data, include_constants=True)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()