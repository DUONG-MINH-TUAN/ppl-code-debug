from typing import List
from interpreter.expression import Expression

class FunctionalComponentExpression(Expression):
    def __init__(self, name: str, params: List[str], body: Expression, line: int):
        super().__init__(line)
        self.name = name
        self.params = params
        self.body = body  

    def interpret(self, context):
        context.current_scope = self.name
        self.body.interpret(context)
