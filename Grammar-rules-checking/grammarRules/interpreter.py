from abc import ABC, abstractmethod
from typing import List, Optional

class Context:
    def __init__(self, input_lines: List[str]):
        self.scopes = [set()]  # Stack of symbol tables
        self.function_names = set()  # Track function names
        self.errors = []
        self.input_lines = input_lines
        self.tag_stack = []
        self.imported_hooks = set()

    def enter_scope(self):
        self.scopes.append(set())

    def exit_scope(self):
        self.scopes.pop()

    def declare_variable(self, name: str, line: int) -> Optional[str]:
        if name in self.scopes[-1]:
            return f"Error at line {line}: Duplicate variable '{name}' in the same scope."
        self.scopes[-1].add(name)
        return None

    def lookup_variable(self, name: str, line: int) -> bool:
        for scope in reversed(self.scopes):
            if name in scope:
                return True
        self.errors.append(f"Error at line {line}: Undefined variable '{name}'.")
        return False

    def declare_function(self, name: str, line: int) -> Optional[str]:
        if name in self.function_names:
            return f"Error at line {line}: Duplicate function name '{name}'."
        self.function_names.add(name)
        return None

    def push_tag(self, tag: str, line: int):
        self.tag_stack.append((tag, line))

    def pop_tag(self, tag: str, line: int) -> Optional[str]:
        if not self.tag_stack:
            return f"Error at line {line}: Closing tag '{tag}' without matching opening tag."
        open_tag, open_line = self.tag_stack.pop()
        if open_tag != tag:
            return f"Error at line {line}: Mismatched tags: opened with '{open_tag}' at line {open_line} but closed with '{tag}'."
        return None

    def declare_hook(self, hook: str, line: int) -> Optional[str]:
        self.imported_hooks.add(hook)
        return None

    def check_hook(self, hook: str, line: int) -> Optional[str]:
        if hook not in self.imported_hooks:
            return f"Error at line {line}: Hook '{hook}' used without import."
        return None

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

class ImportExpression(Expression):
    def __init__(self, hooks: List[str], line: int):
        self.hooks = hooks
        self.line = line

    def interpret(self, context: Context) -> None:
        for hook in self.hooks:
            error = context.declare_hook(hook, self.line)
            if error:
                context.errors.append(error)

class FunctionDeclarationExpression(Expression):
    def __init__(self, name: str, line: int, params: List[str], body: List[Expression]):
        self.name = name
        self.line = line
        self.params = params
        self.body = body

    def interpret(self, context: Context) -> None:
        error = context.declare_function(self.name, self.line)
        if error:
            context.errors.append(error)
        context.enter_scope()
        for param in self.params:
            error = context.declare_variable(param, self.line)
            if error:
                context.errors.append(error)
        for expr in self.body:
            expr.interpret(context)
        context.exit_scope()

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

class VariableDeclarationExpression(Expression):
    def __init__(self, name: str, line: int, value: Optional[Expression] = None):
        self.name = name
        self.line = line
        self.value = value

    def interpret(self, context: Context) -> None:
        error = context.declare_variable(self.name, self.line)
        if error:
            context.errors.append(error)
        if self.value:
            self.value.interpret(context)

class ValueIndicatorExpression(Expression):
    def __init__(self, name: str, line: int):
        self.name = name
        self.line = line

    def interpret(self, context: Context) -> None:
        context.lookup_variable(self.name, self.line)

class ReturnStatementExpression(Expression):
    def __init__(self, element: Expression, line: int):
        self.element = element
        self.line = line

    def interpret(self, context: Context) -> None:
        self.element.interpret(context)

class StringExpression(Expression):
    def __init__(self, value: str, line: int):
        self.value = value
        self.line = line

    def interpret(self, context: Context) -> None:
        pass  # Strings are valid by default

class NumberExpression(Expression):
    def __init__(self, value: str, line: int):
        self.value = value
        self.line = line

    def interpret(self, context: Context) -> None:
        pass  # Numbers are valid by default

class StateSetterExpression(Expression):
    def __init__(self, state_pair: List[str], initial_value: Optional[Expression], line: int):
        self.state_pair = state_pair
        self.initial_value = initial_value
        self.line = line

    def interpret(self, context: Context) -> None:
        error = context.check_hook("useState", self.line)
        if error:
            context.errors.append(error)
        for name in self.state_pair:
            error = context.declare_variable(name, self.line)
            if error:
                context.errors.append(error)
        if self.initial_value:
            self.initial_value.interpret(context)

class ArrayExpression(Expression):
    def __init__(self, values: List[Expression], line: int):
        self.values = values
        self.line = line

    def interpret(self, context: Context) -> None:
        for value in self.values:
            value.interpret(context)

class BigIntExpression(Expression):
    def __init__(self, value: str, line: int):
        self.value = value
        self.line = line

    def interpret(self, context: Context) -> None:
        pass  # BigInt is valid by default

class DateExpression(Expression):
    def __init__(self, line: int):
        self.line = line

    def interpret(self, context: Context) -> None:
        pass  # Date is valid by default

class UseEffectExpression(Expression):
    def __init__(self, callback: Optional[Expression], dependencies: List[str], line: int):
        self.callback = callback
        self.dependencies = dependencies
        self.line = line

    def interpret(self, context: Context) -> None:
        error = context.check_hook("useEffect", self.line)
        if error:
            context.errors.append(error)
        if self.callback:
            self.callback.interpret(context)
        for dep in self.dependencies:
            context.lookup_variable(dep, self.line)

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

class ConsoleCommandExpression(Expression):
    def __init__(self, arg: Optional[Expression], line: int):
        self.arg = arg
        self.line = line

    def interpret(self, context: Context) -> None:
        if self.arg:
            self.arg.interpret(context)

class ArrowFunctionExpression(Expression):
    def __init__(self, params: List[str], body: List[Expression], line: int):
        self.params = params
        self.body = body
        self.line = line

    def interpret(self, context: Context) -> None:
        context.enter_scope()
        for param in self.params:
            error = context.declare_variable(param, self.line)
            if error:
                context.errors.append(error)
        for expr in self.body:
            expr.interpret(context)
        context.exit_scope()