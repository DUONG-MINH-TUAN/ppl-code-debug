import sys
from typing import List
from interpreter.expression import Expression
from interpreter.non_terminal_expression.ArrayExpression import ArrayExpression
from interpreter.terminal_expression.BooleanExpression import BooleanExpression
from interpreter.terminal_expression.StringExpression import StringExpression
from interpreter.terminal_expression.NumberExpression import NumberExpression
from interpreter.terminal_expression.BigIntExpression import BigIntExpression
from interpreter.terminal_expression.DateExpression import DateExpression
class VariableDeclarationExpression(Expression):
    def __init__(self, name, line, value):
        super().__init__(line)
        self.name = name
        self.value = value

    def interpret(self, context):
        print(f"Interpreting VariableDeclarationExpression: {self.name}", file=sys.stderr)
        var_type = None
        value = None
        if self.value:
            self.value.interpret(context)
            if isinstance(self.value, ArrayExpression):
                var_type = "array"
                value = self.value.values
            elif isinstance(self.value, NumberExpression):
                var_type = "number"
                value = self.value.value
            elif isinstance(self.value, StringExpression):
                var_type = "string"
                value = self.value.value
            elif isinstance(self.value, BooleanExpression):
                var_type = "boolean"
                value = self.value.value
            elif isinstance(self.value, BigIntExpression):
                var_type = "bigint"
                value = self.value.value
            elif isinstance(self.value, DateExpression):
                var_type = "date"
                value = None
        context.add_symbol(self.name, context.current_scope, var_type, value)
