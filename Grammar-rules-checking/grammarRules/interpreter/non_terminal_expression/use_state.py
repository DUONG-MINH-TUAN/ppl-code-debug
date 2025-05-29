from typing import List, Optional
from ..expression import Expression
from ..context import Context


class StateSetterExpression(Expression):
    def __init__(self, state_pair: List[str], initial_value: Optional[Expression], line: int):
        self.state_pair = state_pair
        self.initial_value = initial_value
        self.line = line

    def interpret(self, context: Context) -> None:
        error = context.check_hook("useState", self.line)
        if error:
            context.errors.append(error)
        for name in self.state_pair:
            error = context.declare_variable(name, self.line)
            if error:
                context.errors.append(error)
        if self.initial_value:
            self.initial_value.interpret(context)
