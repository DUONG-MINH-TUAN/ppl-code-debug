
import sys
from interpreter.expression import Expression

class ReturnStatementExpression(Expression):
    def __init__(self, element, line):
        super().__init__(line)
        self.element = element

    def interpret(self, context):
        self.element.interpret(context)
