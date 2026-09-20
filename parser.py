import sys
import json
from typing import Any
from errors import Parsing


def take_arges() -> str:
    args = sys.argv
    if len(args) != 2:
        raise Parsing(
            "wrong arguments \ntry this: python3 pac-man.py config.json"
        )
    file = args[1]
    return file


def check_file(file: str) -> str:
    if not file.endswith(".json"):
        raise Parsing(
            "wrong file type \ntry this: python3 pac-man.py config.json"
        )
    try:
        with open(file, "r") as f:
            data = f.read()
    except FileNotFoundError as e:
        raise Parsing(f"file not found {file}: {e}")
    except PermissionError as e:
        raise Parsing(f"permission denied {file}: {e}")
    except Exception as e:
        raise Parsing(f"error reading file {file}: {e}")

    return data


def parse_json(data: str) -> Any:
    config = ""
    for line in data.splitlines():
        line = line.strip()
        line = line.split("#")[0].strip()
        if line.startswith("#"):
            continue
        config += line
    try:
        return json.loads(config)
    except json.JSONDecodeError as e:
        raise Parsing(f"error parsing JSON: {e}")


def check_config_values(config: dict) -> dict:
    default = {
        "highscore_filename": 132432413,
        "width": 15,
        "height": 15,
        "pacgum": 42,
        "lives": 3,
        "points_per_pacgum": 10,
        "points_per_super_pacgum": 50,
        "points_per_ghost": 200,
        "seed": 42,
    }
    for key, value in config.items():
        if key not in default:
            print(f"\033[91mWarning: Unknown config key '{key}'\033[0m")
            continue
        else:
            if not isinstance(value, type(default[key])):
                print(
                    f"\033[91mWarning: Config key '{key}' "
                    "has wrong type.\033[0m"
                )
                continue
            default[key] = value
    return default
