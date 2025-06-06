

import sys
from interpreter.expression import Expression
class ForExpression(Expression):
    def __init__(self, var_name, iterable, body, line):
        super().__init__(line)
        self.var_name = var_name
        self.iterable = iterable
        self.body = body

    def interpret(self, context):
        print(f"Interpreting ForExpression at line {self.line}", file=sys.stderr)
        symbol_info = context.check_symbol(self.iterable, context.current_scope)
        if not symbol_info:
            context.errors.append({
                "error": f"For loop at line {self.line} references undefined iterable '{self.iterable}'.",
                "suggestion": f"Ensure '{self.iterable}' is declared and initialized before the loop (e.g., 'let {self.iterable} = [];')."
            })
        elif symbol_info["type"] != "array":
            context.errors.append({
                "error": f"For loop at line {self.line} uses non-iterable '{self.iterable}' of type {symbol_info['type']}.",
                "suggestion": f"Ensure '{self.iterable}' is an array (e.g., 'let {self.iterable} = [1];')."
            })
        elif not symbol_info["value"] or len(symbol_info["value"]) == 0:
            context.errors.append({
                "error": f"For loop at line {self.line} uses empty array '{self.iterable}'.",
                "suggestion": f"Ensure '{self.iterable}' contains at least one element (e.g., 'let {self.iterable} = [1];')."
            })
        context.add_symbol(self.var_name, context.current_scope, "loop_variable", None)
        for expr in self.body:
            expr.interpret(context)
