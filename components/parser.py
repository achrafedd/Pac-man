import sys
import json
from typing import Any
from .errors import Parsing
from .utils import Config


class Parser:
    """Represent parser behavior.
    """
    def __init__(self) -> None:
        """Initialize the object.
        """
        file = self.take_arges()
        data = self.check_file(file)
        config = self.parse_json(data)
        self.config: Config = self.check_config_values(config)

    def take_arges(self) -> str:
        """Perform the take arges operation.

        Returns:
            str: The operation result.
        """
        args = sys.argv
        if len(args) != 2:
            raise Parsing(
                "wrong arguments \ntry this: python3 pac-man.py config.json"
            )
        file = args[1]
        return file

    def check_file(self, file: str) -> str:
        """Perform the check file operation.

        Args:
            file (str): Value used by the operation.

        Returns:
            str: The operation result.
        """
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

    def parse_json(self, data: str) -> Any:
        """Perform the parse json operation.

        Args:
            data (str): Value used by the operation.

        Returns:
            Any: The operation result.
        """
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

    def check_config_values(self, config: dict) -> Config:
        """Perform the check config values operation.

        Args:
            config (dict): Value used by the operation.

        Returns:
            Config: The operation result.
        """
        default = Config(**config)
        return default
