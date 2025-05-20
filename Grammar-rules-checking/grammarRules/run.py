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
from interpreter import (
    Context, Expression, ProgramExpression, FunctionDeclarationExpression,
    ElementExpression, VariableDeclarationExpression, ValueIndicatorExpression,
    ReturnStatementExpression, StringExpression, NumberExpression,
    StateSetterExpression, ArrayExpression, BigIntExpression, DateExpression,
    ImportExpression, UseEffectExpression, UseCallbackExpression,
    ConsoleCommandExpression, ArrowFunctionExpression
)

load_dotenv()
ANTLR_JAR = os.getenv("ANTLR_DIR")

# Define variables
DIR = os.path.dirname(__file__)
CPL_Dest = "CompiledFiles"
LEXER_SRC = "codeDebugLexer.g4"
PARSER_SRC = "codeDebugParser.g4"
TEMP_FILE = "temp.js"

def printUsage():
    print("python run.py gen", file=sys.stderr)
    print("python run.py test \"<input string>\"", file=sys.stderr)
    sys.stderr.flush()

def printBreak():
    print("-----------------------------------------------", file=sys.stderr)
    sys.stderr.flush()

def generateAntlr2Python():
    print("Antlr4 is running...", file=sys.stderr)
    os.makedirs(CPL_Dest, exist_ok=True)
    print(f"Generating lexer from {LEXER_SRC}...", file=sys.stderr)
    subprocess.run(["java", "-jar", ANTLR_JAR, "-o", CPL_Dest, "-no-listener", "-Dlanguage=Python3", LEXER_SRC])
    print(f"Generating parser from {PARSER_SRC}...", file=sys.stderr)
    subprocess.run(["java", "-jar", ANTLR_JAR, "-o", CPL_Dest, "-no-listener", "-Dlanguage=Python3", PARSER_SRC])
    print("Generate successfully", file=sys.stderr)
    sys.stderr.flush()

def clean_input(input_string: str) -> str:
    """Clean the input string to remove unwanted characters and normalize format."""
    # Remove surrounding quotes if present
    input_string = input_string.strip()
    if input_string.startswith('"') and input_string.endswith('"'):
        input_string = input_string[1:-1]
    elif input_string.startswith("'") and input_string.endswith("'"):
        input_string = input_string[1:-1]
    
    # Normalize escaped quotes (e.g., \" to ")
    input_string = re.sub(r'\\(["\'])', r'\1', input_string)
    
    # Normalize whitespace and newlines
    input_string = re.sub(r'\s+', ' ', input_string).strip()
    # Reformat to add proper newlines for readability
    lines = input_string.replace(';', ';\n').replace('{', '{\n').replace('}', '\n}')
    return '\n'.join(line.strip() for line in lines.split('\n') if line.strip())

class CustomErrorListener(ErrorListener):
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
        if "missing" in msg:
            missing_token = msg.split("missing ")[1].split(" at")[0].strip()
            missing_token = token_map.get(missing_token, missing_token)
            error_message += f"Missing {missing_token} before '{offending_token}'."
            suggestion = f"Check and add a {missing_token} at the appropriate position."
        elif "mismatched input" in msg:
            expected_token = msg.split("expecting ")[1].strip() if "expecting" in msg else "<unknown>"
            expected_token = token_map.get(expected_token, expected_token)
            error_message += f"Found '{offending_token}' but expected {expected_token}."
            suggestion = f"Check the syntax near '{offending_token}' and ensure {expected_token} is used correctly."
        elif "extraneous input" in msg:
            expected_token = msg.split("expecting ")[1].strip() if "expecting" in msg else "<unknown>"
            expected_token = token_map.get(expected_token, expected_token)
            error_message += f"Unexpected '{offending_token}', expected {expected_token}."
            suggestion = f"Check and remove or replace '{offending_token}' with {expected_token}."
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
    def build(self, ctx, input_lines: List[str]) -> Expression:
        print(f"Building AST for {type(ctx).__name__}", file=sys.stderr)
        sys.stderr.flush()
        return self.visit(ctx, input_lines)

    def visit(self, ctx, input_lines: List[str]) -> Expression:
        print(f"Visiting {type(ctx).__name__}", file=sys.stderr)
        sys.stderr.flush()
        if isinstance(ctx, codeDebugParser.ProgramContext):
            import_stmt = self.visit(ctx.main_structure().import_statement(), input_lines) if ctx.main_structure().import_statement() else None
            functions = [self.visit(func, input_lines) for func in ctx.main_structure().function_declaration()]
            return ProgramExpression(import_stmt, functions)
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
        elif isinstance(ctx, codeDebugParser.ElementContext):
            open_tag = ctx.openTag().IDENTIFIER().getText() if ctx.openTag() else "" if not ctx.emptyFragment() else ""
            close_tag = ctx.closeTag().IDENTIFIER().getText() if ctx.closeTag() else "" if not ctx.emptyFragment() else ""
            line = ctx.start.line
            content = [self.visit(content, input_lines) for content in ctx.elementContent()] if ctx.elementContent() else []
            return ElementExpression(open_tag, close_tag, line, content)
        elif isinstance(ctx, codeDebugParser.FragmentOpenContext):
            return ElementExpression("", "", ctx.start.line, [])
        elif isinstance(ctx, codeDebugParser.FragmentCloseContext):
            return ElementExpression("", "", ctx.start.line, [])
        elif isinstance(ctx, codeDebugParser.EmptyFragmentContext):
            return ElementExpression("", "", ctx.start.line, [])
        elif isinstance(ctx, codeDebugParser.VariableDeclarationContext):
            name = ctx.IDENTIFIER().getText()
            line = ctx.IDENTIFIER().symbol.line
            value = None
            if ctx.stringValue():
                value = self.visit(ctx.stringValue(), input_lines)
            elif ctx.array():
                value = self.visit(ctx.array(), input_lines)
            elif ctx.BIGINT_LITERAL():
                value = BigIntExpression(ctx.BIGINT_LITERAL().getText(), line)
            elif ctx.NEW():
                value = DateExpression(line)
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

        # Check for return statement
        has_return = "return" in input_content.lower()
        if not has_return:
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
        errors = error_listener.errors if error_listener.errors else [f"Parsing error: {str(e)}"]
        print(json.dumps({"success": False, "errors": errors}))

    print("Run tests completely", file=sys.stderr)
    sys.stderr.flush()

def runTest():
    print("Running testcases...", file=sys.stderr)
    sys.stderr.flush()

    # Check if input is provided via command-line argument
    if len(sys.argv) < 3:
        # Fallback to stdin for compatibility with piped input
        input_content = sys.stdin.read().strip()
        process_input(input_content)
        return

    # Read and clean input from command-line argument
    input_content = sys.argv[2]
    cleaned_input = clean_input(input_content)

    # Write cleaned input to temporary file
    try:
        with open(TEMP_FILE, "w", encoding="utf-8") as f:
            f.write(cleaned_input)
        
        # Run the script again with input from temp file
        cmd = f"type {TEMP_FILE} | python {sys.argv[0]} test"
        subprocess.run(cmd, shell=True)
    finally:
        # Clean up temporary file
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)

def main(argv):
    if len(argv) < 1:
        printUsage()
    elif argv[0] == "gen":
        generateAntlr2Python()
    elif argv[0] == "test":
        runTest()
    else:
        printUsage()

if __name__ == "__main__":
    main(sys.argv[1:])