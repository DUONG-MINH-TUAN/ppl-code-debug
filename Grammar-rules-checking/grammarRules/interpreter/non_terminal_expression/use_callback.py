from typing import List, Optional
from ..expression import Expression
from ..context import Context



class UseCallbackExpression(Expression):
    def __init__(self, callback: Optional[Expression], dependencies: List[str], line: int):
        self.callback = callback
        self.dependencies = dependencies
        self.line = line

    def interpret(self, context: Context) -> None:
        error = context.check_hook("useCallback", self.line)
        if error:
            context.errors.append(error)
        if self.callback:
            self.callback.interpret(context)
        for dep in self.dependencies:
            context.lookup_variable(dep, self.line)
