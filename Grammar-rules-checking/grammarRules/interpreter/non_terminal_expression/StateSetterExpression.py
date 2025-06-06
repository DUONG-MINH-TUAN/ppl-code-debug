import sys
from interpreter.expression import Expression
class StateSetterExpression(Expression):
    def __init__(self, state_pair, initial_value, line):
        super().__init__(line)
        self.state_pair = state_pair
        self.initial_value = initial_value

    def interpret(self, context):
        print(f"Interpreting StateSetterExpression: {self.state_pair}", file=sys.stderr)
        context.add_symbol(self.state_pair[0], context.current_scope, "state_variable", None)
        context.add_symbol(self.state_pair[1], context.current_scope, "setter_function", None)
        context.check_hook("useState", self.line, context.current_scope, initial_value=self.initial_value)
        if self.initial_value:
            self.initial_value.interpret(context)