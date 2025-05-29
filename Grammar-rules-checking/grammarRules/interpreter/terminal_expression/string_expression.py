from typing import List, Optional
from ..expression import Expression
from ..context import Context


class StringExpression(Expression):
    def __init__(self, value: str, line: int):
        self.value = value
        self.line = line

    def interpret(self, context: Context) -> None:
        pass  # Strings are valid by default
