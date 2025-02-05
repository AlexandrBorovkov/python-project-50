import json

import yaml


def parse(file, extension):
    match extension:
        case "json":
            data = json.load(file)
        case "yml" | "yaml":
            data = yaml.safe_load(file)
    return data
