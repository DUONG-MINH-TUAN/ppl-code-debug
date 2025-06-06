from interpreter.expression import Expression
class BinaryExpression(Expression):
    def __init__(self, op, left, right, line):
        super().__init__(line)
        self.op = op
        self.left = left
        self.right = right

    def interpret(self, context):
        self.left.interpret(context)
        self.right.interpret(context)
