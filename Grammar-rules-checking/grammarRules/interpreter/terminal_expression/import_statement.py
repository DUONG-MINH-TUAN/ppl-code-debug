from typing import List
from ..expression import Expression
from ..context import Context

class ImportExpression(Expression):
    def __init__(self, hooks: List[str], line: int):
        self.hooks = hooks
        self.line = line

    def interpret(self, context: Context) -> None:
        for hook in self.hooks:
            error = context.declare_hook(hook, self.line)
            if error:
                context.errors.append(error)
