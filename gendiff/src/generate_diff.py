import os

from gendiff.output_formats import format_differences
from gendiff.output_formats.replacing_values import replacing_values_json_format
from gendiff.src.create_tree import create_tree_differences
from gendiff.src.parser import parse


def get_extension(file_path):
    extension = os.path.splitext(file_path)[1]
    return extension[1:]


def get_file_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return parse(file, get_extension(file_path))
    except FileNotFoundError:
        return None


def generate_diff(path_line_1, path_line_2, format_name=None):
    data_first = get_file_data(path_line_1)
    data_second = get_file_data(path_line_2)
    if None in (data_first, data_second):
        return "Path does not exist"
    if format_name != "json":
        data_first = replacing_values_json_format(data_first)
        data_second = replacing_values_json_format(data_second)
    tree_differences = create_tree_differences(data_first, data_second)
    return format_differences(tree_differences, format_name)
