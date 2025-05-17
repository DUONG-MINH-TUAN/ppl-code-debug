import sys
import os
import subprocess
import json
from antlr4 import *
from CompiledFiles.codeDebugLexer import codeDebugLexer
from CompiledFiles.codeDebugParser import codeDebugParser
from antlr4.error.ErrorListener import ErrorListener

# Define your variables
DIR = os.path.dirname(__file__)
ANTLR_JAR = 'D:/antlr4/antlr4-4.9.2-complete.jar'
CPL_Dest = 'CompiledFiles'
LEXER_SRC = 'codeDebugLexer.g4'
PARSER_SRC = 'codeDebugParser.g4'

def printUsage():
    print('python run.py gen', file=sys.stderr)
    print('python run.py test (reads input from stdin)', file=sys.stderr)

def printBreak():
    print('-----------------------------------------------', file=sys.stderr)

def generateAntlr2Python():
    print('Antlr4 is running...', file=sys.stderr)
    os.makedirs(CPL_Dest, exist_ok=True)
    print(f'Generating lexer from {LEXER_SRC}...', file=sys.stderr)
    subprocess.run(['java', '-jar', ANTLR_JAR, '-o', CPL_Dest, '-no-listener', '-Dlanguage=Python3', LEXER_SRC])
    print(f'Generating parser from {PARSER_SRC}...', file=sys.stderr)
    subprocess.run(['java', '-jar', ANTLR_JAR, '-o', CPL_Dest, '-no-listener', '-Dlanguage=Python3', PARSER_SRC])
    print('Generate successfully', file=sys.stderr)

def runTest():
    print('Running testcases...', file=sys.stderr)

    class CustomErrorListener(ErrorListener):
        def __init__(self, input_content):
            self.errors = []
            self.input_lines = input_content.splitlines()

        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            token_map = {
                'RIGHT_PARENTHESIS': 'closing parenthesis `)`',
                'LEFT_PARENTHESIS': 'opening parenthesis `(`',
                'RIGHT_BRACE': 'closing brace `}`',
                'LEFT_BRACE': 'opening brace `{`',
                'SEMICOLON': 'semicolon `;`',
                'COMMA': 'comma `,`',
                'EQUAL': 'equals sign `=`',
                'IMPLIE': 'arrow `=>`'
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

    # Đọc input từ stdin
    input_content = sys.stdin.read().strip()

    if not input_content:
        print(json.dumps({"success": False, "error": "No input provided"}))
        print('Run tests completely', file=sys.stderr)
        return

    # Lấy token từ input để debug
    print('List of token: ', file=sys.stderr)
    input_stream = InputStream(input_content)
    lexer = codeDebugLexer(input_stream)
    tokens = []
    token = lexer.nextToken()
    while token.type != Token.EOF:
        tokens.append(token.text)
        token = lexer.nextToken()
    tokens.append('<EOF>')
    print(','.join(tokens), file=sys.stderr)

    # Parse input
    lexer = codeDebugLexer(InputStream(input_content))
    token_stream = CommonTokenStream(lexer)
    parser = codeDebugParser(token_stream)
    parser.removeErrorListeners()
    error_listener = CustomErrorListener(input_content)
    parser.addErrorListener(error_listener)

    try:
        tree = parser.program()
        print(tree.toStringTree(recog=parser), file=sys.stderr)

        # Nếu parser thành công, bỏ qua lỗi từ CustomErrorListener
        if not any("return" in line.lower() for line in input_content.splitlines()):
            print(json.dumps({"success": False, "errors": ["No return statement found in functional component"]}))
        else:
            print(json.dumps({"success": True, "message": "Input accepted"}))
    except Exception as e:
        # Nếu parser thất bại, trả về lỗi (bao gồm cả lỗi từ CustomErrorListener)
        errors = error_listener.errors if error_listener.errors else [f"Parsing error: {str(e)}"]
        print(json.dumps({"success": False, "errors": errors}))

    print('Run tests completely', file=sys.stderr)

def main(argv):
    if len(argv) < 1:
        printUsage()
    elif argv[0] == 'gen':
        generateAntlr2Python()
    elif argv[0] == 'test':
        runTest()
    else:
        printUsage()

if __name__ == '__main__':
    main(sys.argv[1:])