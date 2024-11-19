from gendiff.src.generate_diff import generate_diff


correct_result = """{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""


file_missing = "Path does not exist"


def test_generate_diff_json():
    assert generate_diff("tests/fixtures/file1.json", "tests/fixtures/file2.json", format_name="stylish") == correct_result


def test_generate_diff_yml():
    assert generate_diff("tests/fixtures/file1.yml", "tests/fixtures/file2.yml", format_name="stylish") == correct_result


def test_generate_diff_file_not_found():
    assert generate_diff("tests/fixtures/file1.json", "tests/fixtures/no_name.json", format_name="stylish") == file_missing


def test_generate_diff_nested_structure_json():
    with open("tests/fixtures/file5.txt", encoding='utf8') as file:
        data = file.read()
    assert generate_diff("tests/fixtures/file3.json", "tests/fixtures/file4.json", format_name="stylish") == data


def test_generate_diff_nested_structure_yml():
    with open("tests/fixtures/file5.txt", encoding='utf8') as file:
        data = file.read()
    assert generate_diff("tests/fixtures/file3.yml", "tests/fixtures/file4.yml", format_name="stylish") == data


def test_generate_diff_format_plain():
    with open("tests/fixtures/file6.txt", encoding='utf8') as file:
        data = file.read()
    assert generate_diff("tests/fixtures/file3.json", "tests/fixtures/file4.json", format_name="plain") == data
