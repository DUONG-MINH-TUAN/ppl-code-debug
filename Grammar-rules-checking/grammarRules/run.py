import sys
import os
import subprocess
import json
import traceback
from typing import List, Set
from dotenv import load_dotenv
import re
from antlr4 import *
from CompiledFiles.codeDebugLexer import codeDebugLexer
from CompiledFiles.codeDebugParser import codeDebugParser
from antlr4.error.ErrorListener import ErrorListener

# Define base Expression class
class Expression:
    def __init__(self, line: int):
        self.line = line

    def interpret(self, context):
        pass

# Define non-terminal expressions
class ProgramExpression(Expression):
    def __init__(self, import_stmt, functions):
        super().__init__(0)
        self.import_stmt = import_stmt
        self.functions = functions

    def interpret(self, context):
        print(f"Interpreting ProgramExpression", file=sys.stderr)
        context.current_scope = "global"
        if self.import_stmt:
            self.import_stmt.interpret(context)
        for func in self.functions:
            func.interpret(context)

class FunctionDeclarationExpression(Expression):
    def __init__(self, name, line, params, body):
        super().__init__(line)
        self.name = name
        self.params = params
        self.body = body

    def interpret(self, context):
        print(f"Interpreting FunctionDeclarationExpression: {self.name}", file=sys.stderr)
        context.current_scope = self.name
        for param in self.params:
            context.add_symbol(param, self.name)
        for expr in self.body:
            expr.interpret(context)
        context.current_scope = "global"

class ElementExpression(Expression):
    def __init__(self, open_tag, close_tag, line, content):
        super().__init__(line)
        self.open_tag = open_tag
        self.close_tag = close_tag
        self.content = content

    def interpret(self, context):
        for content in self.content:
            content.interpret(context)

class VariableDeclarationExpression(Expression):
    def __init__(self, name, line, value):
        super().__init__(line)
        self.name = name
        self.value = value

    def interpret(self, context):
        context.add_symbol(self.name, context.current_scope)
        if self.value:
            self.value.interpret(context)

class ReturnStatementExpression(Expression):
    def __init__(self, element, line):
        super().__init__(line)
        self.element = element

    def interpret(self, context):
        self.element.interpret(context)

class StateSetterExpression(Expression):
    def __init__(self, state_pair, initial_value, line):
        super().__init__(line)
        self.state_pair = state_pair
        self.initial_value = initial_value

    def interpret(self, context):
        print(f"Interpreting StateSetterExpression: {self.state_pair}", file=sys.stderr)
        context.add_symbol(self.state_pair[0], context.current_scope)  # Add state variable
        context.add_symbol(self.state_pair[1], context.current_scope)  # Add setter function
        context.check_hook("useState", self.line, context.current_scope, initial_value=self.initial_value)
        if self.initial_value:
            self.initial_value.interpret(context)

class ArrayExpression(Expression):
    def __init__(self, values, line):
        super().__init__(line)
        self.values = values

    def interpret(self, context):
        for value in self.values:
            value.interpret(context)

class UseEffectExpression(Expression):
    def __init__(self, callback, deps, line):
        super().__init__(line)
        self.callback = callback
        self.deps = deps

    def interpret(self, context):
        print(f"Interpreting UseEffectExpression at line {self.line}", file=sys.stderr)
        context.check_hook("useEffect", self.line, context.current_scope, self.callback, self.deps)
        if self.callback:
            self.callback.interpret(context)

class UseCallbackExpression(Expression):
    def __init__(self, callback, deps, line):
        super().__init__(line)
        self.callback = callback
        self.deps = deps

    def interpret(self, context):
        print(f"Interpreting UseCallbackExpression at line {self.line}", file=sys.stderr)
        context.check_hook("useCallback", self.line, context.current_scope, self.callback, self.deps)
        if self.callback:
            self.callback.interpret(context)

class ConsoleCommandExpression(Expression):
    def __init__(self, arg, line):
        super().__init__(line)
        self.arg = arg

    def interpret(self, context):
        if self.arg:
            self.arg.interpret(context)

class HookCallExpression(Expression):
    def __init__(self, name, args, line):
        super().__init__(line)
        self.name = name
        self.args = args

    def interpret(self, context):
        print(f"Interpreting HookCallExpression: {self.name} at line {self.line}", file=sys.stderr)
        context.check_hook(self.name, self.line, context.current_scope, deps=self.args)


class ArrowFunctionExpression(Expression):
    def __init__(self, params, body, line):
        super().__init__(line)
        self.params = params
        self.body = body

    def interpret(self, context):
        for expr in self.body:
            expr.interpret(context)

class ForExpression(Expression):
    def __init__(self, var_name, iterable, body, line):
        super().__init__(line)
        self.var_name = var_name
        self.iterable = iterable
        self.body = body

    def interpret(self, context):
        context.add_symbol(self.var_name, context.current_scope)
        for expr in self.body:
            expr.interpret(context)

class IfExpression(Expression):
    def __init__(self, condition, then_block, else_block, line):
        super().__init__(line)
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def interpret(self, context):
        self.condition.interpret(context)
        for expr in self.then_block:
            expr.interpret(context)
        for expr in self.else_block:
            expr.interpret(context)

# Define terminal expressions
class StringExpression(Expression):
    def __init__(self, value, line):
        super().__init__(line)
        self.value = value

class NumberExpression(Expression):
    def __init__(self, value, line):
        super().__init__(line)
        self.value = value

class ImportExpression(Expression):
    def __init__(self, hooks, line):
        super().__init__(line)
        self.hooks = hooks

class ValueIndicatorExpression(Expression):
    def __init__(self, name, line):
        super().__init__(line)
        self.name = name

class BigIntExpression(Expression):
    def __init__(self, value, line):
        super().__init__(line)
        self.value = value

class DateExpression(Expression):
    def __init__(self, line):
        super().__init__(line)

class BooleanExpression(Expression):
    def __init__(self, value, line):
        super().__init__(line)
        self.value = value

class BinaryExpression(Expression):
    def __init__(self, op, left, right, line):
        super().__init__(line)
        self.op = op
        self.left = left
        self.right = right

    def interpret(self, context):
        self.left.interpret(context)
        self.right.interpret(context)

# Context class to manage scope and errors
class Context:
    def __init__(self, input_lines):
        self.errors = []
        self.input_lines = input_lines
        self.current_scope = "global"
        self.symbols = {}  # scope -> set of variable names
        self.imported_names = set()  # Track imported names
        self.props = set()  # Track component props

    def add_symbol(self, name: str, scope: str):
        """Add a variable to the symbol table for a given scope."""
        if scope not in self.symbols:
            self.symbols[scope] = set()
        self.symbols[scope].add(name)

    def check_symbol(self, name: str, scope: str) -> bool:
        """Check if a variable is defined in the given scope, imports, or props."""
        return (name in self.symbols.get(scope, set()) or 
                name in self.imported_names or 
                name in self.props)

    def add_import(self, name: str):
        """Add an imported name."""
        self.imported_names.add(name)

    def add_prop(self, name: str):
        """Add a prop name."""
        self.props.add(name)

    def collect_identifiers(self, expr, identifiers: set):
        """Recursively collect identifiers from an expression."""
        if isinstance(expr, ValueIndicatorExpression):
            identifiers.add(expr.name)
        elif isinstance(expr, StateSetterExpression):
            identifiers.add(expr.state_pair[0])  # State variable
            identifiers.add(expr.state_pair[1])  # Setter function (e.g., setData)
            if expr.initial_value:
                self.collect_identifiers(expr.initial_value, identifiers)
        elif isinstance(expr, VariableDeclarationExpression):
            identifiers.add(expr.name)
            if expr.value:
                self.collect_identifiers(expr.value, identifiers)
        elif isinstance(expr, ConsoleCommandExpression):
            if expr.arg:
                self.collect_identifiers(expr.arg, identifiers)
        elif isinstance(expr, ArrowFunctionExpression):
            for content in expr.body:
                self.collect_identifiers(content, identifiers)
        elif isinstance(expr, ArrayExpression):
            for value in expr.values:
                self.collect_identifiers(value, identifiers)
        elif isinstance(expr, BinaryExpression):
            self.collect_identifiers(expr.left, identifiers)
            self.collect_identifiers(expr.right, identifiers)
        elif isinstance(expr, (list, tuple)):
            for item in expr:
                self.collect_identifiers(item, identifiers)

    def check_hook(self, hook_type: str, line: int, scope: str, callback: Expression = None, deps: List[str] = None, initial_value: Expression = None):
        """Validate hook usage and dependencies."""
        print(f"Checking hook: {hook_type} at line {line}, scope: {scope}", file=sys.stderr)

        # Check if hook is called inside a component
        if scope == "global":
            self.errors.append({
                "error": f"Invalid {hook_type} call at line {line}: Hooks can only be called inside a React component or custom hook.",
                "suggestion": f"Move the {hook_type} call inside a component function."
            })

        # Specific checks for useState
        if hook_type == "useState":
            if initial_value and isinstance(initial_value, ValueIndicatorExpression):
                if not self.check_symbol(initial_value.name, scope):
                    self.errors.append({
                        "error": f"{hook_type} at line {line} uses undefined variable '{initial_value.name}' as initial value.",
                        "suggestion": f"Ensure '{initial_value.name}' is defined or use a valid initial value (e.g., 0, null)."
                    })

        # Specific checks for useEffect and useCallback
        if hook_type in ["useEffect", "useCallback"] and callback and deps is not None:
            identifiers = set()
            self.collect_identifiers(callback, identifiers)

            # Check for undefined variables
            for ident in identifiers:
                if not self.check_symbol(ident, scope):
                    self.errors.append({
                        "error": f"{hook_type} at line {line} references undefined variable '{ident}'.",
                        "suggestion": f"Ensure '{ident}' is defined (e.g., via useState or props) before using it in {hook_type}."
                    })
                elif ident not in deps and ident not in self.props:  # Props are stable, don't need to be in deps
                    self.errors.append({
                        "error": f"{hook_type} at line {line} has missing dependency: '{ident}' is used but not in the dependency array.",
                        "suggestion": f"Add '{ident}' to the dependency array."
                    })

            # Check for empty dependency array with used variables
            if not deps and identifiers:
                self.errors.append({
                    "error": f"{hook_type} at line {line} uses variables {identifiers} but has an empty dependency array, which may cause stale closures.",
                    "suggestion": f"Include used variables {identifiers} in the dependency array or remove them from the {hook_type} callback."
                })

            # For useEffect: Check for side effects needing cleanup
            if hook_type == "useEffect":
                # Only flag side effects for known persistent operations (grammar limits detection)
                has_persistent_side_effect = False  # Can't detect setInterval, etc., due to grammar
                if has_persistent_side_effect:
                    self.errors.append({
                        "error": f"{hook_type} at line {line} sets up a persistent side effect but lacks a cleanup function.",
                        "suggestion": f"Return a cleanup function from useEffect (e.g., clearInterval) to prevent memory leaks."
                    })

# Constants
DIR = os.path.dirname(__file__)
CPL_DEST = "CompiledFiles"
LEXER_SRC = "codeDebugLexer.g4"
PARSER_SRC = "codeDebugParser.g4"
TEMP_FILE = "temp.js"

# Load environment variables
load_dotenv()
ANTLR_JAR = os.getenv("ANTLR_DIR")

def print_usage():
    """Print usage instructions for the script."""
    print("python run.py gen", file=sys.stderr)
    print("python run.py test \"<input string>\"", file=sys.stderr)
    sys.stderr.flush()

def print_break():
    """Print a separator line for better log readability."""
    print("-----------------------------------------------", file=sys.stderr)
    sys.stderr.flush()

def generate_antlr2python():
    """Generate Python lexer and parser files using ANTLR."""
    print("Antlr4 is running...", file=sys.stderr)
    os.makedirs(CPL_DEST, exist_ok=True)
    print(f"Generating lexer from {LEXER_SRC}...", file=sys.stderr)
    subprocess.run(["java", "-jar", ANTLR_JAR, "-o", CPL_DEST, "-no-listener", "-Dlanguage=Python3", LEXER_SRC])
    print(f"Generating parser from {PARSER_SRC}...", file=sys.stderr)
    subprocess.run(["java", "-jar", ANTLR_JAR, "-o", CPL_DEST, "-no-listener", "-Dlanguage=Python3", PARSER_SRC])
    print("Generate successfully", file=sys.stderr)
    sys.stderr.flush()

def clean_input(input_string: str) -> str:
    """Clean the input string to remove unwanted characters and normalize format."""
    input_string = input_string.strip()
    if input_string.startswith('"') and input_string.endswith('"'):
        input_string = input_string[1:-1]
    elif input_string.startswith("'") and input_string.endswith("'"):
        input_string = input_string[1:-1]
    
    input_string = re.sub(r'\\(["\'])', r'\1', input_string)
    input_string = re.sub(r'\s+', ' ', input_string).strip()
    lines = input_string.replace(';', ';\n').replace('{', '{\n').replace('}', '\n}')
    return '\n'.join(line.strip() for line in lines.split('\n') if line.strip())

class CustomErrorListener(ErrorListener):
    """Custom error listener for ANTLR syntax errors."""
    def __init__(self, input_content):
        self.errors = []
        self.input_lines = input_content.splitlines()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        token_map = {
            "RIGHT_PARENTHESIS": "closing parenthesis `)`",
            "LEFT_PARENTHESIS": "opening parenthesis `(`",
            "RIGHT_BRACE": "closing brace `}`",
            "LEFT_BRACE": "opening brace `{`",
            "SEMICOLON": "semicolon `;`",
            "COMMA": "comma `,`",
            "EQUAL": "equals sign `=`",
            "IMPLIE": "arrow `=>`"
        }
        error_message = f"Syntax error at line {line}, column {column}: "
        suggestion = ""
        offending_token = offendingSymbol.text if offendingSymbol else "<unknown>"

        if "missing" in msg.lower():
            missing_token = msg.split("missing ")[1].split(" at")[0].strip("'")
            missing_token = token_map.get(missing_token, missing_token)
            error_message += f"Missing {missing_token} before '{offending_token}'."
            suggestion = f"Try adding a {missing_token} before '{offending_token}'."
        elif "mismatched input" in msg.lower():
            expected_token = msg.split("expecting ")[1].strip() if "expecting" in msg else "<unknown>"
            expected_token = token_map.get(expected_token, expected_token)
            error_message += f"Found '{offending_token}' but expected {expected_token}."
            suggestion = f"Replace '{offending_token}' with {expected_token} or check the syntax near this position."
        elif "extraneous input" in msg.lower():
            expected_token = msg.split("expecting ")[1].strip() if "expecting" in msg else "<unknown>"
            expected_token = token_map.get(expected_token, expected_token)
            error_message += f"Unexpected '{offending_token}', expected {expected_token}."
            suggestion = f"Remove or replace '{offending_token}' with {expected_token}."
        else:
            error_message += msg
            suggestion = "Review the syntax at this line."

        if line <= len(self.input_lines):
            error_message += f"\nLine {line}: {self.input_lines[line-1].strip()}"
            error_message += f"\n{' ' * (column + len(str(line)) + 2)}^"
        self.errors.append({
            "error": error_message,
            "suggestion": suggestion
        })

class ASTBuilder:
    """Builds an Abstract Syntax Tree (AST) from the ANTLR parse tree."""
    def build(self, ctx, input_lines: List[str]) -> Expression:
        print(f"Building AST for {type(ctx).__name__}", file=sys.stderr)
        sys.stderr.flush()
        return self.visit(ctx, input_lines)
    def visit(self, ctx, input_lines: List[str]) -> Expression:
        print(f"Visiting {type(ctx).__name__}", file=sys.stderr)
        sys.stderr.flush()
        if isinstance(ctx, codeDebugParser.ProgramContext):
            import_stmt = self.visit(ctx.main_structure().import_statement(), input_lines) if ctx.main_structure().import_statement() else None
            functions = [self.visit(node, input_lines) for node in ctx.main_structure().getChildren() if not isinstance(node, codeDebugParser.Import_statementContext)]
            return ProgramExpression(import_stmt, functions)
        elif isinstance(ctx, codeDebugParser.Import_statementContext):
            hooks = [ctx.hook(i).getText() for i in range(len(ctx.hook()))]
            line = ctx.start.line
            return ImportExpression(hooks, line)
        elif isinstance(ctx, codeDebugParser.Function_declarationContext):
            name = ctx.IDENTIFIER().getText()
            line = ctx.IDENTIFIER().symbol.line
            params = []
            if ctx.parameter_list() and ctx.parameter_list().parameter():
                param_nodes = ctx.parameter_list().parameter()
                if isinstance(param_nodes, list):
                    params = [param.getText() for param in param_nodes if hasattr(param, 'getText')]
                else:
                    params = [param_nodes.getText()] if hasattr(param_nodes, 'getText') else []
            body = []
            if ctx.body_function() and ctx.body_function().content():
                content_nodes = ctx.body_function().content()
                if isinstance(content_nodes, list):
                    body = [self.visit(content, input_lines) for content in content_nodes]
                else:
                    body = [self.visit(content_nodes, input_lines)]
            return FunctionDeclarationExpression(name, line, params, body)
        elif isinstance(ctx, codeDebugParser.StatementContext):
            if ctx.variableDeclaration():
                return self.visit(ctx.variableDeclaration(), input_lines)
            elif ctx.consoleCommand():
                return self.visit(ctx.consoleCommand(), input_lines)
            elif ctx.ifStatement():
                return self.visit(ctx.ifStatement(), input_lines)
            elif ctx.forStatement():
                return self.visit(ctx.forStatement(), input_lines)
            elif ctx.useEffectCall():
                return self.visit(ctx.useEffectCall(), input_lines)
            elif ctx.hookCall():
                return self.visit(ctx.hookCall(), input_lines)
            elif ctx.useCallbackCall():
                return self.visit(ctx.useCallbackCall(), input_lines)
            elif ctx.stateSetter():
                return self.visit(ctx.stateSetter(), input_lines)
            elif ctx.bigIntDeclaration():
                return self.visit(ctx.bigIntDeclaration(), input_lines)
            elif ctx.numberDeclaration():
                return self.visit(ctx.numberDeclaration(), input_lines)
            elif ctx.stringDeclaration():
                return self.visit(ctx.stringDeclaration(), input_lines)
            elif ctx.arrowFunction():
                return self.visit(ctx.arrowFunction(), input_lines)
            elif ctx.arrayDeclaration():
                return self.visit(ctx.arrayDeclaration(), input_lines)
            elif ctx.dateDeclaration():
                return self.visit(ctx.dateDeclaration(), input_lines)
            else:
                raise ValueError(f"Unhandled statement child: {ctx.getText()}")
        elif isinstance(ctx, codeDebugParser.ContentContext):
            if ctx.stateSetter():
                return self.visit(ctx.stateSetter(), input_lines)
            elif ctx.useEffectCall():
                return self.visit(ctx.useEffectCall(), input_lines)
            elif ctx.useCallbackCall():
                return self.visit(ctx.useCallbackCall(), input_lines)
            elif ctx.bigIntDeclaration():
                return self.visit(ctx.bigIntDeclaration(), input_lines)
            elif ctx.numberDeclaration():
                return self.visit(ctx.numberDeclaration(), input_lines)
            elif ctx.stringDeclaration():
                return self.visit(ctx.stringDeclaration(), input_lines)
            elif ctx.arrowFunction():
                return self.visit(ctx.arrowFunction(), input_lines)
            elif ctx.arrayDeclaration():
                return self.visit(ctx.arrayDeclaration(), input_lines)
            elif ctx.consoleCommand():
                return self.visit(ctx.consoleCommand(), input_lines)
            elif ctx.dateDeclaration():
                return self.visit(ctx.dateDeclaration(), input_lines)
            elif ctx.return_statement():
                return self.visit(ctx.return_statement(), input_lines)
            elif ctx.variableDeclaration():
                return self.visit(ctx.variableDeclaration(), input_lines)
            elif ctx.forStatement():
                return self.visit(ctx.forStatement(), input_lines)
            elif ctx.ifStatement():
                return self.visit(ctx.ifStatement(), input_lines)
            elif ctx.hookCall():
                hook_name = ctx.hookCall().IDENTIFIER().getText() if ctx.hookCall().IDENTIFIER() else "unknown"
                line = ctx.start.line
                return ValueIndicatorExpression(hook_name, line)
            else:
                raise ValueError(f"Unhandled content child: {ctx.getText()}")
        elif isinstance(ctx, codeDebugParser.ElementContext):
            open_tag = ctx.openTag().getText().lstrip('<').rstrip('>') if ctx.openTag() else ""
            close_tag = ctx.closeTag().IDENTIFIER().getText() if ctx.closeTag() else ""
            line = ctx.start.line
            content = [self.visit(content, input_lines) for content in ctx.elementContent()] if ctx.elementContent() else []
            return ElementExpression(open_tag, close_tag, line, content)
        elif isinstance(ctx, codeDebugParser.SelfClosingTagContext):
            tag = ctx.JSX_OPEN_TAG().getText().lstrip('<').rstrip('>')
            line = ctx.start.line
            return ElementExpression(tag, tag, line, [])
        elif isinstance(ctx, codeDebugParser.FragmentOpenContext) or isinstance(ctx, codeDebugParser.FragmentCloseContext) or isinstance(ctx, codeDebugParser.EmptyFragmentContext):
            return ElementExpression("", "", ctx.start.line, [])
        elif isinstance(ctx, codeDebugParser.ElementContentContext):
            if ctx.element():
                return self.visit(ctx.element(), input_lines)
            elif ctx.valueIndicator():
                return self.visit(ctx.valueIndicator(), input_lines)
            elif ctx.TAG_TEXT():
                return StringExpression(ctx.TAG_TEXT().getText(), ctx.start.line)
            elif ctx.JSX_ATTR():
                attr_text = ctx.JSX_ATTR().getText()
                match = re.match(r'ref=\{(\w+)\}', attr_text)
                if match:
                    identifier = match.group(1)
                    return ValueIndicatorExpression(identifier, ctx.start.line)
                return StringExpression(attr_text, ctx.start.line)
            else:
                raise ValueError(f"Unhandled elementContent child: {ctx.getText()}")
        elif isinstance(ctx, codeDebugParser.VariableDeclarationContext):
            name = ctx.IDENTIFIER().getText()
            line = ctx.IDENTIFIER().symbol.line
            value = None
            if ctx.stringValue():
                value = self.visit(ctx.stringValue(), input_lines)
            elif ctx.NUMBER():
                value = NumberExpression(ctx.NUMBER().getText(), line)
            elif ctx.boolean():
                value = BooleanExpression(ctx.boolean().getText().lower() == "true", line)
            elif ctx.BIGINT_LITERAL():
                value = BigIntExpression(ctx.BIGINT_LITERAL().getText(), line)
            elif ctx.NULL():
                value = StringExpression("null", line)
            elif ctx.SYMBOL_FUNC():
                value = StringExpression("Symbol()", line)
            elif ctx.array():
                value = self.visit(ctx.array(), input_lines)
            elif ctx.NEW():
                value = DateExpression(line)
            return VariableDeclarationExpression(name, line, value)
        elif isinstance(ctx, codeDebugParser.BigIntDeclarationContext):
            name = ctx.IDENTIFIER().getText()
            line = ctx.IDENTIFIER().symbol.line
            value = BigIntExpression(ctx.BIGINT_LITERAL().getText(), line)
            return VariableDeclarationExpression(name, line, value)
        elif isinstance(ctx, codeDebugParser.NumberDeclarationContext):
            name = ctx.IDENTIFIER().getText()
            line = ctx.IDENTIFIER().symbol.line
            value = NumberExpression(ctx.NUMBER()[0].getText(), line)
            return VariableDeclarationExpression(name, line, value)
        elif isinstance(ctx, codeDebugParser.StringDeclarationContext):
            name = ctx.IDENTIFIER().getText()
            line = ctx.IDENTIFIER().symbol.line
            value = self.visit(ctx.stringValue(), input_lines)
            return VariableDeclarationExpression(name, line, value)
        elif isinstance(ctx, codeDebugParser.StateSetterContext):
            state_pair = [ctx.statePair().IDENTIFIER()[0].getText(), ctx.statePair().IDENTIFIER()[1].getText()]
            initial_value = self.visit(ctx.initialValue(), input_lines) if ctx.initialValue() else None
            line = ctx.start.line
            return StateSetterExpression(state_pair, initial_value, line)
        elif isinstance(ctx, codeDebugParser.UseEffectCallContext):
            callback = self.visit(ctx.callbackFunction(), input_lines) if ctx.callbackFunction() else None
            deps = []
            if ctx.dependencyArray() and ctx.dependencyArray().parameter():
                param_nodes = ctx.dependencyArray().parameter()
                if isinstance(param_nodes, list):
                    deps = [param.getText() for param in param_nodes if hasattr(param, 'getText')]
                else:
                    deps = [param_nodes.getText()] if hasattr(param_nodes, 'getText') else []
            line = ctx.start.line
            return UseEffectExpression(callback, deps, line)
        elif isinstance(ctx, codeDebugParser.UseCallbackCallContext):
            callback = self.visit(ctx.callbackFunction(), input_lines) if ctx.callbackFunction() else None
            deps = []
            if ctx.dependencyArray() and ctx.dependencyArray().parameter():
                param_nodes = ctx.dependencyArray().parameter()
                if isinstance(param_nodes, list):
                    deps = [param.getText() for param in param_nodes if hasattr(param, 'getText')]
                else:
                    deps = [param_nodes.getText()] if hasattr(param_nodes, 'getText') else []
            line = ctx.start.line
            return UseCallbackExpression(callback, deps, line)
        elif isinstance(ctx, codeDebugParser.CallbackFunctionContext):
            body = []
            if ctx.content():
                content_nodes = ctx.content()
                if isinstance(content_nodes, list):
                    body = [self.visit(content, input_lines) for content in content_nodes]
                else:
                    body = [self.visit(content_nodes, input_lines)]
            line = ctx.start.line
            return ArrowFunctionExpression([], body, line)
        elif isinstance(ctx, codeDebugParser.ArrowFunctionContext):
            params = []
            if ctx.parameter_list() and ctx.parameter_list().parameter():
                param_nodes = ctx.parameter_list().parameter()
                if isinstance(param_nodes, list):
                    params = [param.getText() for param in param_nodes if hasattr(param, 'getText')]
                else:
                    params = [param_nodes.getText()] if hasattr(param_nodes, 'getText') else []
            body = []
            if ctx.content():
                content_nodes = ctx.content()
                if isinstance(content_nodes, list):
                    body = [self.visit(content, input_lines) for content in content_nodes]
                else:
                    body = [self.visit(content_nodes, input_lines)]
            line = ctx.start.line
            return ArrowFunctionExpression(params, body, line)
        elif isinstance(ctx, codeDebugParser.ConsoleCommandContext):
            arg = None
            if ctx.stringValue():
                arg = self.visit(ctx.stringValue(), input_lines)
            elif ctx.IDENTIFIER():
                arg = ValueIndicatorExpression(ctx.IDENTIFIER().getText(), ctx.IDENTIFIER().symbol.line)
            line = ctx.start.line
            return ConsoleCommandExpression(arg, line)
        elif isinstance(ctx, codeDebugParser.ArrayContext):
            values = [self.visit(value, input_lines) for value in ctx.arrayValue()] if ctx.arrayValue() else []
            line = ctx.start.line
            return ArrayExpression(values, line)
        elif isinstance(ctx, codeDebugParser.StringArrayContext):
            values = [self.visit(value, input_lines) for value in ctx.stringValue()]
            line = ctx.start.line
            return ArrayExpression(values, line)
        elif isinstance(ctx, codeDebugParser.NumberArrayContext):
            values = [NumberExpression(num.getText(), ctx.start.line) for num in ctx.NUMBER()]
            line = ctx.start.line
            return ArrayExpression(values, line)
        elif isinstance(ctx, codeDebugParser.StringValueContext):
            value = ctx.getText()
            line = ctx.start.line
            return StringExpression(value, line)
        elif isinstance(ctx, codeDebugParser.InitialValueContext):
            if ctx.valueForInitialization():
                value = self.visit(ctx.valueForInitialization()[0], input_lines)
                line = ctx.start.line
                return value
            return None
        elif isinstance(ctx, codeDebugParser.ValueForInitializationContext):
            line = ctx.start.line
            # Handle stringValue first to catch empty strings via StringValueContext
            if ctx.stringValue():
                return self.visit(ctx.stringValue(), input_lines)
            elif ctx.NUMBER():
                return NumberExpression(ctx.NUMBER()[0].getText(), line)
            elif ctx.BOOLEAN():
                value = ctx.BOOLEAN()[0].getText().lower() == "true"
                return BooleanExpression(value, line)
            elif ctx.IDENTIFIER():
                return ValueIndicatorExpression(ctx.IDENTIFIER().getText(), line)
            elif ctx.array():
                return self.visit(ctx.array(), input_lines)
            elif ctx.NULL():
                return StringExpression(ctx.NULL()[0].getText(), line)
            elif ctx.SYMBOL_FUNC():
                return StringExpression(ctx.SYMBOL_FUNC()[0].getText(), line)
            elif ctx.NEW():
                return DateExpression(line)
            else:
                raise ValueError(f"Unhandled valueForInitialization child: {ctx.getText()}")
        elif isinstance(ctx, codeDebugParser.ValueIndicatorContext):
            name = ctx.IDENTIFIER().getText()
            line = ctx.IDENTIFIER().symbol.line
            return ValueIndicatorExpression(name, line)
        elif isinstance(ctx, codeDebugParser.Return_statementContext):
            element = self.visit(ctx.element(), input_lines)
            line = ctx.start.line
            return ReturnStatementExpression(element, line)
        elif isinstance(ctx, codeDebugParser.ForStatementContext):
            var_name = ctx.IDENTIFIER()[0].getText()
            iterable = ctx.IDENTIFIER()[1].getText()
            body = [self.visit(content, input_lines) for content in ctx.block().blockContent()] if ctx.block().blockContent() else []
            line = ctx.start.line
            return ForExpression(var_name, iterable, body, line)
        elif isinstance(ctx, codeDebugParser.IfStatementContext):
            condition = self.visit(ctx.expression(), input_lines)
            then_block = [self.visit(content, input_lines) for content in ctx.block(0).blockContent()] if ctx.block(0).blockContent() else []
            else_block = [self.visit(content, input_lines) for content in ctx.block(1).blockContent()] if ctx.block(1) and ctx.block(1).blockContent() else []
            line = ctx.start.line
            return IfExpression(condition, then_block, else_block, line)
        elif isinstance(ctx, codeDebugParser.VarExprContext):
            return self.visit(ctx.valueIndicator(), input_lines)
        elif isinstance(ctx, codeDebugParser.NumExprContext):
            return NumberExpression(ctx.NUMBER().getText(), ctx.start.line)
        elif isinstance(ctx, codeDebugParser.StrExprContext):
            return StringExpression(ctx.stringValue().getText(), ctx.start.line)
        elif isinstance(ctx, codeDebugParser.BoolExprContext):
            value = ctx.boolean().getText().lower() == "true"
            return BooleanExpression(value, ctx.start.line)
        elif isinstance(ctx, codeDebugParser.MulDivExprContext):
            left = self.visit(ctx.expression(0), input_lines)
            right = self.visit(ctx.expression(1), input_lines)
            op = "*" if ctx.MUL() else "/"
            return BinaryExpression(op, left, right, ctx.start.line)
        elif isinstance(ctx, codeDebugParser.AddSubExprContext):
            left = self.visit(ctx.expression(0), input_lines)
            right = self.visit(ctx.expression(1), input_lines)
            op = "+" if ctx.ADD() else "-"
            return BinaryExpression(op, left, right, ctx.start.line)
        elif isinstance(ctx, codeDebugParser.ParenExprContext):
            return self.visit(ctx.expression(), input_lines)
        elif isinstance(ctx, codeDebugParser.HookCallContext):
            hook_name = ctx.IDENTIFIER().getText()
            args = []
            if ctx.parameter_list() and ctx.parameter_list().parameter():
                param_nodes = ctx.parameter_list().parameter()
                if isinstance(param_nodes, list):
                    args = [param.getText() for param in param_nodes if hasattr(param, 'getText')]
                else:
                    args = [param_nodes.getText()] if hasattr(param_nodes, 'getText') else []
            return HookCallExpression(hook_name, args, ctx.start.line)
        else:
            print(f"Unhandled node type: {type(ctx).__name__}", file=sys.stderr)
            sys.stderr.flush()
            raise ValueError(f"Unhandled node type: {type(ctx).__name__}")
    
def collect_function_names(ast: Expression) -> Set[str]:
    """Collect all function names in the AST."""
    function_names = set()
    if isinstance(ast, ProgramExpression):
        for func in ast.functions:
            if isinstance(func, FunctionDeclarationExpression):
                function_names.add(func.name)
    return function_names

def check_element_tags(expr: Expression, function_names: Set[str], errors: List[dict]):
    """Check ElementExpression in AST for lowercase component names."""
    if isinstance(expr, ReturnStatementExpression):
        check_element_tags(expr.element, function_names, errors)
    elif isinstance(expr, ElementExpression):
        tag = expr.open_tag
        if tag and not tag[0].isupper():
            if tag in function_names:
                capitalized_tag = tag[0].upper() + tag[1:] if len(tag) > 1 else tag.upper()
                errors.append({
                    "error": f"Invalid React component name at line {expr.line}: '{tag}' is used as a component but does not start with an uppercase letter.",
                    "suggestion": f"Rename the function '{tag}' to '{capitalized_tag}' to use it as a React component."
                })
        for content in expr.content:
            check_element_tags(content, function_names, errors)
    elif isinstance(expr, (list, tuple)):
        for e in expr:
            check_element_tags(e, function_names, errors)

def process_input(input_content: str):
    """Process the input content through lexer, parser, AST, and interpreter."""
    if not input_content:
        print(json.dumps({"success": False, "errors": [{"error": "No input provided", "suggestion": "Provide valid JavaScript code."}]}))
        print("Run tests completely", file=sys.stderr)
        sys.stderr.flush()
        return

    # Get tokens for debugging
    print("List of token: ", file=sys.stderr)
    input_stream = InputStream(input_content)
    lexer = codeDebugLexer(input_stream)
    tokens = []
    token = lexer.nextToken()
    while token.type != Token.EOF:
        tokens.append(token.text)
        token = lexer.nextToken()
    tokens.append("<EOF>")
    print(",".join(tokens), file=sys.stderr)
    sys.stderr.flush()

    # Parse input
    lexer = codeDebugLexer(InputStream(input_content))
    token_stream = CommonTokenStream(lexer)
    parser = codeDebugParser(token_stream)
    parser.removeErrorListeners()
    error_listener = CustomErrorListener(input_content)
    parser.addErrorListener(error_listener)

    try:
        print("Parsing input...", file=sys.stderr)
        sys.stderr.flush()
        tree = parser.program()
        print("Parse tree:", file=sys.stderr)
        print(tree.toStringTree(recog=parser), file=sys.stderr)
        sys.stderr.flush()

        # If parse tree is successfully created, ignore syntax errors from error_listener
        if tree and not tree.getText().strip() == "":
            error_listener.errors = []  # Clear syntax errors if parse tree is valid

        # If there are syntax errors, return early
        if error_listener.errors:
            print(json.dumps({"success": False, "errors": error_listener.errors}, indent=2))
            print("Run tests completely", file=sys.stderr)
            sys.stderr.flush()
            return

        # Convert parse tree to Interpreter AST
        print("Building AST...", file=sys.stderr)
        sys.stderr.flush()
        context = Context(input_content.splitlines())
        
        # Handle imports and props
        import_matches = re.findall(r'import\s*{\s*([^}]+)\s*}\s*from\s*[\'"]([^\'"]+)[\'"]', input_content)
        for imports, _ in import_matches:
            for imp in imports.split(','):
                context.add_import(imp.strip())
        
        param_matches = re.findall(r'function\s+\w+\s*\(\s*{\s*([^}]+)\s*}\s*\)', input_content)
        for params in param_matches:
            for param in params.split(','):
                context.add_prop(param.strip())

        ast_builder = ASTBuilder()
        ast = ast_builder.build(tree, input_content.splitlines())
       
        if ast is None:
            print(json.dumps({"success": False, "errors": [{"error": "Failed to build AST", "suggestion": "Check for syntax errors in the input code."}]}, indent=2))
            print("Run tests completely", file=sys.stderr)
            sys.stderr.flush()
            return

        # Collect function names
        function_names = collect_function_names(ast)

        # Check for invalid React component names in return statements
        check_element_tags(ast, function_names, context.errors)

        # Interpret the AST
        print("Interpreting AST...", file=sys.stderr)
        sys.stderr.flush()
        ast.interpret(context)

        # Add warning for unsupported constructs
        if 'useRef' in input_content:
            context.errors.append({
                "error": "useRef hook detected, which is not supported by the current grammar.",
                "suggestion": "Remove useRef or extend the grammar to support it."
            })
        # Check for arrow functions only if they appear in a function context
        if '=>' in input_content and re.search(r'\bconst\s+\w+\s*=\s*\([^)]*\)\s*=>\s*{', input_content):
            context.errors.append({
                "error": "Arrow function declarations detected, which are not fully supported by the current grammar.",
                "suggestion": "Use traditional function declarations or extend the grammar to support arrow functions."
            })

        # Output results
        if error_listener.errors or context.errors:
            print(json.dumps({"success": False, "errors": error_listener.errors + context.errors}, indent=2))
        else:
            print(json.dumps({"success": True, "message": "Input accepted"}, indent=2))
    except Exception as e:
        print(f"Exception occurred: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        errors = error_listener.errors if error_listener.errors else [{"error": f"Error while building AST: {str(e)}", "suggestion": "Check for syntax errors or unsupported constructs."}]
        print(json.dumps({"success": False, "errors": errors}, indent=2))

    print("Run tests completely", file=sys.stderr)
    sys.stderr.flush()

    
def run_test():
    """Run test cases for the input content."""
    print("Running testcases...", file=sys.stderr)
    sys.stderr.flush()

    if len(sys.argv) < 3:
        # Fallback to stdin for compatibility with piped input
        input_content = sys.stdin.read().strip()
        process_input(input_content)
        return

    # Read and clean input from command-line argument
    input_content = sys.argv[2]
    cleaned_input = clean_input(input_content)

    # Write cleaned input to temporary file and process it
    try:
        with open(TEMP_FILE, "w", encoding="utf-8") as f:
            f.write(cleaned_input)
        cmd = f"type {TEMP_FILE} | python {sys.argv[0]} test"
        subprocess.run(cmd, shell=True)
    finally:
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)

def main(argv):
    """Main entry point for the script."""
    if len(argv) < 1:
        print_usage()
    elif argv[0] == "gen":
        generate_antlr2python()
    elif argv[0] == "test":
        run_test()
    else:
        print_usage()

if __name__ == "__main__":
    main(sys.argv[1:])