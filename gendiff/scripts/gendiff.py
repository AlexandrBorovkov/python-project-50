#!/usr/bin/env python3


from gendiff.cli import accept_input_parameters
from gendiff.src.generate_diff import generate_diff


def main():
    parameters = accept_input_parameters()
    args = (parameters.first_file, parameters.second_file, parameters.format)
    print(generate_diff(*args))


if __name__ == "__main__":
    main()
