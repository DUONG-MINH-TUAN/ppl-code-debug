from interpreter.expression import Expression


class StringExpression(Expression):
    def __init__(self, value, line):
        super().__init__(line)
        self.value = value
