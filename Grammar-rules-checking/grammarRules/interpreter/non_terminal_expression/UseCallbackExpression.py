import sys
from interpreter.expression import Expression

class UseCallbackExpression(Expression):
    def __init__(self, callback, deps, line):
        super().__init__(line)
        self.callback = callback
        self.deps = deps

    def interpret(self, context):
        print(f"Interpreting UseCallbackExpression at line {self.line}", file=sys.stderr)
        context.check_hook("useCallback", self.line, context.current_scope, self.callback, self.deps)
        if self.callback:
            self.callback.interpret(context)
