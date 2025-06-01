from abc import ABC, abstractmethod
from typing import List, Optional

from interpreter.context import Context


class Expression(ABC):
    @abstractmethod
    def interpret(self, context: Context) -> None:
        pass
class ProgramExpression(Expression):
    def __init__(self, import_stmt: Optional[Expression], functions: List[Expression]):
        self.import_stmt = import_stmt
        self.functions = functions

    def interpret(self, context: Context) -> None:
        if self.import_stmt:
            self.import_stmt.interpret(context)
        for func in self.functions:
            func.interpret(context)