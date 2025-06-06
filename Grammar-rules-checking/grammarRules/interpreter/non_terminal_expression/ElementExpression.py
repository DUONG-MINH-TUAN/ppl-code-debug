from typing import List
from interpreter.expression import Expression

class ElementExpression(Expression):
    def __init__(self, open_tag, close_tag, line, content):
        super().__init__(line)
        self.open_tag = open_tag
        self.close_tag = close_tag
        self.content = content

    def interpret(self, context):
        for content in self.content:
            content.interpret(context)