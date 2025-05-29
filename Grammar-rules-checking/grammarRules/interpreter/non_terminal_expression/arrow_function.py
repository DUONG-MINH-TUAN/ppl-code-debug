from typing import List
from ..expression import Expression
from ..context import Context


class ArrowFunctionExpression(Expression):
    def __init__(self, params: List[str], body: List[Expression], line: int):
        self.params = params
        self.body = body
        self.line = line

    def interpret(self, context: Context) -> None:
        context.enter_scope()
        for param in self.params:
            error = context.declare_variable(param, self.line)
            if error:
                context.errors.append(error)
        for expr in self.body:
            expr.interpret(context)
        context.exit_scope()