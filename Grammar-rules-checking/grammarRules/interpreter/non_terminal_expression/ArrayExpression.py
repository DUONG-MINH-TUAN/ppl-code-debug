from interpreter.expression import Expression
class ArrayExpression(Expression):
    def __init__(self, values, line):
        super().__init__(line)
        self.values = values

    def interpret(self, context):
        for value in self.values:
            value.interpret(context)
