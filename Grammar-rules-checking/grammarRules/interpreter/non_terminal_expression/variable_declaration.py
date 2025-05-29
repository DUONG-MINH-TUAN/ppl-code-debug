from typing import Optional
from ..expression import Expression
from ..context import Context

class VariableDeclarationExpression(Expression):
    def __init__(self, name: str, line: int, value: Optional[Expression]):
        self.name = name
        self.line = line
        self.value = value

    def interpret(self, context: Context) -> None:
        value = self.value.interpret(context) if self.value else None
        error = context.declare_variable(self.name, self.line, value)
        if error:
            context.errors.append(error)