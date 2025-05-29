from typing import List, Optional
from ..expression import Expression
from ..context import Context


class ValueIndicatorExpression(Expression):
    def __init__(self, name: str, line: int):
        self.name = name
        self.line = line

    def interpret(self, context: Context):
        value = context.get_variable(self.name, self.line)
        return value