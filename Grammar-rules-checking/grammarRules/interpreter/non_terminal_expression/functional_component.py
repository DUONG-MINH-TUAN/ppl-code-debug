from typing import List, Optional
from ..expression import Expression
from ..context import Context


class FunctionDeclarationExpression(Expression):
    def __init__(self, name: str, line: int, params: List[str], body: List[Expression]):
        self.name = name
        self.line = line
        self.params = params
        self.body = body

    def interpret(self, context: Context) -> None:
        context.declare_function(self.name, self.line)
        context.enter_scope()
        for param in self.params:
            context.declare_variable(param, self.line, None, initialized=False)
        for stmt in self.body:
            context.track_function_call(self.name, self.line)
            stmt.interpret(context)
        context.exit_scope()
