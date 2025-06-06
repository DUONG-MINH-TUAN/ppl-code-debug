from interpreter.expression import Expression
class IfExpression(Expression):
    def __init__(self, condition, then_block, else_block, line):
        super().__init__(line)
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def interpret(self, context):
        self.condition.interpret(context)
        for expr in self.then_block:
            expr.interpret(context)
        for expr in self.else_block:
            expr.interpret(context)
