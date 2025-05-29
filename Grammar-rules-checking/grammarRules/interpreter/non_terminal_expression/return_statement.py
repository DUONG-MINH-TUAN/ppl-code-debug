
from typing import List, Optional
from ..expression import Expression
from ..context import Context


class ReturnStatementExpression(Expression):
    def __init__(self, element: Expression, line: int):
        self.element = element
        self.line = line

    def interpret(self, context: Context) -> None:
        self.element.interpret(context)
