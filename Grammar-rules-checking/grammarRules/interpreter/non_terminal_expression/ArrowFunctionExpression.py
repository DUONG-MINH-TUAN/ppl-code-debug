from interpreter.expression import Expression
class ArrowFunctionExpression(Expression):
    def __init__(self, params, body, line):
        super().__init__(line)
        self.params = params
        self.body = body

    def interpret(self, context):
        for expr in self.body:
            expr.interpret(context)
