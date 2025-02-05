from gendiff.output_formats.format_json import format_json
from gendiff.output_formats.format_plain import format_plain
from gendiff.output_formats.format_stylish import format_stylish


def format_differences(tree_differences, format_name):
    match format_name:
        case "stylish" | None:
            return format_stylish(tree_differences)
        case "plain":
            return format_plain(tree_differences)
        case "json":
            return format_json(tree_differences)
