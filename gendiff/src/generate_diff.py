import os
import json
import yaml
from gendiff.output_formats.format_json import format_json
from gendiff.output_formats.format_plain import format_plain
from gendiff.output_formats.format_stylish import format_stylish


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


def generate_diff(path_line_1, path_line_2, format_name=None):
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
        match format_name:
            case "stylish" | None:
                result_list = calculate_the_difference(
                    changing_the_value_to_json_format(data_first),
                    changing_the_value_to_json_format(data_second))
                return format_stylish(result_list)
            case "plain":
                result_list = calculate_the_difference(
                    changing_the_value_to_json_format(data_first),
                    changing_the_value_to_json_format(data_second))
                return format_plain(result_list)
            case "json":
                result_list = calculate_the_difference(data_first, data_second)
                return format_json(result_list)
    except FileNotFoundError:
        return "Path does not exist"
