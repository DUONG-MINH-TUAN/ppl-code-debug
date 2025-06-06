
from typing import List
from interpreter.expression import Expression

class ClassComponentExpression(Expression):
    def __init__(self, name: str, methods: List[Expression], line: int):
        super().__init__(line)
        self.name = name
        self.methods = methods

    def interpret(self, context):
        context.current_scope = self.name
        for method in self.methods:
            method.interpret(context)
