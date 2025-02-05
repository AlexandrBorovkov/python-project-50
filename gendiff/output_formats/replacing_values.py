def replacing_values_json_format(dct):
    if isinstance(dct, dict):
        for k, v in dct.items():
            if isinstance(v, dict):
                replacing_values_json_format(v)
            if v in (True, False):
                value = str(v).lower()
                dct[k] = value
            if v is None:
                dct[k] = "null"
    return dct
