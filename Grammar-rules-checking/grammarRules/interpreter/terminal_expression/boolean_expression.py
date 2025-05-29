from typing import List, Optional
from ..expression import Expression
from ..context import Context


class BooleanExpression(Expression):
    def __init__(self, value: bool, line: int):
        self.value = value
        self.line = line

    def interpret(self, context: Context):
        return self.value