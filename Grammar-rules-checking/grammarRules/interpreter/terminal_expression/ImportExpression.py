from interpreter.expression import Expression

class ImportExpression(Expression):
    def __init__(self, hooks, line):
        super().__init__(line)
        self.hooks = hooks

    def interpret(self, context):
        for hook in self.hooks:
            context.add_import(hook)
