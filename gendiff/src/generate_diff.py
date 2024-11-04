import os
import json
import yaml


def translating_to_a_string(dct, counter):
    lst = []
    if isinstance(dct, dict):
        for k, v in dct.items():
            if isinstance(v, dict):
                v = translating_to_a_string(v, counter + 1)
            st = f"{"    " * (counter + 1)}{k}: {v}"
            lst.append(st)
    return f"{{\n{",\n".join(lst)}\n{"    " * counter}}}"


def format_stylish(result_list, counter=1):
    collection_for_result_string = []
    for row in result_list:
        match row[0]:
            case "update":
                if isinstance(row[1][1], list):
                    string = (f"{"    " * counter}{row[1][0]}: "
                              f"{format_stylish(row[1][1], counter + 1)}")
                else:
                    key, value_first, value_second = row[1]
                    if isinstance(value_first, dict):
                        value_first = translating_to_a_string(value_first,
                                                              counter)
                        string = (f"{"    " * (counter - 1) + "  - "}{key}: "
                                  f"{value_first}\n"
                                  f"{"    " * (counter - 1) + "  + "}"
                                  f"{key}: {value_second}")
                    if isinstance(value_second, dict):
                        value_second = translating_to_a_string(value_second,
                                                               counter)
                        string = (f"{"    " * (counter - 1) + "  - "}{key}: "
                                  f"{value_first}\n"
                                  f"{"    " * (counter - 1) + "  + "}"
                                  f"{key}: {value_second}")
                    else:
                        string = (f"{"    " * (counter - 1) + "  - "}{key}: "
                                  f"{value_first}\n"
                                  f"{"    " * (counter - 1) + "  + "}"
                                  f"{key}: {value_second}")
                collection_for_result_string.append(string)
            case "unchanged":
                if isinstance(row[1][1], list):
                    string = (f"{"    " * counter}{row[1][0]}: "
                              f"{format_stylish(row[1][1], counter + 1)}")
                else:
                    key, value = row[1]
                    string = f"{"    " * counter}{key}: {value}"
                collection_for_result_string.append(string)
            case "delete":
                if isinstance(row[1][1], list):
                    string = (f"{"    " * (counter - 1) + "  - "}{row[1][0]}: "
                              f"{format_stylish(row[1][1], counter + 1)}")
                else:
                    key, value = row[1]
                    string = f"{"    " * (counter - 1) + "  - "}{key}: {value}"
                collection_for_result_string.append(string)
            case "added":
                if isinstance(row[1][1], list):
                    string = (f"{"    " * (counter - 1) + "  + "}{row[1][0]}: "
                              f"{format_stylish(row[1][1], counter + 1)}")
                else:
                    key, value = row[1]
                    string = f"{"    " * (counter - 1) + "  + "}{key}: {value}"
                collection_for_result_string.append(string)
    return f"{{\n{"\n".join(collection_for_result_string)}\n" \
           f"{"    " * (counter - 1)}}}"


def calculate_the_difference(data_first, data_second):  # noqa: C901
    list_keys = sorted(list(set(data_first) | set(data_second)))
    result_list = []
    for key in list_keys:
        value_first = data_first.get(key)
        value_second = data_second.get(key)
        if key in data_first and key in data_second:
            if value_first == value_second:
                if isinstance(value_first, dict) and \
                   isinstance(value_second, dict):
                    lst = calculate_the_difference(value_first, value_second)
                    node = ("unchanged", (key, lst))
                    result_list.append(node)
                else:
                    node = ("unchanged", (key, value_first))
                    result_list.append(node)
            elif value_first != value_second:
                if isinstance(value_first, dict) and \
                   isinstance(value_second, dict):
                    lst = calculate_the_difference(value_first, value_second)
                    node = ("update", (key, lst))
                    result_list.append(node)
                else:
                    node = ("update", (key, value_first, value_second))
                    result_list.append(node)
        elif key in data_first and key not in data_second:
            if isinstance(value_first, dict):
                lst = calculate_the_difference(value_first, value_first)
                node = ("delete", (key, lst))
                result_list.append(node)
            else:
                node = ("delete", (key, value_first))
                result_list.append(node)
        elif key not in data_first and key in data_second:
            if isinstance(value_second, dict):
                lst = calculate_the_difference(value_second, value_second)
                node = ("added", (key, lst))
                result_list.append(node)
            else:
                node = ("added", (key, value_second))
                result_list.append(node)
    return result_list


def changing_the_value_to_json_format(dct):
    if isinstance(dct, dict):
        for k, v in dct.items():
            if isinstance(v, dict):
                changing_the_value_to_json_format(v)
            if v in (True, False):
                value = str(v).lower()
                dct[k] = value
            if v is None:
                dct[k] = "null"
    return dct


def generate_diff(path_line_1, path_line_2, format_name="stylish"):
    try:
        with open(path_line_1, "r", encoding="utf-8") as first_file, \
             open(path_line_2, "r", encoding="utf-8") as second_file:
            _, extension = os.path.splitext(path_line_1)
            match extension:
                case ".json":
                    data_first = json.load(first_file)
                    data_second = json.load(second_file)
                case ".yml" | ".yaml":
                    data_first = yaml.safe_load(first_file)
                    data_second = yaml.safe_load(second_file)
        result_list = calculate_the_difference(
            changing_the_value_to_json_format(data_first),
            changing_the_value_to_json_format(data_second))
        match format_name:
            case "stylish":
                return format_stylish(result_list)
            case "plain":
                pass
            case "json":
                pass
    except FileNotFoundError:
        return "Path does not exist"
