from interpreter.expression import Expression

class ValueIndicatorExpression(Expression):
    def __init__(self, name, line):
        super().__init__(line)
        self.name = name
