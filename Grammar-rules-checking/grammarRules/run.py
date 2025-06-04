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
from antlr4.tree.Tree import TerminalNode

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

class FunctionalComponentExpression(Expression):
    def __init__(self, name: str, params: List[str], body: Expression, line: int):
        super().__init__(line)
        self.name = name
        self.params = params
        self.body = body  # Element trả về

    def interpret(self, context):
        context.current_scope = self.name
        self.body.interpret(context)

class ClassComponentExpression(Expression):
    def __init__(self, name: str, methods: List[Expression], line: int):
        super().__init__(line)
        self.name = name
        self.methods = methods

    def interpret(self, context):
        context.current_scope = self.name
        for method in self.methods:
            method.interpret(context)

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

    def interpret(self, context):
        for hook in self.hooks:
            context.add_import(hook)

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
        self.symbols = {}
        self.functions = set()
        self.imported_names = set()
        self.props = set()

    def declare_function(self, name: str, line: int):
        self.functions.add(name)
        print(f"Declared function: {name} at line {line}", file=sys.stderr)

    def add_symbol(self, name: str, scope: str):
        if scope not in self.symbols:
            self.symbols[scope] = set()
        self.symbols[scope].add(name)

    def check_symbol(self, name: str, scope: str) -> bool:
        return (name in self.symbols.get(scope, set()) or 
                name in self.imported_names or 
                name in self.props)

    def add_import(self, name: str):
        self.imported_names.add(name)

    def add_prop(self, name: str):
        self.props.add(name)

    def collect_identifiers(self, expr, identifiers: set):
        if isinstance(expr, ValueIndicatorExpression):
            identifiers.add(expr.name)
        elif isinstance(expr, StateSetterExpression):
            identifiers.add(expr.state_pair[0])
            identifiers.add(expr.state_pair[1])
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
        print(f"Checking hook: {hook_type} at line {line}, scope: {scope}", file=sys.stderr)
        if scope == "global":
            self.errors.append({
                "error": f"Invalid {hook_type} call at line {line}: Hooks can only be called inside a React component or custom hook.",
                "suggestion": f"Move the {hook_type} call inside a component function."
            })
        if hook_type == "useState":
            if initial_value and isinstance(initial_value, ValueIndicatorExpression):
                if not self.check_symbol(initial_value.name, scope):
                    self.errors.append({
                        "error": f"{hook_type} at line {line} uses undefined variable '{initial_value.name}' as initial value.",
                        "suggestion": f"Ensure '{initial_value.name}' is defined or use a valid initial value (e.g., 0, null)."
                    })
        if hook_type in ["useEffect", "useCallback"] and callback and deps is not None:
            identifiers = set()
            self.collect_identifiers(callback, identifiers)
            for ident in identifiers:
                if not self.check_symbol(ident, scope):
                    self.errors.append({
                        "error": f"{hook_type} at line {line} references undefined variable '{ident}'.",
                        "suggestion": f"Ensure '{ident}' is defined (e.g., via useState or props) before using it in {hook_type}."
                    })
                elif ident not in deps and ident not in self.props:
                    self.errors.append({
                        "error": f"{hook_type} at line {line} has missing dependency: '{ident}' is used but not in the dependency array.",
                        "suggestion": f"Add '{ident}' to the dependency array."
                    })
            if not deps and identifiers:
                self.errors.append({
                    "error": f"{hook_type} at line {line} uses variables {identifiers} but has an empty dependency array, which may cause stale closures.",
                    "suggestion": f"Include used variables {identifiers} in the dependency array or remove them from the {hook_type} callback."
                })
            if hook_type == "useEffect":
                has_persistent_side_effect = False
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
    print("python run.py gen", file=sys.stderr)
    print("python run.py test \"<input string>\"", file=sys.stderr)
    sys.stderr.flush()

def print_break():
    print("-----------------------------------------------", file=sys.stderr)
    sys.stderr.flush()

def generate_antlr2python():
    print("Antlr4 is running...", file=sys.stderr)
    os.makedirs(CPL_DEST, exist_ok=True)
    print(f"Generating lexer from {LEXER_SRC}...", file=sys.stderr)
    subprocess.run(["java", "-jar", ANTLR_JAR, "-o", CPL_DEST, "-no-listener", "-Dlanguage=Python3", LEXER_SRC])
    print(f"Generating parser from {PARSER_SRC}...", file=sys.stderr)
    subprocess.run(["java", "-jar", ANTLR_JAR, "-o", CPL_DEST, "-no-listener", "-Dlanguage=Python3", PARSER_SRC])
    print("Generate successfully", file=sys.stderr)
    sys.stderr.flush()

def clean_input(input_string: str) -> str:
    input_string = input_string.strip()
    if (input_string.startswith('"') and input_string.endswith('"')) or (input_string.startswith("'") and input_string.endswith("'")):
        input_string = input_string[1:-1]
    lines = []
    in_string = False
    current_line = ""
    string_char = None
    i = 0
    while i < len(input_string):
        char = input_string[i]
        if char in ['"', "'"] and (i == 0 or input_string[i-1] != '\\'):
            if in_string and char == string_char:
                in_string = False
                string_char = None
            elif not in_string:
                in_string = True
                string_char = char
            current_line += char
        elif char == '\n' and not in_string:
            if current_line.strip():
                lines.append(current_line.strip())
            current_line = ""
        else:
            current_line += char
        i += 1
    if current_line.strip():
        lines.append(current_line.strip())
    result = []
    for line in lines:
        if not (line.startswith('"') and line.endswith('"')) and not (line.startswith("'") and line.endswith("'")):
            line = line.replace(';', ';\n').replace('{', '{\n').replace('}', '\n}')
        result.append(line)
    return '\n'.join(line for line in result if line.strip())

class CustomErrorListener(ErrorListener):
    def __init__(self, input_content):
        self.errors = []
        self.input_lines = input_content.splitlines()
        print(f"Input lines: {self.input_lines}", file=sys.stderr)

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
    def build(self, ctx, input_lines: List[str]) -> Expression:
        print(f"Building AST for {type(ctx).__name__}", file=sys.stderr)
        sys.stderr.flush()
        return self.visit(ctx, input_lines)

    def visit(self, ctx, input_lines: List[str]) -> Expression:
        print(f"Visiting {type(ctx).__name__}", file=sys.stderr)
        sys.stderr.flush()
        if isinstance(ctx, codeDebugParser.ProgramContext):
            print(f"ProgramContext children: {[child.getText() for child in ctx.main_structure().getChildren()]}", file=sys.stderr)
            import_stmt = self.visit(ctx.main_structure().import_statement(), input_lines) if ctx.main_structure().import_statement() else None
            functions = []
            for child in ctx.main_structure().getChildren():
                if isinstance(child, TerminalNode):
                    continue
                visited_node = self.visit(child, input_lines)
                if visited_node:
                    functions.append(visited_node)
                    print(f"Added to functions: {type(visited_node).__name__}, name={getattr(visited_node, 'name', 'N/A')}", file=sys.stderr)
            print(f"Total functions added: {len(functions)}", file=sys.stderr)
            return ProgramExpression(import_stmt, functions)
        elif isinstance(ctx, codeDebugParser.Statement_or_functionContext):
            result = None
            for child in ctx.getChildren():
                if not isinstance(child, TerminalNode):
                    visited = self.visit(child, input_lines)
                    if visited:
                        result = visited
            return result
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
                var_decl = self.visit(ctx.variableDeclaration(), input_lines)
                print(f"VariableDeclaration: name={var_decl.name}, value_type={type(var_decl.value).__name__ if var_decl.value else None}", file=sys.stderr)
                if isinstance(var_decl.value, ArrowFunctionExpression):
                    print(f"Confirmed ArrowFunctionExpression for {var_decl.name}", file=sys.stderr)
                    return VariableDeclarationExpression(var_decl.name, var_decl.line, var_decl.value)
                return var_decl
            elif ctx.consoleCommand():
                return self.visit(ctx.consoleCommand(), input_lines)
            elif ctx.ifStatement():
                return self.visit(ctx.ifStatement(), input_lines)
            elif ctx.forStatement():
                return self.visit(ctx.forStatement(), input_lines)
            elif ctx.useEffectCall():
                return self.visit(ctx.useEffectCall(), input_lines)
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
            elif ctx.arrayDeclaration():
                return self.visit(ctx.arrayDeclaration(), input_lines)
            elif ctx.dateDeclaration():
                return self.visit(ctx.dateDeclaration(), input_lines)
            elif ctx.hookCall():  # Handle hookCall
                return self.visit(ctx.hookCall(), input_lines)
            else:
                print(f"Warning: Unhandled statement at line {ctx.start.line}: '{ctx.getText()}'", file=sys.stderr)
                return None
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
                return self.visit(ctx.hookCall(), input_lines)
            else:
                error_msg = f"Unhandled content child at line {ctx.start.line}: '{ctx.getText()}'"
                print(error_msg, file=sys.stderr)
                raise ValueError(error_msg)
        elif isinstance(ctx, codeDebugParser.ElementContext):
            children = list(ctx.getChildren())
            print(f"ElementContext children: {[child.getText() for child in children]}", file=sys.stderr)
            open_tag = ""
            close_tag = ""
            content = []
            line = ctx.start.line
            if ctx.openTag():
                open_tag_token = ctx.openTag().JSX_OPEN_TAG() or ctx.openTag().TAG_OPEN_TAG()
                open_tag = open_tag_token.getText().lstrip('<').rstrip('>') if open_tag_token else ""
                close_tag = ctx.closeTag().getText().lstrip('</').rstrip('>') if ctx.closeTag() else ""
                if open_tag and close_tag and open_tag != close_tag:
                    print(f"Mismatched tags at line {line}: open_tag '{open_tag}' does not match close_tag '{close_tag}'", file=sys.stderr)
            elif ctx.selfClosingTag():
                open_tag = ctx.selfClosingTag().getText().lstrip('<').rstrip('/>')
                close_tag = open_tag
            elif ctx.fragmentOpen() or ctx.emptyFragment():
                open_tag = ""
                close_tag = ""
            for child in ctx.elementContent():
                content.append(self.visit(child, input_lines))
            print(f"Created ElementExpression with open_tag: {open_tag}, close_tag: {close_tag}, content: {[type(c).__name__ for c in content]}", file=sys.stderr)
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
            else:
                error_msg = f"Unsupported element content at line {ctx.start.line}: '{ctx.getText()}'"
                print(error_msg, file=sys.stderr)
                raise ValueError(error_msg)
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
            elif ctx.arrowFunction():
                value = self.visit(ctx.arrowFunction(), input_lines)
            return VariableDeclarationExpression(name, line, value)
        elif isinstance(ctx, codeDebugParser.ArrowFunctionContext):
            params = [param.getText() for param in ctx.parameter_list().parameter()] if ctx.parameter_list().parameter() else []
            body = []
            if ctx.content():
                content_nodes = ctx.content()
                if isinstance(content_nodes, list):
                    body = [self.visit(content, input_lines) for content in content_nodes]
                else:
                    body = [self.visit(content_nodes, input_lines)]
            elif ctx.element():
                body = [self.visit(ctx.element(), input_lines)]
            line = ctx.start.line
            return ArrowFunctionExpression(params, body, line)
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
        elif isinstance(ctx, codeDebugParser.ArrayValueContext):
            line = ctx.start.line
            if ctx.numberArray():
                values = [NumberExpression(num.getText(), line) for num in ctx.numberArray().NUMBER()]
                return ArrayExpression(values, line)
            elif ctx.stringArray():
                values = [self.visit(value, input_lines) for value in ctx.stringArray().stringValue()]
                return ArrayExpression(values, line)
            elif ctx.arrayArray():
                values = [self.visit(value, input_lines) for value in ctx.arrayArray().array()]
                return ArrayExpression(values, line)
            else:
                error_msg = f"Unhandled array value type at line {line}: '{ctx.getText()}'"
                print(error_msg, file=sys.stderr)
                raise ValueError(error_msg)
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
                return value
            return None
        elif isinstance(ctx, codeDebugParser.ValueForInitializationContext):
            line = ctx.start.line
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
                return StringExpression(ctx.NULL().getText(), line)
            elif ctx.SYMBOL_FUNC():
                return StringExpression(ctx.SYMBOL_FUNC().getText(), line)
            elif ctx.NEW():
                return DateExpression(line)
            else:
                error_msg = f"Unexpected valueForInitialization at line {ctx.start.line}: '{ctx.getText()}'"
                print(error_msg, file=sys.stderr)
                raise ValueError(error_msg)
        elif isinstance(ctx, codeDebugParser.ValueIndicatorContext):
            name = ctx.IDENTIFIER().getText()
            line = ctx.IDENTIFIER().symbol.line
            return ValueIndicatorExpression(name, line)
        elif isinstance(ctx, codeDebugParser.Return_statementContext):
            element = self.visit(ctx.element(), input_lines) if ctx.element() else None
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
        elif isinstance(ctx, codeDebugParser.FunctionalComponentContext):
            name = ctx.IDENTIFIER().getText()
            line = ctx.IDENTIFIER().symbol.line
            params = []
            if ctx.parameter_list() and ctx.parameter_list().parameter():
                param_nodes = ctx.parameter_list().parameter()
                if isinstance(param_nodes, list):
                    params = [param.getText() for param in param_nodes if hasattr(param, 'getText')]
                else:
                    params = [param_nodes.getText()] if hasattr(param_nodes, 'getText') else []
            body = self.visit(ctx.element(), input_lines)
            return FunctionalComponentExpression(name, params, body, line)
        elif isinstance(ctx, codeDebugParser.ClassComponentContext):
            name = ctx.IDENTIFIER(0).getText()
            line = ctx.IDENTIFIER(0).symbol.line
            methods = [self.visit(method, input_lines) for method in ctx.methodDeclaration()] if ctx.methodDeclaration() else []
            return ClassComponentExpression(name, methods, line)
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
            error_msg = f"Unhandled node type at line {ctx.start.line}: {type(ctx).__name__}"
            print(error_msg, file=sys.stderr)
            raise ValueError(error_msg)

def print_parse_tree(ctx, parser, level=0):
    indent = "  " * level
    if isinstance(ctx, TerminalNode):
        token_text = ctx.getText()
        print(f"{indent}{token_text}", file=sys.stderr)
        return
    rule_name = parser.ruleNames[ctx.getRuleIndex()]
    print(f"{indent}({rule_name})", file=sys.stderr)
    if ctx.children:
        for child in ctx.children:
            print_parse_tree(child, parser, level + 1)

def collect_function_names(ast: Expression, context: Context) -> list:
    function_names = set()
    if isinstance(ast, ProgramExpression):
        print(f"Total functions in ProgramExpression: {len(ast.functions)}", file=sys.stderr)
        for i, func in enumerate(ast.functions):
            print(f"Function {i}: {type(func).__name__}", file=sys.stderr)
            if isinstance(func, (FunctionDeclarationExpression, FunctionalComponentExpression, ClassComponentExpression)):
                print(f"Adding function name: {func.name}", file=sys.stderr)
                function_names.add(func.name)
                context.declare_function(func.name, func.line)
            elif isinstance(func, VariableDeclarationExpression):
                print(f"VariableDeclarationExpression: name={func.name}, value_type={type(func.value).__name__ if func.value else None}", file=sys.stderr)
                if isinstance(func.value, ArrowFunctionExpression):
                    print(f"Found ArrowFunctionExpression for {func.name}", file=sys.stderr)
                    function_names.add(func.name)
                    context.declare_function(func.name, func.line)
    print(f"Collected function names: {function_names}", file=sys.stderr)
    sys.stderr.flush()
    return list(function_names)

def collect_used_jsx(expr: Expression, used_tags: set, errors: list):
    if isinstance(expr, ProgramExpression):
        for func in expr.functions:
            collect_used_jsx(func, used_tags, errors)
    elif isinstance(expr, FunctionDeclarationExpression):
        for stmt in expr.body:
            collect_used_jsx(stmt, used_tags, errors)
    elif isinstance(expr, VariableDeclarationExpression):
        if isinstance(expr.value, ArrowFunctionExpression):
            for stmt in expr.value.body:
                collect_used_jsx(stmt, used_tags, errors)
    elif isinstance(expr, ArrowFunctionExpression):
        for stmt in expr.body:
            collect_used_jsx(stmt, used_tags, errors)
    elif isinstance(expr, ReturnStatementExpression) and expr.element:
        collect_used_jsx(expr.element, used_tags, errors)
    elif isinstance(expr, ElementExpression):
        print(f"Found ElementExpression with open_tag: {expr.open_tag}, close_tag: {expr.close_tag} at line {expr.line}", file=sys.stderr)
        if expr.open_tag:
            used_tags.add(expr.open_tag)
            print(f"Added open_tag to used_tags: {expr.open_tag}, used_tags now: {used_tags}", file=sys.stderr)
        if expr.close_tag and expr.close_tag != expr.open_tag:
            used_tags.add(expr.close_tag)
            print(f"Added close_tag to used_tags: {expr.close_tag}, used_tags now: {used_tags}", file=sys.stderr)
            errors.append({
                "error": f"Mismatched JSX tags at line {expr.line}: Opening tag '<{expr.open_tag}>' does not match closing tag '</{expr.close_tag}>'.",
                "suggestion": f"Ensure the closing tag matches the opening tag '<{expr.open_tag}>'.",
            })
        for content in expr.content:
            collect_used_jsx(content, used_tags, errors)
    elif isinstance(expr, (list, tuple)):
        for e in expr:
            collect_used_jsx(e, used_tags, errors)
    if isinstance(expr, ProgramExpression):
        print(f"Collected JSX tags: {used_tags}", file=sys.stderr)
        if not used_tags:
            errors.append({
                "error": "No valid JSX tags found in the program.",
                "suggestion": "Ensure the program contains valid JSX elements or components."
            })
        sys.stderr.flush()

def check_function_return_jsx(expr: Expression, func_name: str) -> tuple[bool, int, str]:
    if isinstance(expr, FunctionDeclarationExpression):
        body = expr.body
    elif isinstance(expr, ArrowFunctionExpression):
        body = expr.body
    else:
        body = expr
    if isinstance(body, (list, tuple)):
        for stmt in body:
            if isinstance(stmt, ReturnStatementExpression) and isinstance(stmt.element, ElementExpression):
                tag = stmt.element.open_tag
                line = stmt.element.line
                print(f"Function {func_name} returns JSX tag '{tag}' at line {line}", file=sys.stderr)
                sys.stderr.flush()
                return True, line, tag
    return False, 0, ""

def check_element_tags(ast: Expression, function_names: list, errors: list):
    used_jsx_tags = set()
    collect_used_jsx(ast, used_jsx_tags, errors)
    print(f"Checking element tags with function names: {function_names}, used JSX tags: {used_jsx_tags}", file=sys.stderr)
    sys.stderr.flush()

    def validate_function(func, func_name: str, line: int):
        if not func_name:
            return
        body = func.body if isinstance(func, (FunctionDeclarationExpression, ArrowFunctionExpression)) else []
        is_jsx_component, return_line, return_tag = check_function_return_jsx(body, func_name)
        is_used_as_jsx = func_name in used_jsx_tags or func_name.lower() in [tag.lower() for tag in used_jsx_tags]
        if is_used_as_jsx:
            if not func_name[0].isupper():
                capitalized_name = func_name[0].upper() + func_name[1:] if len(func_name) > 1 else func_name.upper()
                errors.append({
                    "error": f"Invalid React component name at line {line}: '{func_name}' is used as a component but does not start with an uppercase letter.",
                    "suggestion": f"Rename the function '{func_name}' to '{capitalized_name}' to use it as a React component."
                })
            if return_tag.lower() == func_name.lower():
                errors.append({
                    "error": f"Invalid JSX tag in return statement at line {return_line}: Function '{func_name}' returns a JSX element '<{return_tag}/>' that matches its own name.",
                    "suggestion": f"Avoid using a JSX tag with the same name as the function to prevent recursive or invalid references."
                })

    if isinstance(ast, ProgramExpression):
        for func in ast.functions:
            if isinstance(func, FunctionDeclarationExpression):
                validate_function(func, func.name, func.line)
            elif isinstance(func, VariableDeclarationExpression) and isinstance(func.value, ArrowFunctionExpression):
                validate_function(func.value, func.name, func.line)

    html_tags = {'div', 'span', 'p', 'a', 'button', 'input', 'img', 'h1', 'h2', 'h3', 'ul', 'li', 'table'}
    for tag in used_jsx_tags:
        if tag not in function_names and tag.lower() not in html_tags:
            errors.append({
                "error": f"Invalid JSX tag at line unknown: '{tag}' is used as a JSX tag but no corresponding component is defined.",
                "suggestion": f"Define a component named '{tag[0].upper() + tag[1:]}' or use an existing HTML element."
            })

    print(f"Errors after checking element tags: {errors}", file=sys.stderr)
    sys.stderr.flush()

def process_input(input_content: str):
    required_files = [
        os.path.join(CPL_DEST, "codeDebugLexer.py"),
        os.path.join(CPL_DEST, "codeDebugParser.py")
    ]
    for file in required_files:
        if not os.path.exists(file):
            print(json.dumps({"success": False, "error": f"Missing {file}. Please run 'python run.py gen' to generate lexer/parser files."}))
            print("Run tests completely", file=sys.stderr)
            sys.stderr.flush()
            return

    if not input_content:
        print(json.dumps({"success": False, "errors": [{"error": "No input provided", "suggestion": "Provide valid JavaScript code."}]}))
        print("Run tests completely", file=sys.stderr)
        sys.stderr.flush()
        return

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

    lexer = codeDebugLexer(InputStream(input_content))
    token_stream = CommonTokenStream(lexer)
    parser = codeDebugParser(token_stream)

    parser.removeErrorListeners()
    error_listener = CustomErrorListener(input_content)
    parser.addErrorListener(error_listener)

    try:
        print("Parsing input...", file=sys.stderr)
        sys.stderr.flush()
        print("Parse tree:", file=sys.stderr)
        tree = parser.program()
        print_parse_tree(tree, parser)
        sys.stderr.flush()

        if tree and not tree.getText().strip() == "":
            error_listener.errors = []

        if error_listener.errors:
            print(json.dumps({"success": False, "errors": error_listener.errors}, indent=2))
            print("Run tests completely", file=sys.stderr)
            sys.stderr.flush()
            return

        print("Building AST...", file=sys.stderr)
        sys.stderr.flush()
        print(f"input contents: {input_content}", file=sys.stderr)
        print(f"input content split lines: {input_content.splitlines()}", file=sys.stderr)
        context = Context(input_content.splitlines())
        print(f"Context: {context}", file=sys.stderr)

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

        function_names = collect_function_names(ast, context)
        check_element_tags(ast, function_names, context.errors)

        if context.errors:
            print(json.dumps({"success": False, "errors": context.errors}, indent=2))
            print("Run tests completely", file=sys.stderr)
            sys.stderr.flush()
            return

        print("Interpreting AST...", file=sys.stderr)
        sys.stderr.flush()
        ast.interpret(context)

        if 'useRef' in input_content:
            context.errors.append({
                "error": "useRef hook detected, which is not supported by the current grammar.",
                "suggestion": "Remove useRef or extend the grammar to support it."
            })
        if '=>' in input_content and re.search(r'\bconst\s+\w+\s*=\s*\([^)]*\)\s*=>\s*{', input_content):
            context.errors.append({
                "error": "Arrow function declarations detected, which are not fully supported by the current grammar.",
                "suggestion": "Use traditional function declarations or extend the grammar to support arrow functions."
            })

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
    print("Running testcases...", file=sys.stderr)
    sys.stderr.flush()
    if len(sys.argv) < 3:
        input_content = sys.stdin.read().strip()
        process_input(input_content)
        return
    input_content = sys.argv[2]
    cleaned_input = clean_input(input_content)
    process_input(cleaned_input)

def main(argv):
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