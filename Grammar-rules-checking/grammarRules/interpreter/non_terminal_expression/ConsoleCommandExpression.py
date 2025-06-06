from interpreter.expression import Expression
class ConsoleCommandExpression(Expression):
    def __init__(self, arg, line):
        super().__init__(line)
        self.arg = arg

    def interpret(self, context):
        if self.arg:
            self.arg.interpret(context)
