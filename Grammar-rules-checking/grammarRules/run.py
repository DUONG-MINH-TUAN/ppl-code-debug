import sys
import os
import subprocess
import json
from antlr4 import *

# Define your variables
DIR = os.path.dirname(__file__)
ANTLR_JAR = 'D:/antlr4/antlr4-4.9.2-complete.jar'
CPL_Dest = 'CompiledFiles'
LEXER_SRC = 'codeDebugLexer.g4'  # File lexer grammar
PARSER_SRC = 'codeDebugParser.g4'  # File parser grammar


def printUsage():
    print('python run.py gen')
    print('python run.py test "your code here"')

def printBreak():
    print('-----------------------------------------------')

def generateAntlr2Python():
    print('Antlr4 is running...')
    # Tạo thư mục CompiledFiles nếu chưa tồn tại
    os.makedirs(CPL_Dest, exist_ok=True)
    
    # Tạo lexer từ codeDebugLexer.g4
    print(f'Generating lexer from {LEXER_SRC}...')
    subprocess.run(['java', '-jar', ANTLR_JAR, '-o', CPL_Dest, '-no-listener', '-Dlanguage=Python3', LEXER_SRC])
    
    # Tạo parser từ codeDebugParser.g4
    print(f'Generating parser from {PARSER_SRC}...')
    subprocess.run(['java', '-jar', ANTLR_JAR, '-o', CPL_Dest, '-no-listener', '-Dlanguage=Python3', PARSER_SRC])
    
    print('Generate successfully')

def runTest(input_text=None):
    print('Running testcases...')
    
    from CompiledFiles.codeDebugLexer import codeDebugLexer
    from CompiledFiles.codeDebugParser import codeDebugParser
    from antlr4.error.ErrorListener import ErrorListener

    class CustomErrorListener(ErrorListener):
        def __init__(self):
            self.errors = []

        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            self.errors.append(f"Syntax error at line {line}:{column} - {msg}")

    # Kiểm tra ngữ pháp
    try:
        input_stream = InputStream(input_text)
        lexer = codeDebugLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = codeDebugParser(stream)
        
        error_listener = CustomErrorListener()
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
        
        # In danh sách token để debug
        print('List of tokens: ')
        tokens = []
        token = lexer.nextToken()
        while token.type != Token.EOF:
            tokens.append(token.text)
            token = lexer.nextToken()
        tokens.append('<EOF>')
        print(','.join(tokens))

        # Kiểm tra cú pháp toàn bộ program
        parser.program()
        
        if error_listener.errors:
            result = {"success": False, "errors": error_listener.errors}
        else:
            # Thêm kiểm tra cơ bản để đảm bảo là functional component hợp lệ
            if not any("return" in line.lower() for line in input_text.split('\n')):
                result = {"success": False, "errors": ["No return statement found in functional component"]}
            else:
                result = {"success": True, "message": "Valid functional component syntax"}
    except Exception as e:
        result = {"success": False, "errors": [f"Parsing error: {str(e)}"]}
    
    print(json.dumps(result))
    printBreak()
    print('Run tests completely')

def main(argv):
    print('Complete jar file ANTLR  :  ' + str(ANTLR_JAR))
    print('Length of arguments      :  ' + str(len(argv)))    
    printBreak()

    if len(argv) < 1:
        printUsage()
    elif argv[0] == 'gen':
        generateAntlr2Python()    
    elif argv[0] == 'test':
        if len(argv) < 2:
            print(json.dumps({"success": False, "error": "No input provided. Please provide a functional component code string."}))
            printBreak()
            print('Run tests completely')
        else:
            input_text = argv[1]
            runTest(input_text)
    else:
        printUsage()

if __name__ == '__main__':
    main(sys.argv[1:])