import json
import os


def generate_diff(path_line):
    if os.path.exists(path_line):
        with open(path_line, "r", encoding="utf-8") as file:
            data = json.load(file)

        _, tail = os.path.split(path_line)
        print(tail)
        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print(f"Path '{path_line}' does not exist")



