def get_string_or_value(value):
    if isinstance(value, dict):
        return "[complex value]"
    return value


def format_plain(result_list, row_name=""):
    collection_for_result_string = []
    for dct in result_list:
        match dct["type"]:
            case "nested":
                string = f"{
                    format_plain(
                        dct["value"],
                        row_name + "." + dct["key"]
                        )}"
                collection_for_result_string.append(string)
            case "added":
                value = get_string_or_value(dct["value"])
                if (
                    value
                    not in ["true", "false", "null", "[complex value]"]
                    and not value.isdigit()
                ):
                    value = f"'{value}'"
                string = (
                    f"Property '{(row_name + "." + dct["key"])[1:]}' "
                    f"was added with value: {value}"
                )
                collection_for_result_string.append(string)
            case "delete":
                string = (
                    f"Property '{(row_name + "." + dct["key"])[1:]}' "
                    f"was removed"
                )
                collection_for_result_string.append(string)
            case "update":
                value_old = get_string_or_value(dct["value_old"])
                value_new = get_string_or_value(dct["value_new"])
                if (
                    value_old
                    not in ["true", "false", "null", "[complex value]"]
                    and not value_old.isdigit()
                ):
                    value_old = f"'{value_old}'"
                if (
                    value_new
                    not in ["true", "false", "null", "[complex value]"]
                    and not value_new.isdigit()
                ):
                    value_new = f"'{value_new}'"
                string = (
                    f"Property "
                    f"'{(row_name + "." + dct["key"])[1:]}' "
                    f"was updated. From {value_old} "
                    f"to {value_new}"
                )
                collection_for_result_string.append(string)
    return "\n".join(collection_for_result_string)
