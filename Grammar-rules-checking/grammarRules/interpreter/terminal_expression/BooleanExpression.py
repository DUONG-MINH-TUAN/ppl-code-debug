
from interpreter.expression import Expression

class BooleanExpression(Expression):
    def __init__(self, value, line):
        super().__init__(line)
        self.value = value
