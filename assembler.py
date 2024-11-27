import yaml
import sys

class Assembler:
    def __init__(self):
        self.instructions = []

    def parse_instruction(self, line):
        parts = line.split()
        command = parts[0]

        if command == "LOAD_CONST":
            a, b, c = 36, int(parts[1]), int(parts[2])
            if not (0 <= b < 2**16 and 0 <= c < 1024):  # B - 2 байта, C - 2 байта
                raise ValueError(f"Values out of range: B={b}, C={c} for LOAD_CONST")
            self.instructions.append((a, b, c, 5))  # 5 байтов для LOAD_CONST

        elif command == "READ_MEM":
            a, b, c = 55, int(parts[1]), int(parts[2])
            if not (0 <= b < 2**16 and 0 <= c < 2**16):  # B и C занимают по 2 байта
                raise ValueError(f"Addresses out of range: B={b}, C={c} for READ_MEM")
            self.instructions.append((a, b, c, 5))  # 5 байтов для READ_MEM

        elif command == "WRITE_MEM":
            a, b, c = 84, int(parts[1]), int(parts[2])
            if not (0 <= b < 2**16 and 0 <= c < 2**16):  # B и C занимают по 2 байта
                raise ValueError(f"Addresses out of range: B={b}, C={c} for WRITE_MEM")
            self.instructions.append((a, b, c, 5))  # 5 байтов для WRITE_MEM

        elif command == "BITREVERSE":
            a, b, c = 186, int(parts[1]), int(parts[2])
            if not (0 <= b < 2**16 and 0 <= c < 2**16):  # B и C занимают по 2 байта
                raise ValueError(f"Addresses out of range: B={b}, C={c} for BITREVERSE")
            self.instructions.append((a, b, c, 5))  # 5 байтов для BITREVERSE

    def assemble(self, input_file, output_file, log_file):
        with open(input_file, 'r') as f:
            lines = f.readlines()

        binary_data = bytearray()
        log_entries = []

        for line in lines:
            line = line.strip()
            if not line:
                continue
            self.parse_instruction(line)

        for instr in self.instructions:
            a, b, c, size = instr

	    # Упаковка инструкций в 5 байтов
            if size == 5:
		# Поле A — 8 бит (1 байт)
                a_byte = a.to_bytes(1, byteorder='little')
                
                if a == 36:

		   # Поле B — 13 бит
                   b_value = b & 0x1FFF  # Ограничиваем до 13 бит
                   c_value = c & 0xFFF  # Упаковываем ровно 13 бит
                
                   combined = (b_value) | (c_value << 13)

                   combined_bytes = combined.to_bytes(4, byteorder='little')

                   instruction_bytes = a_byte + combined_bytes[:4]
                   
                else:
                   b_value = b & 0xFFF  # Ограничиваем B до 12 бит
                   c_value = c & 0xFFF  # Ограничиваем C до 12 бит
                   
                   combined = (b_value) | (c_value << 12)
                   
                   combined_bytes = combined.to_bytes(4, byteorder='little')
                   
                   instruction_bytes = a_byte + combined_bytes[:4]

		# Логирование с измененной логикой вывода
                log_entry = f"Тест (A={a}, B={b}, C={c}):\n" + \
                    f"{', '.join(f'0x{byte:02X}' for byte in instruction_bytes)}"
                print(log_entry)
                log_entries.append({
		    'instruction': "LOAD_CONST" if a == 36 else
		    "READ_MEM" if a == 55 else
		    "WRITE_MEM" if a == 84 else
		    "BITREVERSE",
		    'A': a,
		    'B': b,
		    'C': c,
		    'bytes': [f"0x{byte:02X}" for byte in instruction_bytes]
		})

		# Добавление полученной последовательности байтов в итоговый бинарный файл
                binary_data.extend(instruction_bytes)


        # Запись в бинарный файл
        with open(output_file, 'wb') as f:
            f.write(binary_data)

        # Запись лога в YAML файл
        with open(log_file, 'w') as f:
            yaml.dump(log_entries, f)


# Запуск с аргументами командной строки
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 assembler.py <input_file> <output_file> <log_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        log_file = sys.argv[3]

        assembler = Assembler()
        assembler.assemble(input_file, output_file, log_file)
