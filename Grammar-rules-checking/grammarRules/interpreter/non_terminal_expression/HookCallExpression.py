import sys
from interpreter.expression import Expression
class HookCallExpression(Expression):
    def __init__(self, name, args, line):
        super().__init__(line)
        self.name = name
        self.args = args

    def interpret(self, context):
        print(f"Interpreting HookCallExpression: {self.name} at line {self.line}", file=sys.stderr)
        context.check_hook(self.name, self.line, context.current_scope, deps=self.args)
