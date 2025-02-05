def create_tree_differences(data_first, data_second):  # noqa: C901
    list_keys = sorted(list(set(data_first) | set(data_second)))
    result_list = []
    for key in list_keys:
        value_first = data_first.get(key)
        value_second = data_second.get(key)
        if key in data_first and key in data_second:
            if value_first == value_second:
                if isinstance(value_first, dict) and isinstance(
                    value_second, dict
                ):
                    lst = create_tree_differences(value_first, value_second)
                    node = ("unchanged", (key, lst))
                    result_list.append(node)
                else:
                    node = ("unchanged", (key, value_first))
                    result_list.append(node)
            elif value_first != value_second:
                if isinstance(value_first, dict) and isinstance(
                    value_second, dict
                ):
                    lst = create_tree_differences(value_first, value_second)
                    node = ("update", (key, lst))
                    result_list.append(node)
                else:
                    node = ("update", (key, value_first, value_second))
                    result_list.append(node)
        elif key in data_first and key not in data_second:
            if isinstance(value_first, dict):
                lst = create_tree_differences(value_first, value_first)
                node = ("delete", (key, lst))
                result_list.append(node)
            else:
                node = ("delete", (key, value_first))
                result_list.append(node)
        elif key not in data_first and key in data_second:
            if isinstance(value_second, dict):
                lst = create_tree_differences(value_second, value_second)
                node = ("added", (key, lst))
                result_list.append(node)
            else:
                node = ("added", (key, value_second))
                result_list.append(node)
    return result_list
