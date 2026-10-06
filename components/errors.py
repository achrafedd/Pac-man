class Parsing(Exception):
    """Represent parsing behavior.
    """
    def __init__(self, message: str):
        """Initialize the object.

        Args:
            message (str): Value used by the operation.
        """
        super().__init__(
            "\033[91mError Parsing: \033[0m" + message
            )
