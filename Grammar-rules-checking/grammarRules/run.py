import sys
import os
import subprocess
import json
import traceback
from typing import List
from dotenv import load_dotenv
import re
from antlr4 import *
from CompiledFiles.codeDebugLexer import codeDebugLexer
from CompiledFiles.codeDebugParser import codeDebugParser
from antlr4.error.ErrorListener import ErrorListener

from interpreter.context import Context
from interpreter.expression import Expression, ProgramExpression
from interpreter.non_terminal_expression import (
    FunctionDeclarationExpression, ElementExpression, VariableDeclarationExpression,
    ReturnStatementExpression, StateSetterExpression, ArrayExpression,
    UseEffectExpression, UseCallbackExpression, ConsoleCommandExpression,
    ArrowFunctionExpression, ForExpression, IfExpression
)
from interpreter.terminal_expression import (
    StringExpression, NumberExpression, ImportExpression, ValueIndicatorExpression,
    BigIntExpression, DateExpression, BooleanExpression, BinaryExpression
)

# Load environment variables
load_dotenv()
ANTLR_JAR = os.getenv("ANTLR_DIR")

# Constants
DIR = os.path.dirname(__file__)
CPL_DEST = "CompiledFiles"
LEXER_SRC = "codeDebugLexer.g4"
PARSER_SRC = "codeDebugParser.g4"
TEMP_FILE = "temp.js"

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
        if suggestion:
            error_message += f"\nSuggestion: {suggestion}"
        self.errors.append(error_message)

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
            statements_and_functions = [self.visit(node, input_lines) for node in ctx.main_structure().getChildren() if not isinstance(node, codeDebugParser.Import_statementContext)]
            return ProgramExpression(import_stmt, statements_and_functions)
        elif isinstance(ctx, codeDebugParser.Import_statementContext):
            hooks = [ctx.hook(i).getText() for i in range(len(ctx.hook()))]
            line = ctx.start.line
            return ImportExpression(hooks, line)
        elif isinstance(ctx, codeDebugParser.Function_declarationContext):
            name = ctx.IDENTIFIER().getText()
            line = ctx.IDENTIFIER().symbol.line
            params = [param.getText() for param in ctx.parameter_list().parameter()] if ctx.parameter_list().parameter() else []
            body = [self.visit(content, input_lines) for content in ctx.body_function().content()] if ctx.body_function().content() else []
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
            elif ctx.useCallbackCall():
                return self.visit(ctx.useCallbackCall(), input_lines)
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
            deps = [param.getText() for param in ctx.dependencyArray().parameter()] if ctx.dependencyArray().parameter() else []
            line = ctx.start.line
            return UseEffectExpression(callback, deps, line)
        elif isinstance(ctx, codeDebugParser.UseCallbackCallContext):
            callback = self.visit(ctx.callbackFunction(), input_lines) if ctx.callbackFunction() else None
            deps = [param.getText() for param in ctx.dependencyArray().parameter()] if ctx.dependencyArray().parameter() else []
            line = ctx.start.line
            return UseCallbackExpression(callback, deps, line)
        elif isinstance(ctx, codeDebugParser.CallbackFunctionContext):
            body = [self.visit(content, input_lines) for content in ctx.content()] if ctx.content() else []
            line = ctx.start.line
            return ArrowFunctionExpression([], body, line)
        elif isinstance(ctx, codeDebugParser.ArrowFunctionContext):
            params = [param.getText() for param in ctx.parameter_list().parameter()] if ctx.parameter_list().parameter() else []
            body = [self.visit(content, input_lines) for content in ctx.content()] if ctx.content() else []
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
            values = [self.visit(value, input_lines) for value in ctx.valueForInitialization()] if ctx.valueForInitialization() else []
            line = ctx.start.line
            return ArrayExpression(values, line) if values else None
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
        else:
            print(f"Unhandled node type: {type(ctx).__name__}", file=sys.stderr)
            sys.stderr.flush()
            raise ValueError(f"Unhandled node type: {type(ctx).__name__}")

def process_input(input_content: str):
    """Process the input content through lexer, parser, AST, and interpreter."""
    if not input_content:
        print(json.dumps({"success": False, "error": "No input provided"}))
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

        # Convert parse tree to Interpreter AST
        print("Building AST...", file=sys.stderr)
        sys.stderr.flush()
        context = Context(input_content.splitlines())
        ast_builder = ASTBuilder()
        ast = ast_builder.build(tree, input_content.splitlines())
       
        if ast is None:
            print(json.dumps({"success": False, "errors": ["Failed to build AST"]}))
            print("Run tests completely", file=sys.stderr)
            sys.stderr.flush()
            return

        # Interpret the AST
        print("Interpreting AST...", file=sys.stderr)
        sys.stderr.flush()
        ast.interpret(context)

        # Check for return statement only if the input contains a function declaration
        is_functional_component = "function" in input_content.lower() or "export default" in input_content.lower()
        if is_functional_component and "return" not in input_content.lower():
            context.errors.append("No return statement found in functional component")

        # Output results
        if error_listener.errors or context.errors:
            print(json.dumps({"success": False, "errors": error_listener.errors + context.errors}))
        else:
            print(json.dumps({"success": True, "message": "Input accepted"}))
    except Exception as e:
        print(f"Exception occurred: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        errors = error_listener.errors if error_listener.errors else [f"Error while building AST: {str(e)}"]
        print(json.dumps({"success": False, "errors": errors}))

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