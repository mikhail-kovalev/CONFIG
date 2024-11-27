import struct
import sys
import yaml


class Interpreter:
    def __init__(self, memory_size=1024):
        self.memory = [0] * memory_size

    def load_constant(self, b, c):
        self.memory[c] = b
        print(f"LOAD_CONST executed: memory[{c}] = {b}")

    def read_mem(self, b, c):
        if b < len(self.memory) and c < len(self.memory):
            self.memory[c] = self.memory[b]
            print(f"READ_MEM executed: memory[{c}] = memory[{b}] = {self.memory[b]}")
        else:
            print(f"Error: Address out of bounds for READ_MEM: B={b}, C={c}")

    def write_mem(self, b, c):
        if b < len(self.memory) and c < len(self.memory):
            self.memory[b] = self.memory[c]
            print(f"WRITE_MEM executed: memory[{b}] = memory[{c}] = {self.memory[b]}")
        else:
            print(f"Error: Address out of bounds for WRITE_MEM: B={b}, C={c}")

    def bitreverse(self, b, c):
        if b < len(self.memory) and c < len(self.memory):
            self.memory[c] = int('{:08b}'.format(self.memory[b])[::-1], 2)
            print(f"BITREVERSE executed: memory[{c}] = {self.memory[c]}")
        else:
            print(f"Error: Address out of bounds for BITREVERSE: B={b}, C={c}")

    def interpret(self, input_file, output_file, memory_range):
        if memory_range[1] > len(self.memory):
            print(f"Error: Memory range {memory_range} is out of bounds.")
            return

        try:
            with open(input_file, 'rb') as f:
                binary_data = f.read()
        except FileNotFoundError:
            print(f"Error: Input file '{input_file}' not found.")
            return

        i = 0
        while i < len(binary_data):
            a = binary_data[i]
            print(f"Reading byte: A={a}, Position={i}")

            if a == 36:  # LOAD_CONST (4 байта)
               if i + 4 <= len(binary_data):  # Проверка, достаточно ли данных
        # Получаем все 4 байта команды
                  raw_data = int.from_bytes(binary_data[i:i + 4], byteorder='little')

        
        # A: первый байт (самый младший байт)
                  a = raw_data & 0xFF
        # B: биты с 8 по 19
                  b = (raw_data >> 8) & 0x1FFF  # Маска 12 бит
        # C: биты с 20 по 31
                  c = (raw_data >> 21) & 0xFFF  # Маска 12 бит

                  print(f"Command LOAD_CONST found: A={a}, B={b}, C={c}")
                  self.load_constant(b, c)
                  i += 4


            if a in {55, 84, 186}:  # READ_MEM, WRITE_MEM, BITREVERSE (5 байт)
                # Считываем 12 бит для B и 12 бит для C
                combined = int.from_bytes(binary_data[i + 1:i + 4], byteorder='little')
                b = combined & 0xFFF  # Первые 12 бит
                c = (combined >> 12) & 0xFFF  # Следующие 12 бит
                print(f"Command {['READ_MEM', 'WRITE_MEM', 'BITREVERSE'][[55, 84, 186].index(a)]} found: B={b}, C={c}")

                if a == 55:
                    self.read_mem(b, c)
                elif a == 84:
                    self.write_mem(b, c)
                elif a == 186:
                    self.bitreverse(b, c)

                i += 5

            else:
                i += 1

        result = {'memory_range': memory_range, 'values': self.memory[memory_range[0]:memory_range[1]]}

        try:
            with open(output_file, 'w') as f:
                yaml.dump(result, f)
            print(f"Result successfully written to {output_file}")
        except Exception as e:
            print(f"Error writing to output file '{output_file}': {e}")


# Запуск интерпретатора с аргументами командной строки
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 interpreter.py <input_file> <output_file> <memory_start> <memory_end>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        memory_start = int(sys.argv[3])
        memory_end = int(sys.argv[4])
        memory_range = (memory_start, memory_end)

        interpreter = Interpreter()
        interpreter.interpret(input_file, output_file, memory_range)
