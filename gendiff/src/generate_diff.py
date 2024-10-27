import json
import os


def generate_diff(path_line_1, path_line_2):

    if os.path.exists(path_line_1) and os.path.exists(path_line_2):
        with open(path_line_1, "r", encoding="utf-8") as first_file, \
            open(path_line_2, "r", encoding="utf-8") as second_file:
            data_first = json.load(first_file)
            data_second = json.load(second_file)
        
        keys_list = sorted(list(set(data_first) | set(data_second)))
        result_list = []
        for key in keys_list:
            if key in data_first and key in data_second:
                value_1 = data_first.get(key)
                value_2 = data_second.get(key)
                if value_1 == value_2:
                    string = f"    {key}: {value_1}"
                    result_list.append(string)
                elif value_1 != value_2:
                    string_1 = f"  - {key}: {value_1}"
                    result_list.append(string_1)
                    string_2 = f"  + {key}: {value_2}"
                    result_list.append(string_2)

            elif key in data_first and key not in data_second:
                value = data_first.get(key)
                string = f"  - {key}: {value}"
                result_list.append(string)

            elif key not in data_first and key in data_second:
                value = data_second.get(key)
                string = f"  + {key}: {value}"
                result_list.append(string)

    else:
        print(f"Path does not exist")

    start = "{\n"
    end = "\n}"
    result_string = f"{start}{"\n".join(result_list)}{end}"
    return result_string

