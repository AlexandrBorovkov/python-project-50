def translating_to_a_string(dct, counter):
    lst = []
    if isinstance(dct, dict):
        for key, value in dct.items():
            if isinstance(value, dict):
                value = translating_to_a_string(value, counter + 1)
            string = f"{"    " * (counter + 1)}{key}: {value}"
            lst.append(string)
    return f"{{\n{",\n".join(lst)}\n{"    " * counter}}}"


def format_stylish(result_list, counter=1):
    collection_for_result_string = []
    for row in result_list:
        match row[0]:
            case "update":
                if isinstance(row[1][1], list):
                    string = (f"{"    " * counter}{row[1][0]}: "
                              f"{format_stylish(row[1][1], counter + 1)}")
                else:
                    key, value_first, value_second = row[1]
                    if isinstance(value_first, dict):
                        value_first = translating_to_a_string(value_first,
                                                              counter)
                        string = (f"{"    " * (counter - 1) + "  - "}{key}: "
                                  f"{value_first}\n"
                                  f"{"    " * (counter - 1) + "  + "}"
                                  f"{key}: {value_second}")
                    if isinstance(value_second, dict):
                        value_second = translating_to_a_string(value_second,
                                                               counter)
                        string = (f"{"    " * (counter - 1) + "  - "}{key}: "
                                  f"{value_first}\n"
                                  f"{"    " * (counter - 1) + "  + "}"
                                  f"{key}: {value_second}")
                    else:
                        string = (f"{"    " * (counter - 1) + "  - "}{key}: "
                                  f"{value_first}\n"
                                  f"{"    " * (counter - 1) + "  + "}"
                                  f"{key}: {value_second}")
                collection_for_result_string.append(string)
            case "unchanged":
                if isinstance(row[1][1], list):
                    string = (f"{"    " * counter}{row[1][0]}: "
                              f"{format_stylish(row[1][1], counter + 1)}")
                else:
                    key, value = row[1]
                    string = f"{"    " * counter}{key}: {value}"
                collection_for_result_string.append(string)
            case "delete":
                if isinstance(row[1][1], list):
                    string = (f"{"    " * (counter - 1) + "  - "}{row[1][0]}: "
                              f"{format_stylish(row[1][1], counter + 1)}")
                else:
                    key, value = row[1]
                    string = f"{"    " * (counter - 1) + "  - "}{key}: {value}"
                collection_for_result_string.append(string)
            case "added":
                if isinstance(row[1][1], list):
                    string = (f"{"    " * (counter - 1) + "  + "}{row[1][0]}: "
                              f"{format_stylish(row[1][1], counter + 1)}")
                else:
                    key, value = row[1]
                    string = f"{"    " * (counter - 1) + "  + "}{key}: {value}"
                collection_for_result_string.append(string)
    return f"{{\n{"\n".join(collection_for_result_string)}\n" \
           f"{"    " * (counter - 1)}}}"
