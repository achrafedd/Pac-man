class Parsing(Exception):
    def __init__(self, message: str):
        super().__init__(
            "\033[91mError Parsing: \033[0m" + message
            )
