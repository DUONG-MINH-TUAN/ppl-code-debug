from typing import List, Optional
from ..expression import Expression
from ..context import Context

class ConsoleCommandExpression(Expression):
    def __init__(self, arg: Optional[Expression], line: int):
        self.arg = arg
        self.line = line

    def interpret(self, context: Context) -> None:
        if self.arg:
            value = self.arg.interpret(context)
            if isinstance(value, str) and "eval" in value.lower():
                context.errors.append(f"Error at line {self.line}: Potential security risk - use of 'eval' detected.")
