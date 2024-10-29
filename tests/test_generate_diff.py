from gendiff.src.generate_diff import generate_diff


correct_result = """{
  - follow: False
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: True
}"""


file_missing = "Path does not exist"


def test_generate_diff_json():
    assert generate_diff("tests/fixtures/file1.json", "tests/fixtures/file2.json") == correct_result


def test_generate_diff_yml():
    assert generate_diff("tests/fixtures/file1.yml", "tests/fixtures/file2.yml") == correct_result


def test_generate_diff_file_not_found():
    assert generate_diff("tests/fixtures/file1.json", "tests/fixtures/no_name.json") == file_missing