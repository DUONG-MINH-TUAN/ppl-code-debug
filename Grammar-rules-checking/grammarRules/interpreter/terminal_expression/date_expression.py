from typing import List, Optional
from ..expression import Expression
from ..context import Context



class DateExpression(Expression):
    def __init__(self, line: int):
        self.line = line

    def interpret(self, context: Context) -> None:
        pass  # Date is valid by default
