
from typing import List
from ..expression import Expression
from ..context import Context


class IfExpression(Expression):
    def __init__(self, condition: Expression, then_block: List[Expression], else_block: List[Expression], line: int):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block
        self.line = line

    def interpret(self, context: Context) -> None:
        condition_value = self.condition.interpret(context)
        if condition_value:
            context.execution_path.append("if")
            for stmt in self.then_block:
                stmt.interpret(context)
            context.execution_path.pop()
        else:
            context.execution_path.append("else")
            for stmt in self.else_block:
                stmt.interpret(context)
            context.execution_path.pop()