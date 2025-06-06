import sys
from interpreter.expression import Expression
from interpreter.non_terminal_expression.VariableDeclarationExpression import VariableDeclarationExpression
class ProgramExpression(Expression):
    def __init__(self, import_stmt, functions):
        super().__init__(0)
        self.import_stmt = import_stmt
        self.functions = functions

    def interpret(self, context):
        print(f"Interpreting ProgramExpression", file=sys.stderr)
        context.current_scope = "global"
       
        for func in self.functions:
            if isinstance(func, VariableDeclarationExpression):
                # Defer symbol addition to VariableDeclarationExpression.interpret
                print(f"Pre-noted variable {func.name} for global scope", file=sys.stderr)
        # Interpret import statement
        if self.import_stmt:
            self.import_stmt.interpret(context)
        # Interpret all expressions
        for func in self.functions:
            func.interpret(context)