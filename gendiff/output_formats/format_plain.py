def get_string_or_value(value):
    if isinstance(value, dict) or isinstance(value, list):
        return "[complex value]"
    return value


def format_plain(result_list):
    collection_for_result_string = []

    def recursive_function(result_list, row_name=""):
        for row in result_list:
            match row[0]:
                case "update":
                    if isinstance(row[1][1], list):
                        recursive_function(
                            row[1][1], row_name + "." + row[1][0])
                    else:
                        value_1 = get_string_or_value(row[1][1])
                        value_2 = get_string_or_value(row[1][2])
                        if (value_1 not in
                            ["true", "false",
                             "null", "[complex value]"]
                                and not value_1.isdigit()):
                            value_1 = f"'{value_1}'"
                        if (value_2 not in
                            ["true", "false",
                             "null", "[complex value]"]
                                and not value_2.isdigit()):
                            value_2 = f"'{value_2}'"
                        string = f"Property " \
                                 f"'{(row_name + "." + row[1][0])[1:]}' " \
                                 f"was updated. From {value_1} " \
                                 f"to {value_2}"
                        collection_for_result_string.append(string)
                case "unchanged":
                    if isinstance(row[1][1], list):
                        recursive_function(
                            row[1][1], row_name + "." + row[1][0])
                case "delete":
                    string = f"Property '{(row_name + "." + row[1][0])[1:]}' "\
                             f"was removed"
                    collection_for_result_string.append(string)
                case "added":
                    value = get_string_or_value(row[1][1])
                    if (value not in
                        ["true", "false", "null",
                         "[complex value]"]
                            and not value.isdigit()):
                        value = f"'{value}'"
                    string = f"Property '{(row_name + "." + row[1][0])[1:]}' " \
                        f"was added with value: {value}"
                    collection_for_result_string.append(string)
    recursive_function(result_list)
    return "\n".join(collection_for_result_string)
