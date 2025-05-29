# interpreter/non_terminal_expression.py
from typing import List
from ..context import Context

from ..expression import Expression
class ForExpression(Expression):
    def __init__(self, var_name: str, iterable: str, body: List[Expression], line: int):
        self.var_name = var_name
        self.iterable = iterable
        self.body = body
        self.line = line

    def interpret(self, context: Context) -> None:
        iterable_value = context.get_variable(self.iterable, self.line)
        if iterable_value is None:
            return

        loop_id = f"for_{self.line}"
        context.enter_scope()
        for item in iterable_value:
            context.declare_variable(self.var_name, self.line, item, initialized=True)
            context.track_loop(loop_id, self.line)
            for stmt in self.body:
                stmt.interpret(context)
        context.exit_scope()