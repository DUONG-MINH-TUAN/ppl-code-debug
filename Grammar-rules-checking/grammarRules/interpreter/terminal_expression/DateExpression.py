from interpreter.expression import Expression

class DateExpression(Expression):
    def __init__(self, line):
        super().__init__(line)
