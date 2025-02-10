def create_tree_differences(data_first, data_second):
    list_keys = sorted(list(set(data_first) | set(data_second)))
    result_list = []
    for key in list_keys:
        value_first = data_first.get(key)
        value_second = data_second.get(key)
        if isinstance(value_first, dict) and isinstance(value_second, dict):
            result_list.append({
                "key": key,
                "value": create_tree_differences(value_first, value_second),
                "type": "nested"
                })
        else:
            if key not in data_first:
                result_list.append({
                    "key": key,
                    "value": value_second,
                    "type": "added"
                    })
            elif key not in data_second:
                result_list.append({
                    "key": key,
                    "value": value_first,
                    "type": "delete"
                    })
            elif value_first != value_second:
                result_list.append({
                    "key": key,
                    "value_old": value_first,
                    "value_new": value_second,
                    "type": "update"
                    })
            else:
                result_list.append({
                    "key": key,
                    "value": value_first,
                    "type": "unchanged"
                    })
    return result_list
