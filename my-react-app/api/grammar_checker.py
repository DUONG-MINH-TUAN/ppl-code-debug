import sys
import json
from antlr4 import *
from codeDebugLexer import codeDebugLexer
from codeDebugParser import codeDebugParser
from antlr4.error.ErrorListener import ErrorListener

class MyErrorListener(ErrorListener):
    def __init__(self):
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Syntax error at line {line}:{column} - {msg}")

def check_grammar(input_text):
    input_stream = InputStream(input_text)
    lexer = codeDebugLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = codeDebugParser(stream)
    
    error_listener = MyErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)
    
    parser.program()
    
    if error_listener.errors:
        return {"success": False, "errors": error_listener.errors}
    return {"success": True, "message": "Valid useEffect syntax"}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "No input provided. Please provide a useEffect code string."}))
        sys.exit(1)
    
    input_text = sys.argv[1]
    result = check_grammar(input_text)
    print(json.dumps(result))