import sys
from interpreter.expression import Expression

class FunctionDeclarationExpression(Expression):
    def __init__(self, name, line, params, body):
        super().__init__(line)
        self.name = name
        self.params = params
        self.body = body

    def interpret(self, context):
        print(f"Interpreting FunctionDeclarationExpression: {self.name}", file=sys.stderr)
        context.current_scope = self.name
        for param in self.params:
            context.add_symbol(param, self.name, "parameter", None)
        for expr in self.body:
            expr.interpret(context)
        context.current_scope = "global"
