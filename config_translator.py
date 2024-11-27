import json
import re
import sys

class ConfigTranslator:
    def __init__(self):
        self.constants = {}

    def validate_name(self, name):
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', name):
            raise ValueError(f"Invalid name format: {name}")
        return name

    def parse_constant(self, name, value):
        name = self.validate_name(name)  # Validate the name format
        if isinstance(value, int) or isinstance(value, str):
            self.constants[name] = value
        elif isinstance(value, list):
            self.constants[name] = self.parse_list(value)
        else:
            raise ValueError(f"Unsupported constant value: {value}")

    def parse_list(self, items):
        parsed_items = [self.parse_value(item) for item in items]
        return f"list({', '.join(parsed_items)})"

    def parse_value(self, value):
        if isinstance(value, int):
            return str(value)
        elif isinstance(value, str):
            return f"[[{value}]]"
        elif isinstance(value, list):
            return self.parse_list(value)
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    def concat(self, *args):
        return ''.join(str(self.constants.get(arg, arg)) for arg in args)

    def ord_func(self, arg):
        value = self.constants.get(arg, arg)
        if isinstance(value, str) and len(value) > 0:
            return ord(value[0])
        raise ValueError(f"ord() requires a non-empty string, got: {value}")

    def parse_expression(self, expr):
        match = re.match(r'\$\{([+\-*]|concat|ord)\s+([^\}]+)\}', expr)
        if not match:
            raise ValueError(f"Invalid expression format: {expr}")

        op, args = match.groups()
        args = args.split()

        def resolve_value(arg):
            if arg in self.constants:
                return self.constants[arg]
            elif arg.isdigit():
                return int(arg)
            else:
                raise ValueError(f"Undefined constant or invalid value: {arg}")

        if op == '+':
            return resolve_value(args[0]) + resolve_value(args[1])
        elif op == '-':
            return resolve_value(args[0]) - resolve_value(args[1])
        elif op == '*':
            return resolve_value(args[0]) * resolve_value(args[1])
        elif op == "concat":
            return self.concat(*args)
        elif op == "ord":
            return self.ord_func(args[0])
        else:
            raise ValueError(f"Unsupported operation: {op}")


    def translate(self, config):
        output = ""

        # Однострочные комментарии
        if "comment" in config:
            output += f"|| {config['comment']}\n"

        # Многострочные комментарии
        if "multi_comment" in config:
            output += "=begin\n"
            for line in config["multi_comment"]:
                output += f"{line}\n"
            output += "=cut\n"

        # Обработка констант
        if "const" in config:
            for name, value in config["const"].items():
                self.parse_constant(name, value)  # Добавление в self.constants
                if isinstance(value, int):
                    output += f"const {name} = {value}\n"
                elif isinstance(value, str):
                    output += f"const {name} = [[{value}]]\n"
                elif isinstance(value, list):
                    list_values = ', '.join(map(str, value))
                    output += f"const {name} = list({list_values})\n"

        # Обработка массивов
        if "array_value" in config:
            output += f"array_value = {config['array_value']}\n"

        # Выражения
        if "expression_addition" in config:
            result = self.parse_expression(config["expression_addition"])
            output += f"expression_addition = {result}\n"

        if "expression_subtraction" in config:
            result = self.parse_expression(config["expression_subtraction"])
            output += f"expression_subtraction = {result}\n"

        if "expression_multiplication" in config:
            result = self.parse_expression(config["expression_multiplication"])
            output += f"expression_multiplication = {result}\n"

        # Конкатенация
        if "concat_example" in config:
            match = re.match(r'\$\{concat\s+(.+)\}', config["concat_example"])
            if match:
                args = match.group(1).split()
                result = self.concat(*args)
                output += f"concat_example = [[{result}]]\n"

        # Функция ord()
        if "ord_example" in config:
            match = re.match(r'\$\{ord\s+(\w+)\}', config["ord_example"])
            if match:
                arg = match.group(1)
                result = self.ord_func(arg)
                output += f"ord_example = {result}\n"

        return output



def main():
    input_data = json.load(sys.stdin)
    output_path = sys.argv[1] if len(sys.argv) > 1 else "output.txt"

    translator = ConfigTranslator()
    translated_text = translator.translate(input_data)

    with open(output_path, 'w') as output_file:
        output_file.write(translated_text)
        print(f"Configuration saved to {output_path}")

if __name__ == "__main__":
    main()