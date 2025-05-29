
from typing import List
from ..expression import Expression
from ..context import Context


class ArrayExpression(Expression):
    def __init__(self, values: List[Expression], line: int):
        
        self.values = values
        self.line = line

    def interpret(self, context: Context) -> None:
        for value in self.values:
            value.interpret(context)
