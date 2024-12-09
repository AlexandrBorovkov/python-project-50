from gendiff.src.generate_diff import generate_diff

file_missing = "Path does not exist"


def test_generate_diff_file_not_found():
    assert generate_diff("tests/fixtures/file1.json", "tests/fixtures/no_name.json", format_name="stylish") == file_missing


def test_generate_diff_nested_structure_json():
    with open("tests/fixtures/stylish_format.txt", encoding='utf8') as file:
        data = file.read()
    assert generate_diff("tests/fixtures/file_1.json", "tests/fixtures/file_2.json", format_name="stylish") == data


def test_generate_diff_nested_structure_yml():
    with open("tests/fixtures/stylish_format.txt", encoding='utf8') as file:
        data = file.read()
    assert generate_diff("tests/fixtures/file_1.yaml", "tests/fixtures/file_2.yaml", format_name="stylish") == data


def test_generate_diff_format_plain():
    with open("tests/fixtures/plain_format.txt", encoding='utf8') as file:
        data = file.read()
    assert generate_diff("tests/fixtures/file_1.json", "tests/fixtures/file_2.json", format_name="plain") == data


def test_generate_diff_format_json():
    with open("tests/fixtures/json_format.txt", encoding='utf8') as file:
        data = file.read()
    assert generate_diff("tests/fixtures/file_1.json", "tests/fixtures/file_2.json", format_name="json") == data
