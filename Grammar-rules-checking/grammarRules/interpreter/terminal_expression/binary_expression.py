from typing import List, Optional
from ..expression import Expression
from ..context import Context

class BinaryExpression(Expression):
    def __init__(self, op: str, left: Expression, right: Expression, line: int):
        self.op = op
        self.left = left
        self.right = right
        self.line = line

    def interpret(self, context: Context):
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        if self.op == "+":
            return left_value + right_value
        elif self.op == "-":
            return left_value - right_value
        elif self.op == "*":
            return left_value * right_value
        elif self.op == "/":
            if right_value == 0:
                context.errors.append(f"Error at line {self.line}: Division by zero.")
                return 0
            return left_value / right_value