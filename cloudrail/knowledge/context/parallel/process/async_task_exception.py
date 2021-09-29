from typing import Tuple


class AsyncTaskException(Exception):

    def __init__(self, function, args: Tuple) -> None:
        Exception.__init__(self)
        self.function = function
        self.args: Tuple = args

    def __str__(self) -> str:
        return f"function={self.function}, args={str(self.args)}"
