from typing import List, Optional
from ..expression import Expression
from ..context import Context



class ElementExpression(Expression):
    def __init__(self, open_tag: str, close_tag: str, line: int, content: List[Expression]):
        self.open_tag = open_tag
        self.close_tag = close_tag
        self.line = line
        self.content = content

    def interpret(self, context: Context) -> None:
        context.push_tag(self.open_tag, self.line)
        for expr in self.content:
            expr.interpret(context)
        error = context.pop_tag(self.close_tag, self.line)
        if error:
            context.errors.append(error)
