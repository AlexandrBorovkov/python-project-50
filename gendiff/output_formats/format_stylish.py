def translating_to_a_string(dct, counter):
    lst = []
    if isinstance(dct, dict):
        for key, value in dct.items():
            if isinstance(value, dict):
                value = translating_to_a_string(value, counter + 1)
            string = f"{"    " * (counter + 1)}{key}: {value}"
            lst.append(string)
    return f"{{\n{"\n".join(lst)}\n{"    " * counter}}}"


def format_stylish(result_list, counter=1): # noqa: C901
    collection_for_result_string = []
    for dct in result_list:
        match dct["type"]:
            case "nested":
                key, value = dct["key"], dct["value"]
                string = (
                    f"{"    " * counter}{key}: "
                    f"{format_stylish(value, counter + 1)}"
                )
                collection_for_result_string.append(string)
            case "added":
                key, value = dct["key"], dct["value"]
                if isinstance(value, dict):
                        value = translating_to_a_string(
                            value, counter
                        )
                string = f"{"    " * (counter - 1) + "  + "}{key}: {value}"
                collection_for_result_string.append(string)
            case "delete":
                key, value = dct["key"], dct["value"]
                if isinstance(value, dict):
                        value = translating_to_a_string(
                            value, counter
                        )
                string = f"{"    " * (counter - 1) + "  - "}{key}: {value}"
                collection_for_result_string.append(string)
            case "update":
                key = dct["key"]
                value_old = dct["value_old"]
                value_new = dct["value_new"]
                if isinstance(value_new, dict):
                        value_new = translating_to_a_string(
                            value_new, counter
                        )
                if isinstance(value_old, dict):
                        value_old = translating_to_a_string(
                            value_old, counter
                        )
                string = (
                    f"{"    " * (counter - 1) + "  - "}{key}: "
                    f"{value_old}\n"
                    f"{"    " * (counter - 1) + "  + "}"
                    f"{key}: {value_new}"
                )
                collection_for_result_string.append(string)
            case "unchanged":
                key, value = dct["key"], dct["value"]
                string = f"{"    " * counter}{key}: {value}"
                collection_for_result_string.append(string)
    return (
        f"{{\n{"\n".join(collection_for_result_string)}\n"
        f"{"    " * (counter - 1)}}}"
    )
