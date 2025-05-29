from typing import List, Optional
from ..expression import Expression
from ..context import Context


class NumberExpression(Expression):
    def __init__(self, value: str, line: int):
        self.value = value
        self.line = line

    def interpret(self, context: Context) -> None:
        pass  # Numbers are valid by default
