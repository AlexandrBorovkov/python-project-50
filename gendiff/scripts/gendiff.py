#!/usr/bin/env python3


import argparse
from gendiff.src.generate_diff import generate_diff


def main():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference.")
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument("-f", "--format", help="set format of output")
    args = parser.parse_args()
    first_file = args.first_file
    second_file = args.second_file
    format_name = "stylish" if args.format is None else args.format
    print(generate_diff(first_file, second_file, format_name))


if __name__ == "__main__":
    main()
